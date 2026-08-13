# HydroGrow AI — Model Training & Evaluation Report

**Generated Date:** 2026-07-15  
**Phase:** Phase 4 (Model Training & Evaluation)  
**Status:** Completed successfully  

## 1. Dataset Information
- **Source Dataset:** `final_ml_dataset.csv`  
- **Target Variable:** `target_total_weight_g` (Fresh plant weight at harvest)  
- **Number of Samples:** 216 plants  
- **Split Ratio:** 80% Training (172 samples), 20% Testing (44 samples)  
- **Number of Features (Input Matrix `X`):** 34 features (Identifiers and post-harvest biological metrics dropped to prevent target leakage).  

## 2. Models Tested
We trained and evaluated three baseline regression models using scikit-learn Pipelines with numeric standard scaling:
1. **Linear Regression** (simple parametric baseline)
2. **Random Forest Regressor** (bagging ensemble of 100 decision trees)
3. **Gradient Boosting Regressor** (boosting ensemble of 100 decision trees)

## 3. Evaluation Results
The models were evaluated on the test set using Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and $R^2$ Score:

| Model | MAE | RMSE | R2 Score |
| --- | --- | --- | --- |
| Linear Regression | 34.904 | 41.8659 | 0.547 |
| Gradient Boosting | 34.9041 | 41.866 | 0.547 |
| Random Forest | 34.9723 | 42.0951 | 0.5421 |

## 4. Best Model Selection & Rationale
- **Selected Model:** `Linear Regression`  
- **Test Performance:** MAE = 34.9040 g, RMSE = 41.8659 g, $R^2$ Score = 0.5470  

## 5. Visualizations Saved
The following evaluation plots have been saved to the `reports/` folder:
- **Actual vs. Predicted Scatter Plot**: [actual_vs_predicted.png](file:///e:/HydroGrow-AI/reports/actual_vs_predicted.png)
- **Feature Importance Chart**: [feature_importance.png](file:///e:/HydroGrow-AI/reports/feature_importance.png)
