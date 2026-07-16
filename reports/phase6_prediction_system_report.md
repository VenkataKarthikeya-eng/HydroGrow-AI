# HydroGrow AI — Phase 6: Prediction System & AI Decision Support Interface Report

**Generated Date:** 2026-07-15  
**Phase:** Phase 6 (Prediction System & AI Decision Support)  
**Status:** Completed successfully

---

## 1. Objective

Convert the trained HydroGrow AI machine learning model into a professional prediction system where users can:

1. Enter environmental and plant management parameters
2. Receive a predicted lettuce fresh weight (in grams)
3. View a growth performance category (Excellent / Good / Average / Poor)
4. Get AI-generated cultivation recommendations

---

## 2. System Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    Streamlit Dashboard                    │
│                       (app.py)                           │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │ Environmental│  │    Water     │  │    Plant &    │  │
│  │  Conditions  │  │  Parameters  │  │  Management   │  │
│  │  (3 inputs)  │  │  (4 inputs)  │  │  (6 inputs)   │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬────────┘  │
│         └─────────────────┼─────────────────┘            │
│                           ▼                              │
│              ┌────────────────────────┐                  │
│              │   13 User Inputs       │                  │
│              └────────────┬───────────┘                  │
│                           │                              │
│         ┌─────────────────┼─────────────────┐            │
│         ▼                                   ▼            │
│  ┌──────────────────┐             ┌──────────────────┐   │
│  │  prediction.py   │             │ recommendation   │   │
│  │                  │             │   _engine.py     │   │
│  │  Loads:          │             │                  │   │
│  │  - Final model   │             │  12 rule-based   │   │
│  │  - Feature cols  │             │  agriculture     │   │
│  │  - Calibration   │             │  rules           │   │
│  │    config        │             │                  │   │
│  │                  │             │                  │   │
│  │  Derives 34      │             │  Returns list of │   │
│  │  features from   │             │  recommendations │   │
│  │  13 inputs       │             │                  │   │
│  └────────┬─────────┘             └────────┬─────────┘   │
│           ▼                                ▼             │
│  ┌──────────────────────────────────────────────────┐    │
│  │                Results Panel                      │    │
│  │  • Predicted weight (metric card)                 │    │
│  │  • Growth category (color-coded badge)            │    │
│  │  • Recommendations (warning/info/success cards)   │    │
│  └──────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────┘

External Files:
  models/hydrogrow_final_model.pkl     ← Trained model (NOT retrained)
  models/feature_columns.pkl           ← Ordered feature list
  app/config/feature_calibration.json  ← Data-driven calibration values
