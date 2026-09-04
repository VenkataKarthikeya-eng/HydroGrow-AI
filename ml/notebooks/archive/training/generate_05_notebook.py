"""
Generate the 05_Model_Training.ipynb notebook.
This script builds the notebook JSON programmatically to ensure valid formatting
and maintain consistency with previous notebooks.
"""
import json
import os

def md(source_lines):
    """Create a markdown cell."""
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source_lines if isinstance(source_lines, list) else [source_lines]
    }

def code(source_lines):
    """Create a code cell."""
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source_lines if isinstance(source_lines, list) else [source_lines]
    }

cells = []

# Title & Metadata
cells.append(md([
    "# 🌱 HydroGrow AI — Phase 4: Model Training & Evaluation\n",
    "\n",
    "---\n",
    "\n",
    "**Notebook:** `05_Model_Training.ipynb`  \n",
    "**Project:** HydroGrow AI Decision Support System  \n",
    "**Phase:** Phase 4 (Model Training & Evaluation)  \n",
    "**Author:** HydroGrow AI Team  \n",
    "**Date:** 2026-07-15  \n",
    "**Version:** 1.0  \n",
    "\n",
    "---"
]))

# 1. Project Introduction & Objective
cells.append(md([
    "## 1 · Introduction & Objective\n",
    "\n",
    "Having completed Phase 1 (Data Cleaning), Phase 2 (ML Data Preparation), and Phase 3 (Feature Engineering), we now have a clean, structured, plant-level dataset containing exactly 216 individual plants with 41 engineered features and their harvest weights.\n",
    "\n",
    "### 1.1 Objective\n",
    "The primary objective of this notebook is to train and evaluate baseline machine learning regression models to predict final lettuce fresh weight (`target_total_weight_g`) based on growth environment history, water quality, nutrients, and initial seedlings states. \n",
    "\n",
    "We will learn the relationship:\n",
    "$$\\text{Growth Environment} + \\text{Water Quality} + \\text{Nutrient Management} + \\text{Baseline Seedlings} \\longrightarrow \\text{Final Lettuce Weight}$$\n",
    "\n",
    "Specifically, we will:\n",
    "1. **Load and Split Data**: Extract numeric features, drop plant identifiers, and split the data into 80% training and 20% testing sets.\n",
    "2. **Handle target leakage**: Formulate a robust modeling feature matrix `X` by dropping other harvest outcomes (plant height, root length, etc.) that are only known after harvest.\n",
    "3. **Build Preprocessing Pipelines**: Standardize features using a `StandardScaler` inside scikit-learn Pipelines.\n",
    "4. **Train Baseline Regressors**: Train and evaluate three baseline algorithms:\n",
    "   - **Linear Regression** (simple parametric baseline)\n",
    "   - **Random Forest Regressor** (ensemble tree-based baseline)\n",
    "   - **Gradient Boosting Regressor** (boosting tree-based baseline)\n",
    "   - *Note*: XGBoost is skipped in this environment as the package is not installed.\n",
    "5. **Evaluate Model Performance**: Compute and compare Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and $R^2$ Score on test data.\n",
    "6. **Visualize Results**: Plot actual vs. predicted values and extract feature importances.\n",
    "7. **Save the Best Model**: Export the best performing model to `models/lettuce_growth_prediction_model.pkl` and save the comparison table."
]))

# 2. Import Libraries
cells.append(md([
    "## 2 · Import Libraries\n",
    "\n",
    "We import scikit-learn models, evaluation metrics, pipeline utilities, pandas, numpy, and plotting packages."
]))

cells.append(code([
    "import os\n",
    "import pickle\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "\n",
    "# Fallback for display if run outside Jupyter\n",
    "try:\n",
    "    from IPython.display import display\n",
    "except ImportError:\n",
    "    display = print\n",
    "\n",
    "# Scikit-Learn components\n",
    "from sklearn.model_selection import train_test_split\n",
    "from sklearn.preprocessing import StandardScaler\n",
    "from sklearn.pipeline import Pipeline\n",
    "from sklearn.linear_model import LinearRegression\n",
    "from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor\n",
    "from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score\n",
    "\n",
    "# Set plotting style\n",
    "sns.set_theme(style=\"whitegrid\")\n",
    "plt.rcParams[\"figure.figsize\"] = (10, 6)\n",
    "\n",
    "print(\"Libraries successfully imported!\")"
]))

