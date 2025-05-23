# scenario_presets.py
from datetime import datetime, timedelta

SCENARIOS = {
    "baseline": {
        "name": "🔵 Baseline Policy",
        "color": "#3498db",
        "description": "Current operational parameters with optimized supplier selection",
        "params": {}
    },
    "supplier_disruption": {
        "name": "⚠️ Supplier Crisis (2x Lead Time)",
        "color": "#e74c3c",
        "description": "Simulate primary supplier failure with backup supplier activation",
        "params": {
            "force_supplier_id": "SUPPLIER_B",
            "enable_risk": True,
            "lead_time": 14  # Days (normal = 7)
        }
    },
    "moq_optimization": {
        "name": "📉 MOQ Negotiation (100→50)",
        "color": "#2ecc71", 
        "description": "Test impact of reduced minimum order quantities with Supplier C",
        "params": {
            "force_supplier_id": "SUPPLIER_C",
            "MOQ": 50
        }
    },
    "cost_reduction": {
        "name": "💰 Holding Cost Cut (20%→15%)",
        "color": "#9b59b6",
        "description": "Evaluate warehouse efficiency improvements",
        "params": {
            "holding_rate": 0.15
        }
    },
    "demand_collapse": {
        "name": "📉 Market Downturn (-30% Demand)",
        "color": "#f1c40f",
        "description": "Simulate 30% demand reduction across entire forecast period",
        "params": {
            "demand_mods": {
                (datetime.today() + timedelta(days=i)).strftime("%d-%m-%Y"): 
                int(0.7 * 100)  # Replace 100 with actual forecast lookup
                for i in range(0, 30)
            }
        }
    },
    "safety_stock_increase": {
        "name": "🛡️ Safety Stock +25%",
        "color": "#e67e22",
        "description": "Stress test inventory buffers against demand variability",
        "params": {
            "safety_stock_multiplier": 1.25
        }
    },
    "perfect_storm": {
        "name": "🌪️ Perfect Storm Scenario",
        "color": "#2c3e50",
        "description": "Combined supply chain disruption + demand spike",
        "params": {
            "force_supplier_id": "SUPPLIER_D",
            "lead_time": 21,
            "demand_mods": {
                (datetime.today() + timedelta(days=5)).strftime("%d-%m-%Y"): 250,
                (datetime.today() + timedelta(days=6)).strftime("%d-%m-%Y"): 275
            },
            "holding_rate": 0.25,
            "enable_risk": True
        }
    }
}