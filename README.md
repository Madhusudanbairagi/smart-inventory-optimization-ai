# Smart Inventory Optimization Using AI

## 📌 Overview

This project presents an intelligent, data-driven inventory optimization system that uses AI to forecast demand, optimize order quantities, simulate stock movements, and assist in supplier selection.

Built using Python, LightGBM, Optuna, and Streamlit, the system empowers decision-makers to make cost-efficient and risk-aware inventory decisions.

---

## 💡 Key Features

- 🔍 Demand Forecasting using LightGBM with contextual features.
- 📦 EOQ Optimization using cost modeling and Optuna.
- 🔁 Inventory Simulation with lead-time and restock logic.
- 🤝 Supplier Scoring and Comparison using rule-based metrics.
- 🔄 What-If Simulation to test policy and market changes.
- 📊 Streamlit Dashboard for business-friendly insights.

---

## 📁 Project Structure

├── app.py # Streamlit dashboard
├── requirements.txt # Dependencies
├── /data # sales.csv, products.csv, suppliers.csv, etc.
├── /modules # forecasting.py, simulation.py, optimization.py
├── /reports # supplier comparison and visual outputs
├── /notebooks # Optional Jupyter notebooks
└── Project_Report.pdf # Final academic report

---

## 🛠️ Technology Stack

- Python 3.10+
- Streamlit
- LightGBM
- Optuna
- Pandas, NumPy, Plotly, Seaborn

---

## 🚀 How to Run the Dashboard

```bash
cd dashboard/
streamlit run app.py