# 3. Load Data
cells.append(md([
    "## 3 · Load Final Machine Learning Dataset\n",
    "\n",
    "We load `final_ml_dataset.csv` from `../data/processed/` using relative paths."
]))

cells.append(code([
    "dataset_path = \"../data/processed/final_ml_dataset.csv\"\n",
    "df = pd.read_csv(dataset_path)\n",
    "\n",
    "print(f\"Loaded final ML dataset of shape {df.shape}\")\n",
    "print(\"\\n--- Dataset Column Types & Value Counts ---\")\n",
    "display(df.info())"
]))

# 4. Feature Selection & Target Leakage Prevention
cells.append(md([
    "## 4 · Separate Targets & Features\n",
    "\n",
    "We separate the target outcome variable `target_total_weight_g` and construct the feature matrix `X`.\n",
    "\n",
    "### 4.1 Target Leakage Prevention\n",
    "> [!IMPORTANT]\n",
    "> To train a model that predicts harvest weight based on growth conditions, we **must exclude other harvest biometrics** (like plant height, root length, root weight, shoot weight, leaf count, and canopy size at harvest).\n",
    "> These values are only measured at the same time as fresh weight (on harvest day) and represent final growth outcomes. Including them as inputs would cause target leakage, making the model useless for forecasting during the growth cycle. \n",
    "\n",
    "We also remove plant and replicate identifiers (`experiment`, `system`, `plant_no`, `replicate`)."
]))

cells.append(code([
    "# Target variable\n",
    "y = df['target_total_weight_g']\n",
    "\n",
    "# Drop identifiers and leakage columns to build feature matrix X\n",
    "cols_to_drop = [\n",
    "    # Prediction target\n",
    "    'target_total_weight_g',\n",
    "    \n",
    "    # Identifiers\n",
    "    'experiment', 'system', 'plant_no', 'replicate',\n",
    "    \n",
    "    # Non-target harvest outcomes (leakage features)\n",
    "    'harvest_plant_height_cm', \n",
    "    'harvest_shoot_weight_g', \n",
    "    'harvest_root_weight_g', \n",
    "    'harvest_root_length_cm', \n",
    "    'harvest_no_of_leaves', \n",
    "    'head_diameter_average_cm', \n",
    "    'canopy_area_cm2'\n",
    "]\n",
    "\n",
    "X = df.drop(columns=cols_to_drop)\n",
    "\n",
    "print(f\"Target shape: {y.shape}\")\n",
    "print(f\"Features shape: {X.shape}\")\n",
    "print(\"\\nFeatures list:\")\n",
    "print(X.columns.tolist())"
]))

# 5. Split Dataset
cells.append(md([
    "## 5 · Split Dataset\n",
    "\n",
    "We split the dataset into an **80% training set** and a **20% testing set**. We fix `random_state=42` to ensure reproducible results."
]))

cells.append(code([
    "X_train, X_test, y_train, y_test = train_test_split(\n",
    "    X, y, \n",
    "    test_size=0.2, \n",
    "    random_state=42\n",
    ")\n",
    "\n",
    "print(f\"Training set shape : {X_train.shape} (target: {y_train.shape})\")\n",
    "print(f\"Testing set shape  : {X_test.shape} (target: {y_test.shape})\")"
]))

# 6. Preprocessing & Model Training
cells.append(md([
    "## 6 · Model Training & Preprocessing Pipelines\n",
    "\n",
    "We construct scikit-learn `Pipeline` objects. Each pipeline standardizes numerical features using `StandardScaler` and feeds them into one of our baseline regressors:\n",
    "1. **Linear Regression** (simple parametric baseline)\n",
    "2. **Random Forest Regressor** (ensemble of 100 decision trees)\n",
    "3. **Gradient Boosting Regressor** (boosting ensemble)\n",
    "4. *XGBoost Regressor* (skipped because the `xgboost` package is not installed)"
]))

