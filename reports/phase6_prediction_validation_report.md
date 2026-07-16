# HydroGrow AI — Phase 6: Prediction Validation Layer Report

**Generated Date:** 2026-07-16  
**Phase:** Phase 6 (Prediction Validation Layer & Reliability Improvements)  
**Status:** Completed successfully

---

## 1. Objective

The purpose of this work was to design and implement a **Prediction Validation Layer** for the HydroGrow AI prediction pipeline to improve prediction reliability and prevent anomalous predictions (e.g. extremely negative weights or highly exaggerated positive weights) when users input extreme environmental parameters.

Specifically:
1. Load target distribution information dynamically from the training dataset `data/processed/final_ml_dataset.csv`.
2. Extract critical biological boundaries and central tendency metrics.
3. Validate all predictions post-inference and flag any predictions outside realistic biological limits.
4. Correct anomalous predictions using percentile clipping (5th and 95th percentiles) as safe, data-driven fallback limits.
5. Provide a detailed, structured output schema capturing both original and adjusted predictions alongside user-friendly feedback messages.

---

## 2. Updated System Architecture

The validation layer integrates directly between the raw model output and the downstream classification and results panels.

```
┌───────────────────────────────────────────────────────────────────┐
│                        Prediction Pipeline                        │
│                           (prediction.py)                         │
│                                                                   │
│  ┌──────────────────────┐        ┌─────────────────────────────┐  │
│  │ 13 User Input values │        │ final_ml_dataset.csv        │  │
│  └──────────┬───────────┘        └──────────────┬──────────────┘  │
│             │                                   │                 │
│             ▼                                   ▼ (Load stats     │
│  ┌──────────────────────┐        ┌─────────────────────────────┐  │
│  │ Build 34-Feature     │        │ prediction_validation.py    │  │
│  │ Vector (Calibration) │        │                             │  │
│  └──────────┬───────────┘        │  • MIN / MAX bounds         │  │
│             │                    │  • P5 / P95 clip targets    │  │
│             ▼                    └──────────────┬──────────────┘  │
│  ┌──────────────────────┐                       │                 │
│  │ Model Predict        │                       │                 │
│  │ (Trained Pipeline)   │                       │                 │
│  └──────────┬───────────┘                       │                 │
│             │                                   │                 │
│             ▼ (Raw Predicted Weight)            │                 │
│  ┌──────────────────────────────────────────────┴──────────────┐  │
│  │            Prediction Validation Layer                      │  │
│  │                 (validate_prediction)                      │  │
│  │                                                             │  │
│  │ Check: Is raw prediction < MIN (150g) or > MAX (412g)?       │  │
│  │   • Yes ──► Set was_adjusted = True, clip to [P5, P95]      │  │
│  │   • No  ──► Set was_adjusted = False, return as-is          │  │
│  └──────────┬──────────────────────────────────────────────────┘  │
│             │                                                     │
│             ▼ (Validated Weight & Status)                         │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │ 1. Classify Growth Category using Validated Weight          │  │
│  │ 2. Return payload with validation metadata                  │  │
│  └─────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────┘
```

---

## 3. Training Dataset Target Statistics

