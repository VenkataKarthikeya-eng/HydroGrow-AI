# HydroGrow AI — Feature Engineering Report

**Generated Date:** 2026-07-15  
**Phase:** Phase 3 (Feature Engineering)  
**Status:** Completed successfully  

## 1. Dataset Overview
- **Number of Samples (Rows):** 216 plants
- **Number of Features (Columns):** 41 features
- **Target Variable:** `target_total_weight_g` (Fresh weight in grams at harvest)

## 2. Feature Standardizations and Mappings
Replicate systems from sheet-level datasets (`replicate_X_tY`) were mapped to harvest systems as follows:
- **Experiment 1**: Replicate X, Tank Y maps to `R{Y}-T{X}`
- **Experiment 2**: Replicate X, Tank Y maps to `R{X}-T{Y}`
- **Experiment 3**: Replicate X, Tank Y maps to `R{X}T{Y}`

## 3. List of Engineered Features
### 3.1 Metadata & Key Identifiers
- `experiment`
- `system`
- `replicate`
- `plant_no`

### 3.2 Target Outcome Variables
- `target_total_weight_g`
- `harvest_plant_height_cm`
- `harvest_shoot_weight_g`
- `harvest_root_weight_g`
- `harvest_root_length_cm`
- `harvest_no_of_leaves`
- `head_diameter_average_cm`
- `canopy_area_cm2`

### 3.3 Environmental Features (Air Parameters)
- `env_air_temperature_max`
- `env_air_temperature_mean`
- `env_air_temperature_min`
- `env_air_temperature_std`
- `env_co2_max`
- `env_co2_mean`
- `env_co2_min`
- `env_co2_std`
- `env_humidity_max`
- `env_humidity_mean`
- `env_humidity_min`
- `env_humidity_std`

### 3.4 Water Quality Features (Root Zone)
- `water_ec_max`
- `water_ec_mean`
- `water_ec_min`
- `water_ec_std`
- `water_ph_max`
- `water_ph_mean`
- `water_ph_min`
- `water_ph_std`
- `water_tds_max`
- `water_tds_mean`
- `water_tds_min`
- `water_tds_std`
- `water_water_temperature_max`
- `water_water_temperature_mean`
- `water_water_temperature_min`
- `water_water_temperature_std`

### 3.5 Management Input Features
- `total_acid_consumption_ml`
- `total_nutrient_solution_added_ml`
- `total_water_consumption_l`

### 3.6 Starting Baseline Features
- `initial_height_mean_cm`
- `initial_root_length_mean_cm`
- `initial_weight_mean_g`

## 4. Missing Value Treatment Summary
- **Summary Rows Exclusion**: Dropped rows in the harvest sheet with `plant_no = NaN` (these were system-level averages included in raw files). This resulted in exactly **216 clean, complete individual plant rows** (72 per experiment).
- **Acid Consumption (Experiment 2)**: Missing `total_acid_consumption_ml` for Experiment 2 (72 records) was filled with **`0.0`**. Acid additions were not logged or needed during this trial, making 0.0 the correct physical representation.
- **Water Quality (pH, EC, TDS, Water Temp)**: Highly complete; 0% missingness after merging, showing successful temporal aggregation and key mapping.
- **No other missing values exist in the final ML dataset.**