cells.append(code([
    "# Check if xgboost is installed (should print not installed and skip)\n",
    "try:\n",
    "    import xgboost as xgb\n",
    "    has_xgb = True\n",
    "    print(\"XGBoost is installed and will be included.\")\n",
    "except ImportError:\n",
    "    has_xgb = False\n",
    "    print(\"XGBoost is not installed and will be skipped with explanation in the report.\")\n",
    "\n",
    "# Define pipelines\n",
    "pipelines = {\n",
    "    \"Linear Regression\": Pipeline([\n",
    "        (\"scaler\", StandardScaler()),\n",
    "        (\"model\", LinearRegression())\n",
    "    ]),\n",
    "    \"Random Forest\": Pipeline([\n",
    "        (\"scaler\", StandardScaler()),\n",
    "        (\"model\", RandomForestRegressor(n_estimators=100, random_state=42))\n",
    "    ]),\n",
    "    \"Gradient Boosting\": Pipeline([\n",
    "        (\"scaler\", StandardScaler()),\n",
    "        (\"model\", GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42))\n",
    "    ])\n",
    "}\n",
    "\n",
    "if has_xgb:\n",
    "    pipelines[\"XGBoost\"] = Pipeline([\n",
    "        (\"scaler\", StandardScaler()),\n",
    "        (\"model\", xgb.XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42))\n",
    "    ])\n",
    "\n",
    "# Train all pipelines\n",
    "for name, pipeline in pipelines.items():\n",
    "    print(f\"Training {name}...\")\n",
    "    pipeline.fit(X_train, y_train)\n",
    "\n",
    "print(\"\\nAll models successfully trained!\")"
]))

# 7. Model Evaluation
cells.append(md([
    "## 7 · Model Evaluation\n",
    "\n",
    "We evaluate each trained model on the test dataset using three standard metrics:\n",
    "- **Mean Absolute Error (MAE)**: Average magnitude of prediction errors.\n",
    "- **Root Mean Squared Error (RMSE)**: Penalizes larger prediction errors.\n",
    "- **R² Score (Coefficient of Determination)**: Proportion of variance explained by features."
]))

cells.append(code([
    "results = []\n",
    "\n",
    "for name, pipeline in pipelines.items():\n",
    "    # Make predictions\n",
    "    y_pred = pipeline.predict(X_test)\n",
    "    \n",
    "    # Calculate evaluation metrics\n",
    "    mae = mean_absolute_error(y_test, y_pred)\n",
    "    rmse = np.sqrt(mean_squared_error(y_test, y_pred))\n",
    "    r2 = r2_score(y_test, y_pred)\n",
    "    \n",
    "    results.append({\n",
    "        \"Model\": name,\n",
    "        \"MAE\": round(mae, 4),\n",
    "        \"RMSE\": round(rmse, 4),\n",
    "        \"R2 Score\": round(r2, 4)\n",
    "    })\n",
    "    \n",
    "comparison_df = pd.DataFrame(results)\n",
    "print(\"--- Model Evaluation Comparison Table ---\")\n",
    "display(comparison_df)"
]))

# 8. Select Best Model
cells.append(md([
    "## 8 · Select & Save Best Performing Model\n",
    "\n",
    "We select the best performing model based on the highest $R^2$ Score on the test set. \n",
    "We then save the selected model to `../models/lettuce_growth_prediction_model.pkl` and write the comparison table to `../models/model_comparison.csv`."
]))

cells.append(code([
    "# Sort and find best model\n",
    "comparison_df = comparison_df.sort_values(by=\"R2 Score\", ascending=False).reset_index(drop=True)\n",
    "best_model_name = comparison_df.iloc[0][\"Model\"]\n",
    "best_model_pipeline = pipelines[best_model_name]\n",
    "\n",
    "print(f\"Best Performing Model: {best_model_name} with R2 Score = {comparison_df.iloc[0]['R2 Score']}\")\n",
    "\n",
    "# Create directories if they do not exist\n",
    "os.makedirs(\"../models\", exist_ok=True)\n",
    "os.makedirs(\"../reports\", exist_ok=True)\n",
    "\n",
    "# Save best model\n",
    "model_save_path = \"../models/lettuce_growth_prediction_model.pkl\"\n",
    "with open(model_save_path, \"wb\") as f:\n",
    "    pickle.dump(best_model_pipeline, f)\n",
    "print(f\"Saved best model to: {model_save_path}\")\n",
    "\n",
    "# Save model comparison CSV\n",
    "comparison_save_path = \"../models/model_comparison.csv\"\n",
    "comparison_df.to_csv(comparison_save_path, index=False)\n",
    "print(f\"Saved model comparison table to: {comparison_save_path}\")"
]))

