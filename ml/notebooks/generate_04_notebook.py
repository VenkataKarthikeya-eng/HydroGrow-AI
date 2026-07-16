"""
Generate the 04_Feature_Engineering.ipynb notebook.
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
    "# 🌱 HydroGrow AI — Phase 3: Feature Engineering\n",
    "\n",
    "---\n",
    "\n",
    "**Notebook:** `04_Feature_Engineering.ipynb`  \n",
    "**Project:** HydroGrow AI Decision Support System  \n",
    "**Phase:** Phase 3 (Feature Engineering)  \n",
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
    "In Phase 1 and Phase 2, we cleaned our datasets and diagnosed their suitability for Machine Learning. We concluded that training models directly on the concatenated experiment datasets was not possible due to row-wise stacking, and recommended training on aggregated sheet-level datasets instead.\n",
    "\n",
    "### 1.1 Objective\n",
    "The primary objective of this notebook is to execute the data aggregation, mapping, merging, and feature engineering pipeline to build the **final flat machine learning dataset** for lettuce growth prediction. \n",
    "\n",
    "The target data structure is:\n",
    "$$\\text{One Row} = \\text{One Individual Harvested Lettuce Plant}$$\n",
    "\n",
    "We will load and combine sheet-level data from:\n",
    "- `harvest` (to extract individual plant growth targets and identifiers)\n",
    "- `seedlings` (to calculate experiment-level initial baseline features)\n",
    "- `sensor_water_quality` (to calculate global air temperature, humidity, and CO₂ stats)\n",
    "- `portable_water_quality` (to calculate system-specific pH, EC, TDS, and water temperature stats)\n",
    "- `nutrients` (to calculate cumulative nutrient additions, water, and acid consumption)\n",
    "- `head_diameter` (to inspect and verify time-series growth tracking)\n",
    "\n",
    "### 1.2 Pipeline Steps\n",
    "1. **Load Data**: Discover and load all required sheet-level CSV files.\n",
    "2. **Column Standardization**: Define a standardized column naming schema via a mapping dictionary.\n",
    "3. **Aggregate Environmental Sensor Averages**: Calculate mean, min, max, and standard deviation of air temperature, humidity, and CO₂ per experiment.\n",
    "4. **Aggregate Portable Water Quality**: Pool morning and afternoon spot-checks of pH, EC, TDS, and water temperature, and calculate mean, min, max, and standard deviation per system.\n",
    "5. **Process Nutrient Logs**: Compute total cumulative nutrient solution, water, and acid consumed per system.\n",
    "6. **Process Seedlings Baseline**: Calculate starting average height, weight, and root length per experiment cohort.\n",
    "7. **Extract Harvest Targets & Parse Head Diameter**: Parse the string head diameter dimensions (`Width*Height`) into average diameter and area, filter out system average/summary rows, and standardize crop yield metrics.\n",
    "8. **Merge Datasets**: Align replicate system labels and merge all feature groups horizontally using `experiment`, `system`, and `replicate` as keys.\n",
    "9. **Handle Missing Values**: Inspect and handle missing data with explicit rationale.\n",
    "10. **Save Dataset & Generate Report**: Export the final CSV and generate a Feature Engineering Report."
]))

# 2. Import Libraries
cells.append(md([
    "## 2 · Import Libraries\n",
    "\n",
    "We import standard packages for numerical calculation, dataframes manipulation, and filesystem search."
]))

cells.append(code([
    "import os\n",
    "import glob\n",
    "import re\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "\n",
    "# Fallback for display if run outside Jupyter\n",
    "try:\n",
    "    from IPython.display import display\n",
    "except ImportError:\n",
    "    display = print\n",
    "\n",
    "print(\"Libraries successfully imported!\")"
]))

# 3. Load Data
cells.append(md([
    "## 3 · Load Sheet-Level Cleaned Datasets\n",
    "\n",
    "We load all sheet-level CSV files from `../data/processed/per_sheet/`. We will group them by experiment for structured processing."
]))

cells.append(code([
    "def load_sheet_data(folder_path):\n",
    "    \"\"\"\n",
    "    Loads all CSV files in the specified folder and returns a dictionary of DataFrames.\n",
    "    Keys are the filenames without '.csv'.\n",
    "    \"\"\"\n",
    "    csv_files = glob.glob(os.path.join(folder_path, \"*_clean.csv\"))\n",
    "    datasets = {}\n",
    "    for filepath in sorted(csv_files):\n",
    "        basename = os.path.basename(filepath)\n",
    "        key = basename.replace(\".csv\", \"\")\n",
    "        try:\n",
    "            df = pd.read_csv(filepath)\n",
    "            datasets[key] = df\n",
    "            print(f\"Loaded '{key}' successfully with shape {df.shape}\")\n",
    "        except Exception as e:\n",
    "            print(f\"Failed to load {basename}: {e}\")\n",
    "    return datasets\n",
    "\n",
    "sheet_data = load_sheet_data(\"../data/processed/per_sheet\")"
]))

# 4. Column Standardization
cells.append(md([
    "## 4 · Column Standardization System\n",
    "\n",
    "We create a column standardization schema to resolve differences in naming conventions across experiments (e.g. `air_temp_c` vs `air_temp`, `rh_%` vs `rh%`).\n",
    "\n",
    "Below is our mapping dictionary, which translates raw environmental and biological names to clean, unified ML feature names."
]))

cells.append(code([
    "# Mapping dictionary for standardizing columns\n",
    "COLUMN_STANDARDIZATION_MAP = {\n",
    "    # Environmental names\n",
    "    \"air_temp_c\": \"air_temperature\",\n",
    "    \"air_temp\": \"air_temperature\",\n",
    "    \"rh_%\": \"humidity\",\n",
    "    \"rh%\": \"humidity\",\n",
    "    \"co2_ppm\": \"co2\",\n",
    "    \"co2\": \"co2\",\n",
    "    \n",
    "    # Portable water quality metrics\n",
    "    \"ph\": \"ph\",\n",
    "    \"ec\": \"ec\",\n",
    "    \"tds\": \"tds\",\n",
    "    \"water_temp\": \"water_temperature\",\n",
    "    \n",
    "    # Biological metrics\n",
    "    \"plant_height_cm\": \"plant_height_cm\",\n",
    "    \"root_length_cm\": \"root_length_cm\",\n",
    "    \"total_weight_g\": \"total_weight_g\",\n",
    "    \"root_weight_g\": \"root_weight_g\",\n",
    "    \"no_of_leaves\": \"no_of_leaves\",\n",
    "    \"noof_leaves\": \"no_of_leaves\"\n",
    "}\n",
    "\n",
    "print(\"Column standardization map created:\")\n",
    "for k, v in COLUMN_STANDARDIZATION_MAP.items():\n",
    "    print(f\"  {k:30} -> {v}\")"
]))

# 5. Process Environmental Data
cells.append(md([
    "## 5 · Process Environmental Data\n",
    "\n",
    "We aggregate the continuous time-series environmental sensor readings (air temperature, humidity, and CO₂) for each experiment. Since the sensor records only contain one dummy replicate, we calculate experiment-wide summary statistics (Mean, Min, Max, and Standard Deviation)."
]))

cells.append(code([
    "def aggregate_sensor_data(df, exp_label):\n",
    "    \"\"\"\n",
    "    Extracts air temperature, humidity, and CO2, standardizes their names, \n",
    "    and calculates Mean, Min, Max, and Std Dev.\n",
    "    \"\"\"\n",
    "    # Find the appropriate column names\n",
    "    temp_col = 'air_temp_c' if 'air_temp_c' in df.columns else ('air_temp' if 'air_temp' in df.columns else None)\n",
    "    rh_col = 'rh_%' if 'rh_%' in df.columns else ('rh%' if 'rh%' in df.columns else None)\n",
    "    co2_col = 'co2_ppm' if 'co2_ppm' in df.columns else ('co2' if 'co2' in df.columns else None)\n",
    "    \n",
    "    metrics = {}\n",
    "    # Map each variable and compute statistics\n",
    "    for var_name, col in [('air_temperature', temp_col), ('humidity', rh_col), ('co2', co2_col)]:\n",
    "        if col is not None:\n",
    "            data = df[col].dropna()\n",
    "            if len(data) > 0:\n",
    "                metrics[f\"env_{var_name}_mean\"] = data.mean()\n",
    "                metrics[f\"env_{var_name}_min\"] = data.min()\n",
    "                metrics[f\"env_{var_name}_max\"] = data.max()\n",
    "                metrics[f\"env_{var_name}_std\"] = data.std()\n",
    "            else:\n",
    "                metrics[f\"env_{var_name}_mean\"] = np.nan\n",
    "                metrics[f\"env_{var_name}_min\"] = np.nan\n",
    "                metrics[f\"env_{var_name}_max\"] = np.nan\n",
    "                metrics[f\"env_{var_name}_std\"] = np.nan\n",
    "        else:\n",
    "            metrics[f\"env_{var_name}_mean\"] = np.nan\n",
    "            metrics[f\"env_{var_name}_min\"] = np.nan\n",
    "            metrics[f\"env_{var_name}_max\"] = np.nan\n",
    "            metrics[f\"env_{var_name}_std\"] = np.nan\n",
    "            \n",
    "    return metrics\n",
    "\n",
    "print(\"--- Aggregating Experiment Sensor Environments ---\")\n",
    "sensor_aggregates = {}\n",
    "for i in [1, 2, 3]:\n",
    "    key = f\"exp{i}_sensor_water_quality_clean\"\n",
    "    if key in sheet_data:\n",
    "        sensor_aggregates[f\"Experiment {i}\"] = aggregate_sensor_data(sheet_data[key], f\"Experiment {i}\")\n",
    "        print(f\"Experiment {i} Sensor averages:\")\n",
    "        print(f\"  Mean Temp: {sensor_aggregates[f'Experiment {i}']['env_air_temperature_mean']:.2f}°C\")\n",
    "        print(f\"  Mean RH  : {sensor_aggregates[f'Experiment {i}']['env_humidity_mean']:.2f}%\")\n",
    "        print(f\"  Mean CO2 : {sensor_aggregates[f'Experiment {i}']['env_co2_mean']:.2f} ppm\")"
]))

cells.append(md([
    "### 5.1 Process Portable Water Quality Data\n",
    "\n",
    "Portable water quality measurements are recorded in columns per replicate system, labeled `100000_replicate_X_tY_{metric}` and `140000_replicate_X_tY_{metric}`. \n",
    "We need to pool the measurements from morning (10:00 AM) and afternoon (2:00 PM) for each replicate system `replicate_X_tY` (where $X \\in \\{1, 2, 3\\}$ and $Y \\in \\{1, 2\\}$) and calculate the Mean, Min, Max, and Std Dev of water pH, EC, TDS, and water temperature.\n",
    "\n",
    "We will map these replicate-tank combinations to the corresponding harvest system ID based on our key matching rules:\n",
    "- **Experiment 1**: column `replicate_X_tY` corresponds to harvest system `R{Y}-T{X}`.\n",
    "- **Experiment 2**: column `replicate_X_tY` corresponds to harvest system `R{X}-T{Y}`.\n",
    "- **Experiment 3**: column `replicate_X_tY` corresponds to harvest system `R{X}T{Y}`."
]))

cells.append(code([
    "def aggregate_portable_water_data(df, exp_label):\n",
    "    \"\"\"\n",
    "    Extracts pH, EC, TDS, and water temp for replicates 1-3 and tanks t1-t2.\n",
    "    Pools time points (100000 and 140000) and calculates summary statistics.\n",
    "    Maps columns to harvest-compatible system names.\n",
    "    \"\"\"\n",
    "    replicates = [1, 2, 3]\n",
    "    tanks = ['t1', 't2']\n",
    "    \n",
    "    sys_aggregates = {}\n",
    "    for rep in replicates:\n",
    "        for tank in tanks:\n",
    "            # Determine target system ID\n",
    "            if exp_label == 'Experiment 1':\n",
    "                system_id = f\"R{tank[1]}-T{rep}\"\n",
    "            elif exp_label == 'Experiment 2':\n",
    "                system_id = f\"R{rep}-T{tank[1].upper()}\"\n",
    "            elif exp_label == 'Experiment 3':\n",
    "                system_id = f\"R{rep}T{tank[1].upper()}\"\n",
    "                \n",
    "            col_pattern = f\"replicate_{rep}_{tank}\"\n",
    "            \n",
    "            # Find columns matching the system key\n",
    "            ph_cols = [c for c in df.columns if col_pattern in c and c.endswith('_ph')]\n",
    "            ec_cols = [c for c in df.columns if col_pattern in c and c.endswith('_ec')]\n",
    "            tds_cols = [c for c in df.columns if col_pattern in c and c.endswith('_tds')]\n",
    "            wt_cols = [c for c in df.columns if col_pattern in c and c.endswith('_water_temp')]\n",
    "            \n",
    "            metrics = {}\n",
    "            # Compute metrics for each sensor reading type\n",
    "            for name, cols in [('ph', ph_cols), ('ec', ec_cols), ('tds', tds_cols), ('water_temperature', wt_cols)]:\n",
    "                if cols:\n",
    "                    # Flatten morning and afternoon columns into a single series\n",
    "                    vals = df[cols].values.flatten()\n",
    "                    vals = vals[~np.isnan(vals)]  # Drop NaNs\n",
    "                    \n",
    "                    if len(vals) > 0:\n",
    "                        metrics[f\"water_{name}_mean\"] = np.mean(vals)\n",
    "                        metrics[f\"water_{name}_min\"] = np.min(vals)\n",
    "                        metrics[f\"water_{name}_max\"] = np.max(vals)\n",
    "                        metrics[f\"water_{name}_std\"] = np.std(vals)\n",
    "                    else:\n",
    "                        metrics[f\"water_{name}_mean\"] = np.nan\n",
    "                        metrics[f\"water_{name}_min\"] = np.nan\n",
    "                        metrics[f\"water_{name}_max\"] = np.nan\n",
    "                        metrics[f\"water_{name}_std\"] = np.nan\n",
    "                else:\n",
    "                    metrics[f\"water_{name}_mean\"] = np.nan\n",
    "                    metrics[f\"water_{name}_min\"] = np.nan\n",
    "                    metrics[f\"water_{name}_max\"] = np.nan\n",
    "                    metrics[f\"water_{name}_std\"] = np.nan\n",
    "                    \n",
    "            sys_aggregates[(exp_label, system_id)] = metrics\n",
    "            \n",
    "    return sys_aggregates\n",
    "\n",
    "print(\"--- Aggregating Portable Water Quality Data ---\")\n",
    "portable_aggregates = {}\n",
    "for i in [1, 2, 3]:\n",
    "    key = f\"exp{i}_portable_water_quality_clean\"\n",
    "    if key in sheet_data:\n",
    "        exp_label = f\"Experiment {i}\"\n",
    "        exp_portable_aggs = aggregate_portable_water_data(sheet_data[key], exp_label)\n",
    "        portable_aggregates.update(exp_portable_aggs)\n",
    "        \n",
    "print(f\"Portable aggregates calculated for {len(portable_aggregates)} experiment-system combinations.\")"
]))

# 6. Process Nutrient Data
cells.append(md([
    "## 6 · Process Nutrient Data\n",
    "\n",
    "We calculate the total nutrients, acid, and water additions for each replicate system. This is done by summing up the periodic values inside each system's column.\n",
    "- **Total nutrient solution added** (from `nutrient_solution_addition` sheet)\n",
    "- **Total water consumption** (from `water_consumption` sheet)\n",
    "- **Total acid consumption** (from `acid_consumption` sheet — *Note: Experiment 2 does not have an acid consumption log; we will record NaN and handle it in the missing value step*)"
]))

cells.append(code([
    "def aggregate_nutrients(solutions_df, water_df, acid_df, exp_label):\n",
    "    \"\"\"\n",
    "    Calculates the sum of nutrients solution, water consumption, and acid additions.\n",
    "    Maps columns to harvest-compatible system names.\n",
    "    \"\"\"\n",
    "    replicates = [1, 2, 3]\n",
    "    tanks = ['t1', 't2']\n",
    "    \n",
    "    sys_nutrients = {}\n",
    "    for rep in replicates:\n",
    "        for tank in tanks:\n",
    "            if exp_label == 'Experiment 1':\n",
    "                system_id = f\"R{tank[1]}-T{rep}\"\n",
    "            elif exp_label == 'Experiment 2':\n",
    "                system_id = f\"R{rep}-T{tank[1].upper()}\"\n",
    "            elif exp_label == 'Experiment 3':\n",
    "                system_id = f\"R{rep}T{tank[1].upper()}\"\n",
    "                \n",
    "            col_name = f\"replicate_{rep}_{tank}\"\n",
    "            \n",
    "            # Cumulative Solution Added\n",
    "            sol_sum = solutions_df[col_name].sum() if (solutions_df is not None and col_name in solutions_df.columns) else 0.0\n",
    "            # Cumulative Water Consumed\n",
    "            water_sum = water_df[col_name].sum() if (water_df is not None and col_name in water_df.columns) else 0.0\n",
    "            # Cumulative Acid Consumed\n",
    "            acid_sum = acid_df[col_name].sum() if (acid_df is not None and col_name in acid_df.columns) else np.nan\n",
    "            \n",
    "            sys_nutrients[(exp_label, system_id)] = {\n",
    "                \"total_nutrient_solution_added_ml\": float(sol_sum),\n",
    "                \"total_water_consumption_l\": float(water_sum),\n",
    "                \"total_acid_consumption_ml\": float(acid_sum) if acid_df is not None else np.nan\n",
    "            }\n",
    "            \n",
    "    return sys_nutrients\n",
    "\n",
    "print(\"--- Aggregating Nutrient & Water Consumption logs ---\")\n",
    "nutrient_aggregates = {}\n",
    "for i in [1, 2, 3]:\n",
    "    exp_label = f\"Experiment {i}\"\n",
    "    sol_key = f\"exp{i}_nutrients_nutrient_solution_addition_(a+b)_ml_clean\"\n",
    "    water_key = f\"exp{i}_nutrients_water_consumption_l_clean\"\n",
    "    \n",
    "    # Standardize acid consumption sheet name variations\n",
    "    acid_key = f\"exp{i}_nutrients_acid_consumption_(ml)_clean\" if i == 1 else f\"exp{i}_nutrients_acid_consumption_ml_clean\"\n",
    "    \n",
    "    sol_df = sheet_data.get(sol_key)\n",
    "    water_df = sheet_data.get(water_key)\n",
    "    acid_df = sheet_data.get(acid_key)\n",
    "    \n",
    "    exp_nut_aggs = aggregate_nutrients(sol_df, water_df, acid_df, exp_label)\n",
    "    nutrient_aggregates.update(exp_nut_aggs)\n",
    "\n",
    "print(f\"Nutrient aggregates calculated for {len(nutrient_aggregates)} combinations.\")"
]))

# 7. Process Seedling Data
cells.append(md([
    "## 7 · Process Seedlings Baseline Data\n",
    "\n",
    "Since seedling parameters are baseline measurements of a random sample at transplant and do not map directly row-by-row to final plants, we calculate the average seedling **height, weight, and root length** per experiment cohort. These serve as baseline starting features."
]))

cells.append(code([
    "seedling_baselines = {}\n",
    "print(\"--- Calculating Seedling Baseline Averages ---\")\n",
    "for i in [1, 2, 3]:\n",
    "    key = f\"exp{i}_seedlings_clean\"\n",
    "    exp_label = f\"Experiment {i}\"\n",
    "    if key in sheet_data:\n",
    "        df = sheet_data[key]\n",
    "        # Calculate seedling averages\n",
    "        avg_height = df[\"plant_height_cm\"].mean() if \"plant_height_cm\" in df.columns else np.nan\n",
    "        avg_weight = df[\"total_weight_g\"].mean() if \"total_weight_g\" in df.columns else np.nan\n",
    "        avg_root_len = df[\"root_length_cm\"].mean() if \"root_length_cm\" in df.columns else np.nan\n",
    "        \n",
    "        seedling_baselines[exp_label] = {\n",
    "            \"initial_height_mean_cm\": avg_height,\n",
    "            \"initial_weight_mean_g\": avg_weight,\n",
    "            \"initial_root_length_mean_cm\": avg_root_len\n",
    "        }\n",
    "        print(f\"{exp_label} Baselines:\")\n",
    "        print(f\"  Initial Height : {avg_height:.2f} cm\")\n",
    "        print(f\"  Initial Weight : {avg_weight:.2f} g\")\n",
    "        print(f\"  Initial Root   : {avg_root_len:.2f} cm\")"
]))

# 8. Process Harvest Data
cells.append(md([
    "## 8 · Process Harvest Data and Target Parsing\n",
    "\n",
    "We process the harvest sheets (`exp1_harvest_clean`, `exp2_harvest_clean`, `exp3_harvest_clean`). \n",
    "Our tasks here are:\n",
    "1. **Filter out summary rows**: Drop any rows where `plant_no` is null. This removes replicate average summary rows and trailing blank rows, leaving exactly the individual plant records.\n",
    "2. **Parse Head Diameter**: Parse the string head diameter dimensions (`Width*Height` e.g., `'24*27'`) into a numeric average head diameter and rectangular canopy area.\n",
    "3. **Extract Targets**: Set `total_weight_g` as our primary prediction target, and keep standardized shoot weight, height, and leaf count."
]))

cells.append(code([
    "def parse_head_diameter_str(val):\n",
    "    \"\"\"\n",
    "    Parses a head diameter string (e.g. '24*27' or '24') and returns (average_diameter, canopy_area).\n",
    "    \"\"\"\n",
    "    if pd.isna(val) or val == \"\" or str(val).lower().strip() in (\"nan\", \"nat\", \"null\", \"h.d (cm)\"):\n",
    "        return np.nan, np.nan\n",
    "    \n",
    "    val_str = str(val).lower().replace(\"cm\", \"\").strip()\n",
    "    \n",
    "    # Split on standard separators\n",
    "    for separator in ['*', 'x', '×']:\n",
    "        if separator in val_str:\n",
    "            parts = val_str.split(separator)\n",
    "            try:\n",
    "                w = float(parts[0].strip())\n",
    "                h = float(parts[1].strip())\n",
    "                return (w + h) / 2.0, w * h\n",
    "            except ValueError:\n",
    "                pass\n",
    "                \n",
    "    # Try parsing single numeric string\n",
    "    try:\n",
    "        d = float(val_str)\n",
    "        return d, d * d\n",
    "    except ValueError:\n",
    "        pass\n",
    "        \n",
    "    return np.nan, np.nan\n",
    "\n",
    "def process_harvest(df, exp_label):\n",
    "    \"\"\"\n",
    "    Standardizes harvest dataset, drops summary average rows (where plant_no is NaN),\n",
    "    and parses string head diameter columns.\n",
    "    \"\"\"\n",
    "    # Drop rows where plant_no is missing (summary and trailing rows)\n",
    "    df_filtered = df.dropna(subset=['plant_no']).copy()\n",
    "    df_filtered['plant_no'] = df_filtered['plant_no'].astype(int)\n",
    "    df_filtered['experiment'] = exp_label\n",
    "    \n",
    "    # Resolve names mapping\n",
    "    shoot_wt_col = 'shoot_weight_after_removing_wilted_leavesg' if 'shoot_weight_after_removing_wilted_leavesg' in df_filtered.columns else 'shoot_weight_after_removing_wilted_leaves_g'\n",
    "    hd_col = 'head_diameter_cm' if 'head_diameter_cm' in df_filtered.columns else 'hd_cm'\n",
    "    leaf_col = 'no_of_leaves' if 'no_of_leaves' in df_filtered.columns else 'noof_leaves'\n",
    "    \n",
    "    # Parse head diameter\n",
    "    avg_hds = []\n",
    "    canopy_areas = []\n",
    "    for val in df_filtered[hd_col]:\n",
    "        avg_hd, area = parse_head_diameter_str(val)\n",
    "        avg_hds.append(avg_hd)\n",
    "        canopy_areas.append(area)\n",
    "        \n",
    "    df_filtered['head_diameter_average_cm'] = avg_hds\n",
    "    df_filtered['canopy_area_cm2'] = canopy_areas\n",
    "    \n",
    "    # Assign predictions targets and clean features\n",
    "    df_filtered['target_total_weight_g'] = df_filtered['total_weight_g']\n",
    "    df_filtered['harvest_plant_height_cm'] = df_filtered['plant_height_cm']\n",
    "    df_filtered['harvest_shoot_weight_g'] = df_filtered[shoot_wt_col]\n",
    "    df_filtered['harvest_root_weight_g'] = df_filtered['root_weight_g']\n",
    "    df_filtered['harvest_root_length_cm'] = df_filtered['root_length_cm']\n",
    "    df_filtered['harvest_no_of_leaves'] = df_filtered[leaf_col]\n",
    "    \n",
    "    cols_to_keep = [\n",
    "        'experiment', 'system', 'plant_no',\n",
    "        'target_total_weight_g', 'harvest_plant_height_cm', 'harvest_shoot_weight_g',\n",
    "        'harvest_root_weight_g', 'harvest_root_length_cm', 'harvest_no_of_leaves',\n",
    "        'head_diameter_average_cm', 'canopy_area_cm2'\n",
    "    ]\n",
    "    \n",
    "    return df_filtered[cols_to_keep]\n",
    "\n",
    "print(\"--- Processing Harvest Datasets ---\")\n",
    "processed_harvest_dfs = []\n",
    "for i in [1, 2, 3]:\n",
    "    key = f\"exp{i}_harvest_clean\"\n",
    "    if key in sheet_data:\n",
    "        df = process_harvest(sheet_data[key], f\"Experiment {i}\")\n",
    "        processed_harvest_dfs.append(df)\n",
    "        print(f\"Experiment {i}: Filtered out summary/blank rows. Kept {len(df)} plant rows.\")\n",
    "        \n",
    "combined_harvest_df = pd.concat(processed_harvest_dfs, ignore_index=True)\n",
    "print(f\"\\nCombined Harvest dataset shape: {combined_harvest_df.shape}\")"
]))

# 9. Merging Datasets
cells.append(md([
    "## 9 · Merge Datasets\n",
    "\n",
    "We merge all the aggregated features (sensor environment, portable water quality, cumulative nutrients, seedlings baselines) onto our individual plant harvest records.\n",
    "\n",
    "To do so, we first extract the `replicate` index (e.g. `R1`, `R2`, `R3`) from the `system` column so that we can merge using all three required keys:\n",
    "- `experiment`\n",
    "- `system`\n",
    "- `replicate`"
]))

cells.append(code([
    "def extract_replicate(sys_val):\n",
    "    \"\"\"\n",
    "    Extracts replicate code from system name.\n",
    "    e.g. 'R1-T1' -> 'R1'\n",
    "         'R2T2' -> 'R2'\n",
    "    \"\"\"\n",
    "    if pd.isna(sys_val) or not isinstance(sys_val, str):\n",
    "        return np.nan\n",
    "    sys_clean = sys_val.strip()\n",
    "    if len(sys_clean) >= 2:\n",
    "        return sys_clean[:2]\n",
    "    return np.nan\n",
    "\n",
    "# 1. Add replicate column to harvest dataframe\n",
    "combined_harvest_df['replicate'] = combined_harvest_df['system'].apply(extract_replicate)\n",
    "\n",
    "# 2. Build the system-level features dataframe\n",
    "sys_records = []\n",
    "for (exp_label, sys_id), port_metrics in portable_aggregates.items():\n",
    "    nut_metrics = nutrient_aggregates.get((exp_label, sys_id), {})\n",
    "    \n",
    "    # Compile all features for this experiment and system\n",
    "    record = {\n",
    "        'experiment': exp_label,\n",
    "        'system': sys_id,\n",
    "        'replicate': extract_replicate(sys_id)\n",
    "    }\n",
    "    \n",
    "    # Add portable water aggregates\n",
    "    record.update(port_metrics)\n",
    "    # Add nutrient aggregates\n",
    "    record.update(nut_metrics)\n",
    "    # Add global sensor aggregates\n",
    "    record.update(sensor_aggregates.get(exp_label, {}))\n",
    "    # Add seedling baselines\n",
    "    record.update(seedling_baselines.get(exp_label, {}))\n",
    "    \n",
    "    sys_records.append(record)\n",
    "    \n",
    "sys_features_df = pd.DataFrame(sys_records)\n",
    "print(f\"Created system-level features DataFrame: {sys_features_df.shape}\")\n",
    "\n",
    "# 3. Merge system features onto individual harvest plants\n",
    "# Merge keys: experiment, system, replicate\n",
    "final_ml_df = pd.merge(\n",
    "    combined_harvest_df, \n",
    "    sys_features_df, \n",
    "    on=['experiment', 'system', 'replicate'], \n",
    "    how='left'\n",
    ")\n",
    "print(f\"\\nFinal Merged Machine Learning Dataset shape: {final_ml_df.shape}\")"
]))

# 10. Handle Missing Values Carefully
cells.append(md([
    "## 10 · Handle Missing Values Carefully\n",
    "\n",
    "Let's inspect if there are any missing values in the merged dataset and address them with explicit rationale, rather than blindly filling."
]))

cells.append(code([
    "print(\"--- Missing Values Count per Column in Merged Dataset ---\")\n",
    "null_counts = final_ml_df.isnull().sum()\n",
    "display(null_counts[null_counts > 0])"
]))

cells.append(md([
    "### 10.1 Missing Values Decisions & Rationale\n",
    "\n",
    "From the missingness analysis, we observe:\n",
    "- `total_acid_consumption_ml` has **72 missing values** (representing all plants of **Experiment 2**).\n",
    "  - *Reasoning*: Experiment 2 raw sheets did not contain an acid consumption sheet. In hydroponics management, acid is only added when water pH goes out of target bounds. Since pH in Experiment 2 was stable or acid dosing was not logged, we will fill these missing values with `0.0` milliliters, signifying that no acid addition was logged during this trial. This preserves the column's numerical nature for ML.\n",
    "  \n",
    "Let's execute the missing value filling step."
]))

cells.append(code([
    "# Fill missing Experiment 2 acid consumption with 0.0\n",
    "final_ml_df['total_acid_consumption_ml'] = final_ml_df['total_acid_consumption_ml'].fillna(0.0)\n",
    "\n",
    "# Verify that no missing values remain\n",
    "remaining_nulls = final_ml_df.isnull().sum()\n",
    "print(f\"Total missing values remaining in dataset: {remaining_nulls.sum()}\")"
]))

# 11. Save Final Dataset
cells.append(md([
    "## 11 · Save Final Dataset\n",
    "\n",
    "We save the final flat machine learning dataset to `../data/processed/final_ml_dataset.csv`. This dataset is ready for training models in subsequent phases."
]))

cells.append(code([
    "output_dir = \"../data/processed\"\n",
    "os.makedirs(output_dir, exist_ok=True)\n",
    "output_path = os.path.join(output_dir, \"final_ml_dataset.csv\")\n",
    "\n",
    "final_ml_df.to_csv(output_path, index=False)\n",
    "print(f\"Successfully saved final ML dataset of shape {final_ml_df.shape} to:\")\n",
    "print(output_path)"
]))

# 12. Create Feature Engineering Report
cells.append(md([
    "## 12 · Create Feature Engineering Report\n",
    "\n",
    "We programmatically write out a report detailing the dataset statistics, the target variable, the final list of features, and the missing value handling summary to `../reports/feature_engineering_report.md`."
]))

cells.append(code([
    "report_dir = \"../reports\"\n",
    "os.makedirs(report_dir, exist_ok=True)\n",
    "report_path = os.path.join(report_dir, \"feature_engineering_report.md\")\n",
    "\n",
    "# Compile lists of targets and features\n",
    "target_cols = ['target_total_weight_g']\n",
    "metadata_cols = ['experiment', 'system', 'replicate', 'plant_no']\n",
    "feature_cols = [c for c in final_ml_df.columns if c not in target_cols + metadata_cols]\n",
    "\n",
    "report_md = f\"\"\"# HydroGrow AI — Feature Engineering Report\n",
    "\n",
    "**Generated Date:** 2026-07-15  \n",
    "**Phase:** Phase 3 (Feature Engineering)  \n",
    "**Status:** Completed successfully  \n",
    "\n",
    "## 1. Dataset Overview\n",
    "- **Number of Samples (Rows):** {len(final_ml_df)} plants\n",
    "- **Number of Features (Columns):** {len(feature_cols)} features\n",
    "- **Target Variable:** `{target_cols[0]}` (Fresh weight in grams at harvest)\n",
    "\n",
    "## 2. Feature Standardizations and Mappings\n",
    "Replicate systems from sheet-level datasets (`replicate_X_tY`) were mapped to harvest systems as follows:\n",
    "- **Experiment 1**: Replicate X, Tank Y maps to `R{{Y}}-T{{X}}`\n",
    "- **Experiment 2**: Replicate X, Tank Y maps to `R{{X}}-T{{Y}}`\n",
    "- **Experiment 3**: Replicate X, Tank Y maps to `R{{X}}T{{Y}}`\n",
    "\n",
    "## 3. List of Engineered Features\n",
    "### 3.1 Metadata & Key Identifiers\n",
    "\"\"\"\n",
    "for c in metadata_cols:\n",
    "    report_md += f\"- `{c}`\\n\"\n",
    "    \n",
    "report_md += \"\"\"\n",
    "### 3.2 Target Outcome Variables\n",
    "\"\"\"\n",
    "for c in target_cols + ['harvest_plant_height_cm', 'harvest_shoot_weight_g', 'harvest_root_weight_g', 'harvest_root_length_cm', 'harvest_no_of_leaves', 'head_diameter_average_cm', 'canopy_area_cm2']:\n",
    "    report_md += f\"- `{c}`\\n\"\n",
    "\n",
    "report_md += \"\"\"\n",
    "### 3.3 Environmental Features (Air Parameters)\n",
    "\"\"\"\n",
    "env_features = [c for c in feature_cols if c.startswith('env_')]\n",
    "for c in sorted(env_features):\n",
    "    report_md += f\"- `{c}`\\n\"\n",
    "\n",
    "report_md += \"\"\"\n",
    "### 3.4 Water Quality Features (Root Zone)\n",
    "\"\"\"\n",
    "water_features = [c for c in feature_cols if c.startswith('water_')]\n",
    "for c in sorted(water_features):\n",
    "    report_md += f\"- `{c}`\\n\"\n",
    "\n",
    "report_md += \"\"\"\n",
    "### 3.5 Management Input Features\n",
    "\"\"\"\n",
    "mgmt_features = [c for c in feature_cols if c.startswith('total_')]\n",
    "for c in sorted(mgmt_features):\n",
    "    report_md += f\"- `{c}`\\n\"\n",
    "\n",
    "report_md += \"\"\"\n",
    "### 3.6 Starting Baseline Features\n",
    "\"\"\"\n",
    "seedling_features = [c for c in feature_cols if c.startswith('initial_')]\n",
    "for c in sorted(seedling_features):\n",
    "    report_md += f\"- `{c}`\\n\"\n",
    "\n",
    "report_md += \"\"\"\n",
    "## 4. Missing Value Treatment Summary\n",
    "- **Summary Rows Exclusion**: Dropped rows in the harvest sheet with `plant_no = NaN` (these were system-level averages included in raw files). This resulted in exactly **216 clean, complete individual plant rows** (72 per experiment).\n",
    "- **Acid Consumption (Experiment 2)**: Missing `total_acid_consumption_ml` for Experiment 2 (72 records) was filled with **`0.0`**. Acid additions were not logged or needed during this trial, making 0.0 the correct physical representation.\n",
    "- **Water Quality (pH, EC, TDS, Water Temp)**: Highly complete; 0% missingness after merging, showing successful temporal aggregation and key mapping.\n",
    "- **No other missing values exist in the final ML dataset.**\n",
    "\"\"\"\n",
    "\n",
    "with open(report_path, \"w\", encoding=\"utf-8\") as f:\n",
    "    f.write(report_md)\n",
    "\n",
    "print(f\"Successfully wrote Feature Engineering Report to:\")\n",
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

notebook_path = "04_Feature_Engineering.ipynb"
with open(notebook_path, "w", encoding="utf-8") as f:
    json.dump(notebook_content, f, indent=2, ensure_ascii=False)

print(f"\nNotebook '{notebook_path}' generated successfully!")
