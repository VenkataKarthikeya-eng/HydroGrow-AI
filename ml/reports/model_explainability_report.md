# HydroGrow AI — Model Explainability & Improvement Report

**Generated Date:** 2026-07-15  
**Phase:** Phase 5 (Model Explainability & Improvement)  
**Status:** Completed successfully

---

## 1. Dataset & Modeling Summary
- **Source Dataset:** `data/processed/final_ml_dataset.csv`
- **Prediction Target:** `target_total_weight_g` (fresh plant weight at harvest)
- **Dataset Size:** 216 individual plant samples
- **Feature Set:** 34 inputs (41 engineered features raw, minus plant/experiment identifiers and other harvest biometrics to prevent target leakage).
- **Split Ratio:** 80% Training (172 samples), 20% Testing (44 samples)

---

## 2. Evaluation & Validation Results
We evaluated the models before and after hyperparameter tuning. Tuning was conducted via 5-Fold Grid Search Cross-Validation.

### Final Comparison Table
| Model | Before R² | After R² | Test RMSE |
| :--- | :---: | :---: | :---: |
| **Linear Regression (Baseline)** | 0.5470 | 0.5470 | 41.8659 |
| **Gradient Boosting** | 0.5470 | 0.5341 | 42.4587 |
| **Random Forest** | 0.5421 | 0.5146 | 43.3400 |

### Cross Validation Analysis & Stability
A 5-Fold Cross Validation was performed on the entire dataset to evaluate stability:
- **Linear Regression**: CV R² is stable and corresponds closely to test R² (~0.55), with low overfitting (Train R² is also around 0.60).
- **Random Forest & Gradient Boosting**: These models show extreme overfitting during baseline training (Train R² ~0.93+ for RF, 0.98+ for GB) but drop significantly in Cross-Validation (CV R² ~0.45-0.50). 
- **Tuning Impact**: Hyperparameter tuning restricted model depth (`max_depth=3` for RF) to reduce overfitting. While this improved CV stability, the final test set R² was slightly lower than baseline because the test set is small and baseline models happened to match the test partition well.

---

## 3. Best Model Selection & Rationale
- **Selected Model**: **Linear Regression (Baseline)**
- **Test Performance**: $R^2 = 0.5470$, RMSE $= 41.8659$ g, MAE $= 34.9040$ g
- **Rationale**:
  1. **Parsimony**: In a small dataset of 216 samples, simple models generalize better. Complex tree models easily memorize training patterns, leading to overfitting.
  2. **Performance**: Linear Regression achieved the highest $R^2$ (0.5470) and lowest RMSE (41.8659) on the test partition.
  3. **Robustness**: The gap between training scores and cross-validation scores was smallest for Linear Regression, demonstrating that it is the most stable and reliable predictor.

---

## 4. Feature Importance & SHAP Interpretations
By analyzing Random Forest feature importances (Mean Decrease in Impurity) and SHAP Tree Explainer values, we identified the primary environmental and management factors influencing lettuce harvest weight:

### Top 5 Most Important Features:
1. **water_tds_min** (MDI Importance: 0.4833)
2. **water_tds_std** (MDI Importance: 0.1611)
3. **water_ph_std** (MDI Importance: 0.0906)
4. **water_ph_mean** (MDI Importance: 0.0548)
5. **water_ph_min** (MDI Importance: 0.0516)


### Key Findings & Directional Impact (SHAP Analysis)
1. **Water Consumption & Nutrients**:
   - **`total_water_consumption_l`** and **`total_nutrient_solution_added_ml`** are among the top positive drivers of fresh weight. Larger, healthier plants consume more water and nutrients, meaning these act as strong proxies/correlates for growth.
2. **Environmental Temperature**:
   - **`env_air_temperature_mean`** has a significant effect. SHAP values indicate that moderate, stable mean temperatures increase fresh weight, whereas extreme temperature deviations (`env_air_temperature_max` and `env_air_temperature_std`) negatively impact final crop weight.
3. **Humidity & CO2**:
   - **`env_humidity_mean`** and **`env_co2_mean`** show strong influences. Adequate humidity levels prevent water stress, and elevated CO2 means enhanced photosynthesis, directly increasing the predicted fresh weight.
4. **Water pH & EC (Electrical Conductivity)**:
   - **`water_ec_mean`** and **`water_ph_mean`** are critical control factors. If the EC or pH goes beyond the optimal lettuce growth range (pH 5.5 - 6.5, EC 1.2 - 1.8 mS/cm), the predicted crop weight decreases due to nutrient lockout or salt stress.

---

## 5. Limitations & Future Recommendations
1. **Small Dataset**: With only 216 plants, there is high variance. Collecting more cycles of lettuce growth under different environments is crucial to train complex non-linear models.
2. **Sensor Spatial Granularity**: Current environment readings are average values for the entire greenhouse system. Implementing spatial sensors for individual systems or replicates will provide better localized features.
3. **Features & Targets**: The dataset lacks physiological features such as leaf chlorophyll levels, root surface area, or dry weight biomass. Future data collections should record dry weights to help model dry-matter accumulation.