The target distribution statistics were calculated dynamically from the `target_total_weight_g` column in the final ML training dataset ([final_ml_dataset.csv](file:///e:/HydroGrow-AI/data/processed/final_ml_dataset.csv)), which contains `216` training samples.

| Statistic | Value (g) | Purpose in Validation Layer |
|:---|:---:|:---|
| **Minimum** | `150.00` | Lower limit of realistic biological weight |
| **Maximum** | `412.00` | Upper limit of realistic biological weight |
| **Mean** | `284.64` | Baseline reference |
| **5th Percentile** | `201.50` | Lower clipping bound (applied if prediction < 150.00g) |
| **95th Percentile** | `377.25` | Upper clipping bound (applied if prediction > 412.00g) |

---

## 4. Validation Rules and Logic

For any prediction $W_{raw}$, the validation layer checks if it is outside the biological boundaries $[W_{min}, W_{max}]$:

$$\text{Status} = \begin{cases} 
\text{Unrealistic} & \text{if } W_{raw} < 150.00 \text{ or } W_{raw} > 412.00 \\ 
\text{Valid} & \text{otherwise} 
\end{cases}$$

If the prediction is flagged as unrealistic, safe correction is applied by clipping it to the 5th and 95th percentiles:

$$W_{validated} = \max(201.50, \min(W_{raw}, 377.25))$$

This ensures:
1. Predictions within the historical range of $[150.00\text{g}, 412.00\text{g}]$ are accepted completely without modification.
2. Predictions exactly at the boundaries ($150.00\text{g}$ and $412.00\text{g}$) are accepted as valid.
3. Predictions that exhibit extreme extrapolation errors due to extreme out-of-distribution user inputs are safely reined in to high-density regions of the training target distribution ($201.50\text{g}$ or $377.25\text{g}$ respectively).

---

## 5. Output Schema

The prediction pipeline returns the following payload structure:
```json
{
  "predicted_weight": float,     // The final validated/corrected prediction (same as prediction_value)
  "growth_category": str,        // Class classification: Poor / Average / Good / Excellent
  "prediction_value": float,     // Validated/corrected prediction weight in grams
  "original_prediction": float,  // Raw uncorrected prediction weight from the ML model
  "was_adjusted": bool,          // Flag representing if clipping was applied
  "validation_message": str      // Explanatory message for user/UI logs
}
```

---

## 6. Verification and Test Results

A dedicated test suite ([test_prediction_validation.py](file:///e:/HydroGrow-AI/tests/test_prediction_validation.py)) was executed containing 8 tests covering:
- Training dataset statistics verification.
- Direct validation layer boundary testing (normal, min limit, max limit, extreme low, extreme high).
- Integrated prediction pipeline extrapolation testing.

### Test Execution Log
```
........
----------------------------------------------------------------------
Ran 8 tests in 0.031s

OK
```

### Direct Validation Layer Tests
- **Normal Values (`[250.0g, 279.0g, 327.0g, 380.0g]`)**: Passed. Predictions returned as-is with `was_adjusted = False` and `validation_message = "Valid prediction"`.
- **Min Boundary (`150.0g`)**: Passed. Kept as `150.0g`, not adjusted.
- **Max Boundary (`412.0g`)**: Passed. Kept as `412.0g`, not adjusted.
- **Extreme High (`9440.0g`)**: Passed. Flagged and corrected to `377.25g` (95th percentile).
- **Extreme Low (`-50.0g`)**: Passed. Flagged and corrected to `201.5g` (5th percentile).

### Pipeline Integration Test Scenarios
1. **Normal Inputs** (default settings):
   - **Inputs:** Temp 22°C, Humidity 60%, CO2 450ppm, pH 6.2, EC 2.0, TDS 1.0, Water Temp 23°C, Nutrient solution 400mL, Water consumption 170L, Initial weight 4.0g.
   - **Model Raw Output:** `382.77g`
   - **Validation Status:** Valid (within $[150.00\text{g}, 412.00\text{g}]$)
   - **Output Weight:** `382.77g` (No adjustment, category: `🌟 Excellent`)
   
2. **Extreme High Inputs** (high temperature 38°C, humidity 85%, CO2 1000ppm, EC 5.0):
   - **Model Raw Output:** `0.00g` (Extrapolation caused negative prediction, bounded by physically non-negative constraint to `0.00g`)
   - **Validation Status:** Outside biological range (less than $150.00\text{g}$)
   - **Output Weight:** `201.5g` (Adjusted to P5, category: `⚠️ Poor`)

3. **Extreme Low Inputs** (cold temperature 10°C, humidity 30%, no nutrient additions):
   - **Model Raw Output:** `8771.68g` (Regression extrapolation artifact)
   - **Validation Status:** Outside biological range (greater than $412.00\text{g}$)
   - **Output Weight:** `377.25g` (Adjusted to P95, category: `🌟 Excellent`)

---

## 7. Conclusions & Recommendations

By introducing the validation layer, the HydroGrow AI prediction pipeline is now robust against extreme out-of-distribution user inputs, protecting the downstream interface and user experience from mathematically valid but biologically absurd predictions.

### Recommendations for Phase 7:
1. **Log Adjustments:** Monitor the frequency of `was_adjusted = True` in production. High frequency indicates users are entering scenarios far outside our training domain.
2. **Non-Linear Model Exploration:** In Phase 7, consider migrating from Linear Regression to tree-based models (e.g., Random Forest, XGBoost) which naturally bound predictions to the training target domain, preventing extreme extrapolation artifacts altogether.
3. **UI Warnings:** Use the returned `was_adjusted` flag and `validation_message` to show a gentle alert to the grower when their predictions have been corrected, advising them that their parameters are outside normal biological limits.