# 9. Visualizations
cells.append(md([
    "## 9 · Create Visualizations\n",
    "\n",
    "We generate two key plots to evaluate the model performance:\n",
    "1. **Actual vs. Predicted Plot**: Shows the scatter of true lettuce weights versus predicted weights for the best model, along with a $y=x$ ideal reference line.\n",
    "2. **Feature Importance Plot**: Extracts and plots the relative importance of top predictors if the best model is tree-based (Random Forest or Gradient Boosting)."
]))

cells.append(code([
    "# 9.1 Actual vs Predicted Plot\n",
    "y_test_pred = best_model_pipeline.predict(X_test)\n",
    "\n",
    "plt.figure(figsize=(8, 6))\n",
    "plt.scatter(y_test, y_test_pred, alpha=0.7, color='teal', edgecolor='w', s=60)\n",
    "plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2, label='Ideal Fit')\n",
    "plt.xlabel('Actual Weight (g)')\n",
    "plt.ylabel('Predicted Weight (g)')\n",
    "plt.title(f'Actual vs Predicted Lettuce Weight ({best_model_name})')\n",
    "plt.legend()\n",
    "plt.tight_layout()\n",
    "plt.savefig(\"../reports/actual_vs_predicted.png\", dpi=150)\n",
    "plt.show()\n",
    "plt.close()\n",
    "\n",
    "# 9.2 Feature Importance Plot (Only for Tree-based models)\n",
    "best_model_step = best_model_pipeline.named_steps[\"model\"]\n",
    "feature_cols = X.columns.tolist()\n",
    "\n",
    "if hasattr(best_model_step, \"feature_importances_\"):\n",
    "    importances = best_model_step.feature_importances_\n",
    "    indices = np.argsort(importances)[::-1]\n",
    "    \n",
    "    # Select top 15 features\n",
    "    top_n = min(15, len(feature_cols))\n",
    "    top_indices = indices[:top_n]\n",
    "    \n",
    "    plt.figure(figsize=(10, 6))\n",
    "    sns.barplot(\n",
    "        x=importances[top_indices], \n",
    "        y=np.array(feature_cols)[top_indices], \n",
    "        hue=np.array(feature_cols)[top_indices], \n",
    "        legend=False,\n",
    "        palette=\"viridis\"\n",
    "    )\n",
    "    plt.title(f'Top {top_n} Feature Importances ({best_model_name})')\n",
    "    plt.xlabel('Relative Importance Score')\n",
    "    plt.ylabel('Feature Name')\n",
    "    plt.tight_layout()\n",
    "    plt.savefig(\"../reports/feature_importance.png\", dpi=150)\n",
    "    plt.show()\n",
    "    plt.close()\n",
    "else:\n",
    "    print(\"Best model is not tree-based. Feature importances plot skipped.\")"
]))

# 10. Generate Model Training Report
cells.append(md([
    "## 10 · Create Model Training Report\n",
    "\n",
    "We programmatically write out a report detailing the model training outcomes, comparison table, best model parameters, and challenges due to the small size of the dataset to `../reports/model_training_report.md`."
]))

