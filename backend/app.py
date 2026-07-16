"""
app.py — HydroGrow AI Streamlit Dashboard

A professional prediction interface for hydroponic lettuce growth prediction.
Users enter environmental, water, and plant parameters and receive:
  1. Predicted lettuce fresh weight (grams)
  2. Growth performance category
  3. AI-generated cultivation recommendations

Usage:
    streamlit run app.py
"""

import json
import os
import streamlit as st

# Add project root to sys.path to ensure correct import resolution
import sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.normpath(os.path.join(BASE_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Import project modules
from backend.services.prediction.prediction import predict, calibration
from backend.services.intelligence.recommendation_engine import generate_recommendations
from backend.services.intelligence.explanation_engine import generate_explanation
from backend.chat_interface import render_chat_interface


# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="HydroGrow AI — Smart Growth Prediction",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------------------------
# Custom CSS for professional styling
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 50%, #43A047 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        color: white;
        text-align: center;
    }
    .main-header h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 700;
    }
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }

    /* Metric card styling */
    .metric-card {
        background: linear-gradient(135deg, #E8F5E9, #C8E6C9);
        border: 1px solid #A5D6A7;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card h2 {
        margin: 0;
        font-size: 2.5rem;
        color: #1B5E20;
        font-weight: 800;
    }
    .metric-card p {
        margin: 0.3rem 0 0 0;
        font-size: 1rem;
        color: #2E7D32;
    }

    /* Category badge */
    .category-excellent { background-color: #1B5E20; color: white; padding: 0.5rem 1.5rem; border-radius: 20px; font-weight: 600; display: inline-block; }
    .category-good { background-color: #2E7D32; color: white; padding: 0.5rem 1.5rem; border-radius: 20px; font-weight: 600; display: inline-block; }
    .category-average { background-color: #F57F17; color: white; padding: 0.5rem 1.5rem; border-radius: 20px; font-weight: 600; display: inline-block; }
    .category-poor { background-color: #C62828; color: white; padding: 0.5rem 1.5rem; border-radius: 20px; font-weight: 600; display: inline-block; }

    /* Section headers */
    .section-header {
        border-left: 4px solid #2E7D32;
        padding-left: 12px;
        margin-bottom: 1rem;
    }

    /* Recommendation cards */
    .rec-critical { border-left: 4px solid #C62828; background: #FFEBEE; padding: 0.8rem 1rem; border-radius: 6px; margin-bottom: 0.5rem; }
    .rec-warning { border-left: 4px solid #F57F17; background: #FFF8E1; padding: 0.8rem 1rem; border-radius: 6px; margin-bottom: 0.5rem; }
    .rec-info { border-left: 4px solid #1565C0; background: #E3F2FD; padding: 0.8rem 1rem; border-radius: 6px; margin-bottom: 0.5rem; }
    .rec-success { border-left: 4px solid #2E7D32; background: #E8F5E9; padding: 0.8rem 1rem; border-radius: 6px; margin-bottom: 0.5rem; }

    /* Explanation summary card */
    .summary-card { background: linear-gradient(135deg, #E8F5E9, #C8E6C9); border-left: 5px solid #2E7D32; border-radius: 8px; padding: 1rem 1.5rem; margin-bottom: 1rem; font-size: 1.1rem; font-weight: 500; color: #1B5E20; }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/color/96/plant-under-rain--v1.png", width=80)
    st.title("HydroGrow AI")
    st.markdown("**Smart Hydroponic Growth Prediction System**")

    st.divider()

    st.markdown("#### 📊 Model Information")
    st.markdown(f"- **Model**: Linear Regression Pipeline")
    st.markdown(f"- **Features**: 34 (derived from 13 inputs)")
    st.markdown(f"- **Training Samples**: 216 plants")
    st.markdown(f"- **Target**: Fresh weight (g)")

    st.divider()

    st.markdown("#### 🎯 Growth Categories")
    st.markdown("- 🌟 **Excellent**: ≥ 327 g")
    st.markdown("- ✅ **Good**: 279 – 327 g")
    st.markdown("- 📊 **Average**: 241 – 279 g")
    st.markdown("- ⚠️ **Poor**: < 241 g")

    st.divider()

    st.caption("HydroGrow AI v1.0 — Phase 6")
    st.caption("Feature calibration from training data")


# ---------------------------------------------------------------------------
# Main header
# ---------------------------------------------------------------------------
st.markdown("""
<div class="main-header">
    <h1>🌱 HydroGrow AI</h1>
    <p>Smart Hydroponic Lettuce Growth Prediction & Decision Support System</p>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Load calibration ranges for slider defaults
# ---------------------------------------------------------------------------
direct = calibration["direct_features"]
sensor = calibration["sensor_groups"]


# ---------------------------------------------------------------------------
# Input sections
# ---------------------------------------------------------------------------
st.markdown('<div class="section-header"><h3>📝 Enter Growth Parameters</h3></div>', unsafe_allow_html=True)

col_a, col_b = st.columns(2)

# --- Section A: Environmental Conditions ---
with col_a:
    st.markdown("#### 🌡️ A) Environmental Conditions")

    air_temperature = st.slider(
        "Air Temperature (°C)",
        min_value=10.0, max_value=40.0,
        value=22.0, step=0.5,
        help="Average greenhouse air temperature during the growth cycle"
    )
    humidity = st.slider(
        "Humidity (%)",
        min_value=30.0, max_value=90.0,
        value=60.0, step=1.0,
        help="Average relative humidity in the growing environment"
    )
    co2 = st.slider(
        "CO2 Level (ppm)",
        min_value=300.0, max_value=1000.0,
        value=450.0, step=10.0,
        help="Average CO2 concentration in the growing environment"
    )

# --- Section B: Water Parameters ---
with col_b:
    st.markdown("#### 💧 B) Water Parameters")

    water_ph = st.slider(
        "Water pH",
        min_value=4.0, max_value=9.0,
        value=6.2, step=0.1,
        help="Average pH of the nutrient solution"
    )
    water_ec = st.slider(
        "Water EC (mS/cm)",
        min_value=0.5, max_value=5.0,
        value=2.0, step=0.1,
        help="Average electrical conductivity of the nutrient solution"
    )
    water_tds = st.slider(
        "Water TDS",
        min_value=0.3, max_value=3.0,
        value=1.0, step=0.1,
        help="Average total dissolved solids in the nutrient solution"
    )
    water_temperature = st.slider(
        "Water Temperature (°C)",
        min_value=15.0, max_value=35.0,
        value=23.0, step=0.5,
        help="Average temperature of the nutrient solution"
    )

col_c, col_d = st.columns(2)

# --- Section C: Plant Starting Conditions ---
with col_c:
    st.markdown("#### 🌿 C) Plant Starting Conditions")

    initial_height = st.number_input(
        "Initial Seedling Height (cm)",
        min_value=5.0, max_value=20.0,
        value=12.0, step=0.5,
        help="Average height of seedlings at transplant"
    )
    initial_weight = st.number_input(
        "Initial Seedling Weight (g)",
        min_value=0.5, max_value=10.0,
        value=4.0, step=0.1,
        help="Average weight of seedlings at transplant"
    )
    initial_root_length = st.number_input(
        "Initial Root Length (cm)",
        min_value=3.0, max_value=15.0,
        value=7.0, step=0.5,
        help="Average root length of seedlings at transplant"
    )

# --- Section D: Management Inputs ---
with col_d:
    st.markdown("#### ⚙️ D) Management Inputs")

    nutrient_solution = st.number_input(
        "Nutrient Solution Added (mL)",
        min_value=0.0, max_value=1500.0,
        value=400.0, step=10.0,
        help="Total nutrient solution added during the growth cycle"
    )
    water_consumption = st.number_input(
        "Water Consumption (L)",
        min_value=0.0, max_value=500.0,
        value=170.0, step=5.0,
        help="Total water consumed by the system during the growth cycle"
    )
    acid_consumption = st.number_input(
        "Acid Consumption (mL)",
        min_value=0.0, max_value=200.0,
        value=40.0, step=5.0,
        help="Total pH-down acid solution used during the growth cycle"
    )


# ---------------------------------------------------------------------------
# Prediction button and results
# ---------------------------------------------------------------------------
st.divider()

predict_clicked = st.button(
    "🔬 Predict Lettuce Growth",
    use_container_width=True,
    type="primary"
)

if predict_clicked:
    # Assemble user inputs dictionary
    user_inputs = {
        "air_temperature": air_temperature,
        "humidity": humidity,
        "co2": co2,
        "water_ph": water_ph,
        "water_ec": water_ec,
        "water_tds": water_tds,
        "water_temperature": water_temperature,
        "nutrient_solution_ml": nutrient_solution,
        "water_consumption_l": water_consumption,
        "acid_consumption_ml": acid_consumption,
        "initial_height_cm": initial_height,
        "initial_weight_g": initial_weight,
        "initial_root_length_cm": initial_root_length,
    }

    # --- Run prediction ---
    try:
        result = predict(user_inputs)
        weight = result["predicted_weight"]
        category = result["growth_category"]

        # --- Results display ---
        st.markdown("---")
        st.markdown('<div class="section-header"><h3>📊 Prediction Results</h3></div>', unsafe_allow_html=True)

        res_col1, res_col2, res_col3 = st.columns(3)

        with res_col1:
            st.markdown(f"""
            <div class="metric-card">
                <h2>{weight:.1f} g</h2>
                <p>Predicted Fresh Weight</p>
            </div>
            """, unsafe_allow_html=True)

        with res_col2:
            # Determine category CSS class
            if "Excellent" in category:
                cat_class = "category-excellent"
            elif "Good" in category:
                cat_class = "category-good"
            elif "Average" in category:
                cat_class = "category-average"
            else:
                cat_class = "category-poor"

            st.markdown(f"""
            <div class="metric-card">
                <p style="margin-bottom: 0.5rem;">Growth Performance</p>
                <span class="{cat_class}">{category}</span>
            </div>
            """, unsafe_allow_html=True)

        with res_col3:
            # Training data context
            target = calibration["target_distribution"]
            percentile = "—"
            if weight >= target["q75"]:
                percentile = "Top 25%"
            elif weight >= target["q50"]:
                percentile = "Above Median"
            elif weight >= target["q25"]:
                percentile = "Below Median"
            else:
                percentile = "Bottom 25%"

            st.markdown(f"""
            <div class="metric-card">
                <h2>{percentile}</h2>
                <p>vs. Training Data (mean: {target['mean']:.0f} g)</p>
            </div>
            """, unsafe_allow_html=True)

        # --- Recommendations ---
        recommendations = generate_recommendations(user_inputs)

        # --- AI Growth Explanation ---
        st.markdown("---")
        st.markdown('<div class="section-header"><h3>🤖 AI Growth Explanation</h3></div>', unsafe_allow_html=True)

        explanation = generate_explanation(user_inputs, result, recommendations)

        # Display Prediction Summary Card
        st.markdown(f"""
        <div class="summary-card">
            {explanation['summary']}
        </div>
        """, unsafe_allow_html=True)

        # Display Positive Factors and Improvement Opportunities in two columns
        col_pos, col_imp = st.columns(2)

        with col_pos:
            st.markdown("#### 🌿 Positive Growth Factors")
            if explanation["positive_factors"]:
                for factor in explanation["positive_factors"]:
                    st.markdown(f"**✅ {factor['factor']}**")
                    st.markdown(f"<p style='color: #1B5E20; margin-top: -0.5rem; font-size: 0.95rem;'>{factor['explanation']}</p>", unsafe_allow_html=True)
            else:
                st.write("No parameters are currently in optimal range.")

        with col_imp:
            st.markdown("#### 🔧 Improvement Opportunities")
            if explanation["improvement_opportunities"]:
                for opportunity in explanation["improvement_opportunities"]:
                    st.markdown(f"**⚠️ {opportunity['factor']}**")
                    st.markdown(f"<p style='color: #B71C1C; margin-top: -0.5rem; font-size: 0.95rem;'>{opportunity['explanation']}</p>", unsafe_allow_html=True)
            else:
                st.markdown("<span style='color: #2E7D32; font-weight: 500;'>🎉 All parameters are within optimal ranges! Excellent management.</span>", unsafe_allow_html=True)

        # Display Model Confidence Explanation
        st.markdown(f"""
        <div style="background-color: #F5F5F5; border-left: 4px solid #757575; padding: 0.6rem 1rem; border-radius: 6px; margin-top: 1.5rem; font-size: 0.85rem; color: #616161;">
            ℹ️ <strong>Model Confidence:</strong> {explanation['confidence_explanation']}
        </div>
        """, unsafe_allow_html=True)

        # --- Ask HydroGrow AI Assistant ---
        st.markdown("---")
        render_chat_interface(user_inputs, result, recommendations, explanation)

        # --- Recommendations ---
        st.markdown("---")
        st.markdown('<div class="section-header"><h3>💡 Cultivation Recommendations</h3></div>', unsafe_allow_html=True)

        recommendations = generate_recommendations(user_inputs)

        # Separate by type
        criticals = [r for r in recommendations if r["type"] == "critical"]
        warnings = [r for r in recommendations if r["type"] == "warning"]
        successes = [r for r in recommendations if r["type"] == "success"]

        # Show critical first, then warnings, then successes
        for rec in criticals:
            st.markdown(f"""
            <div class="rec-critical">
                <strong>🚨 Critical Alert — {rec['parameter']} ({rec['value']})</strong><br>
                <p style="margin: 0.3rem 0; font-size: 0.95rem;">{rec['message']}</p>
                <small style="color: #721C24;"><strong>Action:</strong> {rec['action']}</small>
            </div>
            """, unsafe_allow_html=True)
            
        for rec in warnings:
            st.markdown(f"""
            <div class="rec-warning">
                <strong>⚠️ Warning — {rec['parameter']} ({rec['value']})</strong><br>
                <p style="margin: 0.3rem 0; font-size: 0.95rem;">{rec['message']}</p>
                <small style="color: #856404;"><strong>Action:</strong> {rec['action']}</small>
            </div>
            """, unsafe_allow_html=True)

        for rec in successes:
            st.markdown(f"""
            <div class="rec-success">
                <strong>✅ Optimal Condition — {rec['parameter']} ({rec['value']})</strong><br>
                <p style="margin: 0.3rem 0; font-size: 0.95rem;">{rec['message']}</p>
                <small style="color: #155724;"><strong>Action:</strong> {rec['action']}</small>
            </div>
            """, unsafe_allow_html=True)

        # Summary counts
        st.markdown(f"""
        <br>
        <small>
        📋 <strong>Summary:</strong>
        {len(criticals)} critical alert(s) · {len(warnings)} warning(s) · {len(successes)} optimal condition(s)
        </small>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Prediction Error: {str(e)}")
        st.info("Please check that all input values are within valid ranges.")

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown("---")
st.caption(
    "🌱 HydroGrow AI v1.0 — Phase 6: Prediction System & AI Decision Support Interface | "
    "Model trained on 216 lettuce samples | "
    "Statistical features reconstructed using calibration values learned from the training dataset"
)