```

---

## 3. Input Features

The dashboard accepts 13 user-facing inputs, grouped into 4 sections:

### A) Environmental Conditions
| Input | Unit | Default | Training Range |
|:---|:---|:---:|:---|
| Air Temperature | °C | 22.0 | 19.9 – 25.5 |
| Humidity | % | 60.0 | 57.4 – 61.5 |
| CO2 Level | ppm | 450.0 | 450.3 – 456.1 |

### B) Water Parameters
| Input | Unit | Default | Training Range |
|:---|:---|:---:|:---|
| Water pH | — | 6.2 | 5.8 – 7.4 |
| Water EC | mS/cm | 2.0 | 1.8 – 2.7 |
| Water TDS | — | 1.0 | 0.8 – 1.4 |
| Water Temperature | °C | 23.0 | 22.3 – 26.4 |

### C) Plant Starting Conditions
| Input | Unit | Default | Training Range |
|:---|:---|:---:|:---|
| Initial Seedling Height | cm | 12.0 | 9.8 – 14.5 |
| Initial Seedling Weight | g | 4.0 | 1.2 – 4.9 |
| Initial Root Length | cm | 7.0 | 6.4 – 8.2 |

### D) Management Inputs
| Input | Unit | Default | Training Range |
|:---|:---|:---:|:---|
| Nutrient Solution Added | mL | 400 | 64 – 754 |
| Water Consumption | L | 170 | 30 – 390 |
| Acid Consumption | mL | 40 | 0 – 78 |

---

## 4. Feature Calibration & Derivation Methodology

> **Important Note:** The deployed dashboard accepts simplified user inputs and reconstructs required statistical features using calibration values learned from the training dataset.

The trained model expects **34 features**, many of which are statistical aggregates (mean, min, max, standard deviation) computed over the full growth cycle. Since a user provides only a single representative value per sensor parameter, we derive the remaining statistical columns as follows:

- **`feature_mean`** = user input value (representative of the growth cycle average)
- **`feature_min`** = user input − `min_offset` (median of `mean − min` across 216 training samples)
- **`feature_max`** = user input + `max_offset` (median of `max − mean` across 216 training samples)
- **`feature_std`** = `std_value` (median of the std column across 216 training samples)

These calibration offsets are stored in `app/config/feature_calibration.json` and were computed directly from `data/processed/final_ml_dataset.csv`. They are **not hardcoded** — changing the calibration file automatically changes the feature derivation.

### Calibration Values Summary

| Sensor Group | min_offset | max_offset | std_value |
|:---|:---:|:---:|:---:|
| Water pH | 0.7521 | 0.8457 | 0.4210 |
| Water EC | 0.6944 | 0.7626 | 0.2300 |
| Water TDS | 0.4500 | 0.3813 | 0.2662 |
| Water Temperature | 5.2816 | 5.8743 | 2.1693 |
| Air Temperature | 8.3335 | 17.3389 | 3.5189 |
| Humidity | 16.5099 | 10.7001 | 5.5293 |
| CO2 | 46.8850 | 101.1358 | 22.5461 |

---

## 5. Growth Performance Categories

Categories are defined using quartile thresholds from the training target distribution (`target_total_weight_g`, n=216):

| Category | Weight Range | Percentile |
|:---|:---|:---|
| 🌟 Excellent | ≥ 327 g | 75th percentile and above |
| ✅ Good | 279 – 327 g | 50th to 75th percentile |
| 📊 Average | 241 – 279 g | 25th to 50th percentile |
| ⚠️ Poor | < 241 g | Below 25th percentile |

---

## 6. Recommendation Rules

The recommendation engine evaluates inputs against established hydroponic lettuce growing guidelines:

| Parameter | Optimal Range | Warning If Below | Warning If Above |
|:---|:---|:---|:---|
| Water pH | 5.5 – 6.5 | Nutrient absorption decreases | Iron/manganese become unavailable |
| Water EC | 1.2 – 2.5 mS/cm | Insufficient nutrients | Osmotic stress, tip burn |
| Air Temperature | 18 – 24°C | Growth rate slows | Bolting risk, bitter taste |
| Humidity | 50 – 70% | Transpiration stress | Fungal disease risk |
| CO2 | 400 – 800 ppm | Below ambient, supplement | Diminishing returns |
| Water Temperature | 18 – 24°C | Slow nutrient uptake | Low dissolved oxygen, Pythium risk |
| Nutrient Solution | > 100 mL | Check dosing system | Monitor EC for salt buildup |
| Seedling Weight | > 2.0 g | Transplant at larger stage | — |
| Seedling Height | > 10.0 cm | Allow extra growing days | — |

---

## 7. Prediction Workflow

1. User enters 13 parameters via sliders and number inputs
2. `prediction.py` loads the trained model, feature column order, and calibration config
3. 13 inputs are expanded into 34 features using calibration offsets
4. The sklearn Pipeline (StandardScaler → LinearRegression) predicts the fresh weight
5. The prediction is classified into a growth category using training quartile thresholds
6. `recommendation_engine.py` evaluates the same inputs against optimal ranges
7. Results (weight, category, recommendations) are displayed in the dashboard

---

## 8. Validation Results

### Standalone Module Tests
- **`prediction.py`**: Successfully loaded model, derived 34 features, predicted 382.77 g (🌟 Excellent) for typical healthy inputs
- **`recommendation_engine.py`**: Generated 9 recommendations for edge-case inputs (warnings for low pH, high EC, high temperature, high humidity, low CO2, high water temp, low nutrients, small seedlings)

### Sample Prediction
| Input | Value |
|:---|:---|
| Air Temperature | 22.0°C |
| Humidity | 60.0% |
| CO2 | 450 ppm |
| Water pH | 6.2 |
| Water EC | 2.0 mS/cm |
| Water TDS | 1.0 |
| Water Temperature | 23.0°C |
| Nutrient Solution | 400 mL |
| Water Consumption | 170 L |
| Acid Consumption | 40 mL |
| Initial Height | 12.0 cm |
| Initial Weight | 4.0 g |
| Initial Root Length | 7.0 cm |

**Result**: Predicted Weight = **382.77 g** (🌟 Excellent)

---

## 9. Limitations

1. **Model Accuracy**: The underlying model has an R² of 0.5470 and RMSE of 41.87 g. Predictions should be treated as estimates, not exact values.
2. **Small Training Dataset**: The model was trained on only 216 plants from 3 experiments. It may not generalize well to substantially different growing conditions.
3. **Statistical Feature Approximation**: The derived min/max/std values are median approximations. Real sensor data would vary per growth cycle. The calibration values assume typical variability patterns observed in the training data.
4. **No Temporal Dynamics**: The model uses cycle-aggregated statistics, not time-series data. It cannot capture within-cycle growth dynamics.
5. **Rule-Based Recommendations**: The recommendation engine uses static rules, not learned patterns. A larger dataset could enable ML-based recommendation generation.

---

## 10. Future Improvements

1. **More Training Data**: Collect additional growth cycles under diverse conditions to improve model accuracy and reduce overfitting.
2. **Advanced Models**: With more data, explore gradient boosting or neural network models that can capture non-linear interactions.
3. **Time-Series Features**: Incorporate daily or weekly sensor readings instead of cycle aggregates for richer feature representation.
4. **ML-Based Recommendations**: Train a separate model on expert-labeled recommendation data to provide more nuanced, data-driven suggestions.
5. **User Authentication & History**: Add user login, prediction history logging, and batch prediction capability.
6. **Cloud Deployment**: Deploy via Streamlit Cloud, AWS, or GCP for remote access by greenhouse operators.