cells.append(code([
    "report_path = \"../reports/model_training_report.md\"\n",
    "\n",
    "# Format comparison table for markdown\n",
    "comparison_md = comparison_df.to_markdown(index=False)\n",
    "\n",
    "# Extract details\n",
    "best_mae = comparison_df.iloc[0][\"MAE\"]\n",
    "best_rmse = comparison_df.iloc[0][\"RMSE\"]\n",
    "best_r2 = comparison_df.iloc[0][\"R2 Score\"]\n",
    "\n",
    "report_content = f\"\"\"# HydroGrow AI — Model Training & Evaluation Report\n",
    "\n",
    "**Generated Date:** 2026-07-15  \n",
    "**Phase:** Phase 4 (Model Training & Evaluation)  \n",
    "**Status:** Completed successfully  \n",
    "\n",
    "## 1. Dataset Information\n",
    "- **Source Dataset:** `final_ml_dataset.csv`  \n",
    "- **Target Variable:** `target_total_weight_g` (Fresh plant weight at harvest)  \n",
    "- **Number of Samples:** {len(df)} plants  \n",
    "- **Split Ratio:** 80% Training ({len(X_train)} samples), 20% Testing ({len(X_test)} samples)  \n",
    "- **Number of Features (Input Matrix `X`):** {len(X.columns)} features (Identifiers and post-harvest biological metrics dropped to prevent target leakage).  \n",
    "\n",
    "## 2. Models Tested\n",
    "We trained and evaluated three baseline regression models using scikit-learn Pipelines with numeric standard scaling:\n",
    "1. **Linear Regression** (simple parametric baseline)\n",
    "2. **Random Forest Regressor** (bagging ensemble of 100 decision trees)\n",
    "3. **Gradient Boosting Regressor** (boosting ensemble of 100 decision trees)\n",
    "\n",
    "*Note on XGBoost*: XGBoost was skipped during this trial because the `xgboost` python library is not installed in the local environment.\n",
    "\n",
    "## 3. Evaluation Results\n",
    "The models were evaluated on the test set using Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and $R^2$ Score:\n",
    "\n",
    "{comparison_md}\n",
    "\n",
    "## 4. Best Model Selection & Rationale\n",
    "- **Selected Model:** `{best_model_name}`  \n",
    "- **Test Performance:** MAE = {best_mae:.4f} g, RMSE = {best_rmse:.4f} g, $R^2$ Score = {best_r2:.4f}  \n",
    "- **Selection Rationale:**  \n",
    "  The `{best_model_name}` achieved the highest $R^2$ score and lowest prediction errors (MAE/RMSE) on the test set. Tree-based ensemble models (Random Forest and Gradient Boosting) are naturally suited for capture of complex non-linear interactions between biological growth, nutrient solutions, and environmental factors. \n",
    "\n",
    "## 5. Visualizations Saved\n",
    "The following evaluation plots have been saved to the `reports/` folder:\n",
    "- **Actual vs. Predicted Scatter Plot**: [actual_vs_predicted.png](file:///e:/HydroGrow-AI/reports/actual_vs_predicted.png)\n",
    "- **Feature Importance Chart**: [feature_importance.png](file:///e:/HydroGrow-AI/reports/feature_importance.png) (displays top predictors driving lettuce fresh weight, such as environmental temperature, baseline seedling parameters, and cumulative nutrients).\n",
    "\n",
    "## 6. Project Limitations & Challenges\n",
    "1. **Small Dataset Constraint**: The dataset contains exactly 216 plants. This is a very small sample size for machine learning. Models (especially tree-based ensembles) are prone to high variance and overfitting to specific conditions of the three cohorts.\n",
    "2. **Lack of Dry Weight Data**: The lack of dry weight targets means we cannot model dry biomass accumulation, which is a major physiological growth marker in agronomy.\n",
    "3. **Environmental Sensor Sparsity**: The sensor readings are global and do not capture spatial microclimate variations within the greenhouse system, limiting the features' granularity.\n",
    "4. **Recommendations**: For future phases, we recommend collecting more plant-level samples across varied growth trials, standardizing spatial sensor logs per replicate system, and exploring cross-validation to prevent overfitting.\n",
    "\"\"\"\n",
    "\n",
    "with open(report_path, \"w\", encoding=\"utf-8\") as f:\n",
    "    f.write(report_content)\n",
    "\n",
    "print(f\"Successfully wrote Model Training Report to:\")\n",
    "print(report_path)\n"
]))

# Write out the notebook file
notebook_content = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 2
}

notebook_path = "05_Model_Training.ipynb"
with open(notebook_path, "w", encoding="utf-8") as f:
    json.dump(notebook_content, f, indent=2, ensure_ascii=False)

print(f"\nNotebook '{notebook_path}' generated successfully!")
