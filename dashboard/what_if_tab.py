import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Import simulation tools
from what_if_simulator.simulator import run_simulation, compare_scenarios
from what_if_simulator.data_loader import DataLoader as SimDataLoader
from data_loader import DataLoader as DashDataLoader

# Dashboard utility
from utils import format_number, get_forecast_sparkline


def what_if_tab():
    st.title("🧪 What-If Scenario Simulator")

    # ----------------------------------
    # Setup loaders
    # ----------------------------------
    sim_loader = SimDataLoader()
    dash_loader = DashDataLoader()

    # Load forecast only for sparkline (from dashboard data folder)
    forecast_df = dash_loader.load_forecast()
    products = forecast_df['product_id'].unique().tolist()

    # ----------------------------------
    # Product selection
    # ----------------------------------
    product_id = st.selectbox("Select Product", products)

    default_start = datetime.today()
    default_end = default_start + timedelta(days=30)
    col1, col2 = st.columns(2)
    start_date = col1.date_input("Start Date", default_start)
    end_date = col2.date_input("End Date", default_end)

    # ----------------------------------
    # Scenario Settings
    # ----------------------------------
    st.markdown("### ⚙️ Simulation Settings")
    col3, col4 = st.columns(2)
    enable_risk = col3.checkbox("Enable Supplier Variability", value=False)

    supplier_ids = sim_loader.load_all_suppliers()['supplier_id'].unique().tolist()
    force_supplier = col4.selectbox("Force Supplier (Optional)", ["None"] + supplier_ids)
    force_supplier = None if force_supplier == "None" else force_supplier

    holding_rate = st.slider("Inventory Holding Rate (Annual %)", 0.0, 0.5, 0.20, step=0.01)

    # ----------------------------------
    # Optional Demand Modification
    # ----------------------------------
    st.markdown("### ✏️ Demand Adjustments (Optional)")
    demand_modifications = {}
    with st.expander("Modify Demand for Specific Days"):
        mod_date = st.date_input("Choose Date to Modify", default_start)
        mod_qty = st.number_input("New Demand Quantity", min_value=0, step=1)
        if st.button("Add Demand Modification"):
            demand_modifications[mod_date.strftime("%d-%m-%Y")] = mod_qty
            st.success(f"Modification added: {mod_date.strftime('%d-%m-%Y')} → {mod_qty} units")
    
    if start_date >= end_date:
        st.warning("⚠️ Please choose an end date that is after the start date.")
        return

    # ----------------------------------
    # Run Simulation
    # ----------------------------------
    if st.button("▶️ Run Simulation"):
        with st.spinner("Running simulation..."):
            result = run_simulation(
                product_id=product_id,
                start_date=start_date.strftime("%d-%m-%Y"),
                end_date=end_date.strftime("%d-%m-%Y"),
                demand_modifications=demand_modifications,
                enable_risk=enable_risk,
                holding_rate=holding_rate,
                force_supplier_id=force_supplier
            )

        timeline = result['timeline'].reset_index()
        st.write("🧪 Simulation Output Snapshot")
        st.dataframe(timeline.head())  # Show first few rows
        st.write("Columns:", timeline.columns.tolist())  # List columns

        metrics = result['metrics']
        orders = result['orders']

        st.subheader("📊 Daily Simulation Overview")
        timeline['date'] = pd.to_datetime(timeline['date'])  # Safe conversion
        st.write("✅ Inventory values", timeline['inventory'].describe())
        st.write("✅ Demand values", timeline['demand'].describe())


        if 'inventory' in timeline.columns and 'demand' in timeline.columns:
            timeline['date'] = pd.to_datetime(timeline['date'])  # ✅ Ensure datetime index
            st.line_chart(timeline.set_index("date")[['inventory', 'demand']])
        else:
            st.warning("⚠️ Columns missing from timeline.")


        st.subheader("📌 Key Metrics")
        col5, col6, col7 = st.columns(3)
        col5.metric("Total Stockouts", format_number(metrics['stockout_days']))
        col6.metric("Holding Cost", f"₹{metrics['total_holding_cost']:.2f}")
        col7.metric("Ordering Cost", f"₹{metrics['total_ordering_cost']:.2f}")
        st.metric("Stockout Penalty", f"₹{metrics['total_stockout_cost']:.2f}")

        st.subheader("📦 Orders Placed")
        if orders:
            st.dataframe(pd.DataFrame(orders))
        else:
            st.info("No orders were placed during this simulation window.")

        st.subheader("🔮 Forecast Preview")
        st.plotly_chart(get_forecast_sparkline(forecast_df, product_id), use_container_width=True)

    # ----------------------------------
    # Scenario Comparison
    # ----------------------------------
    with st.expander("📈 Compare Scenarios"):
        st.info("Run multiple predefined scenarios to compare results.")

        base = {
            "name": "Baseline",
            "demand_mods": {},
            "params": {
                "enable_risk": False,
                "holding_rate": holding_rate
            }
        }
        spike = {
            "name": "Demand Spike",
            "demand_mods": {(default_start + timedelta(days=5)).strftime("%d-%m-%Y"): 300},
            "params": {"enable_risk": False}
        }
        risk_mode = {
            "name": "Risk + Supplier Change",
            "params": {"enable_risk": True, "force_supplier_id": force_supplier}
        }

        if st.button("📊 Compare Scenarios"):
            with st.spinner("Running scenario comparisons..."):
                comparison = compare_scenarios(
                    product_id=product_id,
                    scenarios=[base, spike, risk_mode],
                    start_date=start_date.strftime("%d-%m-%Y"),
                    end_date=end_date.strftime("%d-%m-%Y")
                )
                st.dataframe(pd.DataFrame(comparison).T)

# For manual testing
if __name__ == '__main__':
    what_if_tab()
