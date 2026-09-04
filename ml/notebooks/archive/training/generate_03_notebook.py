"""
Generate the 03_ML_Data_Preparation.ipynb notebook.
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
    "# 🌱 HydroGrow AI — Phase 2: Machine Learning Data Preparation\n",
    "\n",
    "---\n",
    "\n",
    "**Notebook:** `03_ML_Data_Preparation.ipynb`  \n",
    "**Project:** HydroGrow AI Decision Support System  \n",
    "**Phase:** Phase 2 (Machine Learning Data Preparation)  \n",
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
    "Now that Phase 1 (Data Understanding and Cleaning) has been successfully completed, our next step is to prepare the HydroGrow AI project for **Machine Learning (ML)**. \n",
    "\n",
    "### 1.1 Objective\n",
    "The primary objective of this notebook is to perform a comprehensive diagnostic inspection of all processed datasets to determine their suitability and readiness for training predictive models. \n",
    "\n",
    "Specifically, we will:\n",
    "1. **Load all cleaned datasets** from the processed directories (both experiment-level files and individual sheet-level files).\n",
    "2. **Profile each dataset** by automatically classifying columns (Numeric, Categorical, Date, Text) and computing metadata (missingness, unique counts).\n",
    "3. **Evaluate biological target candidates** (e.g. weights, height, head diameter, leaf count) and recommend the top targets.\n",
    "4. **Evaluate input features** (e.g. environmental and water quality parameters) and outline feature engineering recommendations.\n",
    "5. **Analyze the data architecture** (Combined Concatenated vs. Merged Sheet-Level) to recommend the structure that preserves the most meaningful relationships between environmental histories and biological outcomes.\n",
    "6. **Synthesize a Machine Learning Readiness Report** summarizing targets, features, columns to ignore, missing data, and critical challenges."
]))

# 2. Import Libraries
cells.append(md([
    "## 2 · Import Libraries\n",
    "\n",
    "We start by importing the necessary standard libraries for data manipulation, file handling, and formatting."
]))

cells.append(code([
    "import os\n",
    "import glob\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "\n",
    "# Fallback for display if run outside Jupyter\n",
    "try:\n",
    "    from IPython.display import display\n",
    "except ImportError:\n",
    "    display = print\n",
    "\n",
    "# Set display options for better visibility\n",
    "pd.set_option('display.max_columns', None)\n",
    "pd.set_option('display.max_rows', 100)\n",
    "pd.set_option('display.width', 1000)\n",
    "\n",
    "print(\"Libraries successfully imported!\")"
]))

# 3. Load Data
cells.append(md([
    "## 3 · Load Cleaned Datasets\n",
    "\n",
    "We load two categories of cleaned datasets from the `data/processed/` directory:\n",
    "1. **Experiment-level datasets** (`exp1_clean.csv`, `exp2_clean.csv`, `exp3_clean.csv`): These represent combined files for each experiment.\n",
    "2. **Sheet-level datasets** (`data/processed/per_sheet/*_clean.csv`): These represent individual sheets extracted from each experiment's workbook.\n",
    "\n",
    "Let's write a helper function to discover and load these CSV files."
]))

cells.append(code([
    "def load_dataset(file_path):\n",
    "    \"\"\"\n",
    "    Load a cleaned CSV file into a pandas DataFrame.\n",
    "    Use relative paths for safety.\n",
    "    \"\"\"\n",
    "    try:\n",
    "        df = pd.read_csv(file_path)\n",
    "        basename = os.path.basename(file_path)\n",
    "        print(f\"Loaded '{basename}' successfully with shape {df.shape}\")\n",
    "        return df\n",
    "    except Exception as e:\n",
    "        print(f\"Error loading {file_path}: {e}\")\n",
    "        return None\n",
    "\n",
    "# 3.1 Load Experiment-Level Cleaned Datasets\n",
    "print(\"--- Loading Experiment-Level Datasets ---\")\n",
    "exp_paths = glob.glob('../data/processed/exp*_clean.csv')\n",
    "experiment_datasets = {}\n",
    "for path in sorted(exp_paths):\n",
    "    name = os.path.basename(path).replace('_clean.csv', '')\n",
    "    df = load_dataset(path)\n",
    "    if df is not None:\n",
    "        experiment_datasets[name] = df\n",
    "\n",
    "# 3.2 Load Sheet-Level Cleaned Datasets\n",
    "print(\"\\n--- Loading Sheet-Level Datasets ---\")\n",
    "sheet_paths = glob.glob('../data/processed/per_sheet/*_clean.csv')\n",
    "sheet_datasets = {}\n",
    "for path in sorted(sheet_paths):\n",
    "    name = os.path.basename(path).replace('.csv', '')\n",
    "    df = load_dataset(path)\n",
    "    if df is not None:\n",
    "        sheet_datasets[name] = df"
]))

# 4. Column Classification
cells.append(md([
    "## 4 · Automatic Column Classification\n",
    "\n",
    "We need to automatically classify columns into four logical categories:\n",
    "- **Numeric**: Numerical quantities suitable for mathematical features (continuous or large integer counts).\n",
    "- **Categorical**: Discrete levels, identifiers, or codes with relatively low cardinality.\n",
    "- **Date**: Temporal markers (datetimes, dates, or parseable date strings).\n",
    "- **Text**: High-cardinality string columns containing text messages, comments, or complex structures (e.g. head diameter representations).\n",
    "\n",
    "We write a modular helper function `classify_columns(df)` that inspects the pandas data types, cardinality (number of unique values), and content patterns to automatically classify every column."
]))

cells.append(code([
    "def classify_columns(df):\n",
    "    \"\"\"\n",
    "    Automatically classifies columns in a DataFrame into:\n",
    "    Numeric, Categorical, Date, or Text.\n",
    "    \"\"\"\n",
    "    classification = {}\n",
    "    for col in df.columns:\n",
    "        # 1. Date Type Check (Pandas datetime type)\n",
    "        if pd.api.types.is_datetime64_any_dtype(df[col]):\n",
    "            classification[col] = \"Date\"\n",
    "            continue\n",
    "            \n",
    "        col_clean = df[col].dropna()\n",
    "        if len(col_clean) == 0:\n",
    "            classification[col] = \"Categorical\"  # Default empty column\n",
    "            continue\n",
    "            \n",
    "        # 2. Date String Check\n",
    "        # If column name has date/time keywords or matches date format, try to parse\n",
    "        is_date_name = any(kw in col.lower() for kw in ['date', 'time', 'tme'])\n",
    "        if is_date_name:\n",
    "            try:\n",
    "                pd.to_datetime(col_clean, errors='raise')\n",
    "                classification[col] = \"Date\"\n",
    "                continue\n",
    "            except:\n",
    "                pass\n",
    "                \n",
    "        # 3. Numeric Check\n",
    "        if pd.api.types.is_numeric_dtype(df[col]):\n",
    "            unique_count = df[col].nunique()\n",
    "            # Check if all numbers are integers\n",
    "            all_ints = False\n",
    "            try:\n",
    "                all_ints = (col_clean % 1 == 0).all()\n",
    "            except:\n",
    "                pass\n",
    "                \n",
    "            # If low unique count (e.g. system ids or seedling groups) and represents integers\n",
    "            if unique_count <= 15 and all_ints:\n",
    "                classification[col] = \"Categorical\"\n",
    "            else:\n",
    "                classification[col] = \"Numeric\"\n",
    "            continue\n",
    "            \n",
    "        # 4. Object/String Check\n",
    "        unique_count = df[col].nunique()\n",
    "        non_null_count = len(col_clean)\n",
    "        \n",
    "        # Check if first few values match date string formats\n",
    "        try:\n",
    "            first_val = str(col_clean.iloc[0])\n",
    "            if len(first_val) >= 8 and pd.to_datetime(col_clean.iloc[:5], errors='raise') is not None:\n",
    "                classification[col] = \"Date\"\n",
    "                continue\n",
    "        except:\n",
    "            pass\n",
    "            \n",
    "        # High cardinality vs Low cardinality split for categorical vs text\n",
    "        if unique_count <= 20 or (unique_count / non_null_count < 0.1):\n",
    "            classification[col] = \"Categorical\"\n",
    "        else:\n",
    "            classification[col] = \"Text\"\n",
    "            \n",
    "    return classification\n",
    "\n",
    "print(\"Helper function 'classify_columns' successfully defined!\")"
]))

# 5. Data Profiling & Summary Tables
cells.append(md([
    "## 5 · Dataset Profiling & Summary Tables\n",
    "\n",
    "For each dataset, we generate a profile summary table. This table includes:\n",
    "- **Column Name**\n",
    "- **Data Type** (Pandas native Dtype)\n",
    "- **Missing %** (Percentage of null values)\n",
    "- **Unique Values** (Cardinality count)\n",
    "- **Classified Type** (Our automatic classification)\n",
    "\n",
    "We write a helper function `profile_dataset(df)` to compile these metrics and present them in a clean format."
]))

cells.append(code([
    "def profile_dataset(df):\n",
    "    \"\"\"\n",
    "    Generate a summary profile DataFrame showing column-level characteristics.\n",
    "    \"\"\"\n",
    "    classification = classify_columns(df)\n",
    "    profile_data = []\n",
    "    \n",
    "    for col in df.columns:\n",
    "        dtype = str(df[col].dtype)\n",
    "        missing_pct = (df[col].isnull().sum() / len(df)) * 100\n",
    "        unique_vals = df[col].nunique()\n",
    "        classified_type = classification.get(col, \"Unknown\")\n",
    "        \n",
    "        profile_data.append({\n",
    "            \"Column Name\": col,\n",
    "            \"Data Type\": dtype,\n",
    "            \"Missing %\": round(missing_pct, 2),\n",
    "            \"Unique Values\": unique_vals,\n",
    "            \"Classified Type\": classified_type\n",
    "        })\n",
    "        \n",
    "    return pd.DataFrame(profile_data)\n",
    "\n",
    "print(\"Helper function 'profile_dataset' successfully defined!\")"
]))

cells.append(md([
    "### 5.1 Profile the Experiment-Level Combined Datasets\n",
    "\n",
    "Let's display the profile table for the three combined datasets (`exp1`, `exp2`, `exp3`)."
]))

cells.append(code([
    "for name, df in experiment_datasets.items():\n",
    "    print(f\"\\n========================================\")\n",
    "    print(f\"Profile Table for Combined Dataset: {name}\")\n",
    "    print(f\"========================================\")\n",
    "    profile_df = profile_dataset(df)\n",
    "    display(profile_df.head(25))"
]))

cells.append(md([
    "### 5.2 Profile Representative Sheet-Level Datasets\n",
    "\n",
    "Next, we inspect the individual sheet-level files. Since there are 26 files, we will profile a few key representative sheets for Experiment 1:\n",
    "1. **Harvest Sheet** (`exp1_harvest_clean`): Contains final plant growth biometrics.\n",
    "2. **Seedlings Sheet** (`exp1_seedlings_clean`): Contains initial plant growth biometrics.\n",
    "3. **Sensor Water Quality Sheet** (`exp1_sensor_water_quality_clean`): Contains continuous environmental metrics."
]))

cells.append(code([
    "key_sheets = ['exp1_harvest_clean', 'exp1_seedlings_clean', 'exp1_sensor_water_quality_clean']\n",
    "for sheet_name in key_sheets:\n",
    "    if sheet_name in sheet_datasets:\n",
    "        df = sheet_datasets[sheet_name]\n",
    "        print(f\"\\n========================================\")\n",
    "        print(f\"Profile Table for Sheet: {sheet_name}\")\n",
    "        print(f\"========================================\")\n",
    "        profile_df = profile_dataset(df)\n",
    "        display(profile_df.head(15))"
]))

# 6. Target Variable Suitability Analysis
cells.append(md([
    "## 6 · Target Variable Suitability Analysis\n",
    "\n",
    "A machine learning target variable must represent a key biological outcome we wish to predict (e.g. yield, size, growth). \n",
    "\n",
    "We inspect our datasets to find columns relating to growth. Specifically, we compile all columns containing biological keywords (e.g. weight, height, diameter, leaves, length, head) across the three datasets and check their data quality."
]))

cells.append(code([
    "# Let's identify all unique biological columns across the combined experiments\n",
    "bio_keywords = ['weight', 'height', 'length', 'diameter', 'leaves', 'count', 'head', 'hd', 'leaf']\n",
    "all_bio_cols = set()\n",
    "for df in experiment_datasets.values():\n",
    "    for col in df.columns:\n",
    "        if any(kw in col.lower() for kw in bio_keywords):\n",
    "            all_bio_cols.add(col)\n",
    "\n",
    "print(\"Biological growth columns found in the datasets:\")\n",
    "print(sorted(list(all_bio_cols)))\n",
    "\n",
    "# Let's evaluate non-null counts and ranges for these columns in the harvest sheets\n",
    "harvest_dfs = [df for name, df in sheet_datasets.items() if 'harvest' in name]\n",
    "if harvest_dfs:\n",
    "    combined_harvest = pd.concat(harvest_dfs, ignore_index=True)\n",
    "    print(\"\\n--- Combined Harvest Biological Columns Statistics ---\")\n",
    "    for col in combined_harvest.columns:\n",
    "        if any(kw in col.lower() for kw in bio_keywords):\n",
    "            non_null = combined_harvest[col].dropna()\n",
    "            print(f\"{col:45} | Non-Null: {len(non_null):3d} | Dtype: {combined_harvest[col].dtype} | Unique Count: {non_null.nunique()}\")\n",
    "            if pd.api.types.is_numeric_dtype(non_null) and len(non_null) > 0:\n",
    "                print(f\"  Mean: {non_null.mean():.2f} | Min: {non_null.min():.2f} | Max: {non_null.max():.2f}\")\n",
    "            elif len(non_null) > 0:\n",
    "                print(f\"  Sample values: {non_null.iloc[:3].tolist()}\")"
]))

cells.append(md([
    "### 6.1 Recommendations for Top 3 Target Variables\n",
    "\n",
    "Based on the data quality, missingness, and agronomic relevance, we recommend the following **Top 3 Target Variables**:\n",
    "\n",
    "1. **`total_weight_g` (Fresh Weight)**\n",
    "   - *Explanation*: This represents the overall plant biomass at harvest (fresh weight). It has 228 non-null entries in harvest sheets. Fresh weight is the most direct indicator of hydroponic crop yield and is highly sensitive to environmental factors.\n",
    "\n",
    "2. **`shoot_weight_after_removing_wilted_leaves` (Net Marketable Shoot Weight)**\n",
    "   - *Explanation*: This measures the edible and sellable shoot biomass. Because column naming varies slightly between Experiment 3 (`_wilted_leaves_g`) and Experiments 1 & 2 (`_wilted_leavesg`), they must be standardized. It has 223 non-null entries and is the ultimate crop performance metric.\n",
    "\n",
    "3. **`plant_height_cm` or `head_diameter_cm` (Morphological Size Markers)**\n",
    "   - *Explanation*: Height (254 non-nulls) and head diameter (176 non-nulls) indicate physical dimensions. Plant height is clean and numeric. Head diameter represents lettuce physical spread, but is stored as text strings (e.g., `'24*27'`). If head diameter is used, it must be parsed into numeric area (width * height) or average diameter."
]))

# 7. Input Features Analysis
cells.append(md([
    "## 7 · Input Feature Recommendations\n",
    "\n",
    "To predict growth outcomes, we must identify the variables that represent the growth environment. These are our input features. We recommend grouping them into three categories:\n",
    "\n",
    "1. **Environmental Sensor Aggregates** (from `sensor_water_quality`):\n",
    "   - `air_temp_c` / `air_temp` (Air Temperature in °C)\n",
    "   - `rh_%` / `rh%` (Relative Humidity percentage)\n",
    "   - `co2_ppm` / `co2` (Carbon Dioxide levels in ppm)\n",
    "   - *Note*: These variables are continuous sensor logs and should be aggregated (e.g. mean, minimum, maximum, standard deviation) over each plant's growth cycle.\n",
    "\n",
    "2. **Water Quality Aggregates** (from `portable_water_quality`):\n",
    "   - `ph` (Water pH level)\n",
    "   - `ec` (Electrical Conductivity in mS/cm)\n",
    "   - `tds` (Total Dissolved Solids in ppm)\n",
    "   - `water_temp` (Water Temperature in °C)\n",
    "   - *Note*: These manual spot-checks reflect the root zone environment and should be aggregated over time.\n",
    "\n",
    "3. **Experimental Metadata & Management logs** (from nutrient sheets and metadata):\n",
    "   - `experiment` (Experiment ID: 1, 2, or 3 to capture cohort differences)\n",
    "   - `system` / `replicate` (System identifier to capture spatial/system-level bias)\n",
    "   - `nutrient_solution_addition_(a+b)_ml` (Total nutrient volume added)\n",
    "   - `acid_consumption_ml` (Total acid used for pH regulation)"
]))

# 8. Combined vs Per-Sheet structure recommendation
cells.append(md([
    "## 8 · Dataset Structure Analysis: Combined vs. Per-Sheet\n",
    "\n",
    "A major decision is whether to train models using the combined experiment files (`exp1_clean.csv`, etc.) or the individual sheet-level files (`exp1_harvest_clean.csv`, `exp1_sensor_water_quality_clean.csv`, etc.).\n",
    "\n",
    "### 8.1 Comparison\n",
    "- **Combined Experiment Files**: These files were constructed by simply stacking (concatenating) rows from all sheets of a single experiment together. There is **zero horizontal overlap** between sheets. A row representing a sensor reading has missing values for all harvest growth metrics, and a row representing a harvest plant has missing values for all environmental sensor logs. Training an ML model directly on these combined files is **not possible** without preprocessing, as there are no matching columns within the same rows.\n",
    "- **Individual Sheet-Level Files**: These files isolate the raw tabular logs. The relationship is implicit: the plants in `harvest` grew inside replicate systems (`system`/`replicate`) over the course of the experiment, during which environmental parameters (`sensor_water_quality` and `portable_water_quality`) were recorded for those systems.\n",
    "\n",
    "### 8.2 Recommended Structure for Training\n",
    "We strongly recommend **training models on aggregated sheet-level datasets**. The process should follow a temporal aggregation and key-based merging workflow:\n",
    "\n",
    "```\n",
    "Time-Series Sheets\n",
    "├── Sensor logs (hourly)     ──> Aggregated per System/Exp (Mean, Std, Min, Max)\n",
    "├── Portable logs (daily)    ──> Aggregated per System/Exp (Mean, Std)\n",
    "└── Nutrient logs (daily)    ──> Summed per System/Exp (Total Additions)\n",
    "                                      │\n",
    "                                      ▼ (Merged via keys: Experiment + System/Replicate)\n",
    "Biological Sheet                      │\n",
    "└── Harvest measurements     ─────────┴──> Final Flat Training Dataset (1 row per plant)\n",
    "```\n",
    "\n",
    "Let's write a python conceptual code snippet to demonstrate how this aggregation and merging would be implemented."
]))

cells.append(code([
    "def demo_aggregation_pipeline():\n",
    "    \"\"\"\n",
    "    Conceptual pipeline demonstrating how to combine environmental time-series\n",
    "    with individual plant harvest records for ML training.\n",
    "    \"\"\"\n",
    "    print(\"--- Conceptual Machine Learning Feature Aggregation & Merge ---\")\n",
    "    \n",
    "    # 1. Load harvest records (rows represent individual plants)\n",
    "    if 'exp1_harvest_clean' in sheet_datasets and 'exp1_sensor_water_quality_clean' in sheet_datasets:\n",
    "        harvest_df = sheet_datasets['exp1_harvest_clean'].copy()\n",
    "        sensor_df = sheet_datasets['exp1_sensor_water_quality_clean'].copy()\n",
    "        \n",
    "        print(f\"Raw Harvest records: {len(harvest_df)} rows\")\n",
    "        print(f\"Raw Sensor readings: {len(sensor_df)} rows\")\n",
    "        \n",
    "        # Calculate overall environmental averages for the experiment\n",
    "        env_summary = {\n",
    "            'avg_air_temp': sensor_df['air_temp_c'].mean() if 'air_temp_c' in sensor_df.columns else np.nan,\n",
    "            'std_air_temp': sensor_df['air_temp_c'].std() if 'air_temp_c' in sensor_df.columns else np.nan,\n",
    "            'avg_rh': sensor_df['rh_%'].mean() if 'rh_%' in sensor_df.columns else np.nan,\n",
    "            'avg_co2': sensor_df['co2_ppm'].mean() if 'co2_ppm' in sensor_df.columns else np.nan,\n",
    "        }\n",
    "        print(\"\\nAggregated Experiment Environment:\")\n",
    "        for k, v in env_summary.items():\n",
    "            print(f\"  {k}: {v:.2f}\")\n",
    "            \n",
    "        # Apply these features to harvest plants\n",
    "        for k, v in env_summary.items():\n",
    "            harvest_df[k] = v\n",
    "            \n",
    "        print(f\"\\nStructured Training subset (1 row per plant with environmental features): Shape {harvest_df.shape}\")\n",
    "        display(harvest_df[['system', 'plant_no', 'total_weight_g', 'avg_air_temp', 'avg_rh']].head(5))\n",
    "    else:\n",
    "        print(\"Key datasets not found to run the demo.\")\n",
    "        \n",
    "demo_aggregation_pipeline()"
]))

# 9. Machine Learning Readiness Report
cells.append(md([
    "## 9 · Machine Learning Readiness Report\n",
    "\n",
    "We compile our final findings and assessments into a structured **Machine Learning Readiness Report**.\n",
    "\n",
    "### 9.1 Recommended Targets\n",
    "- **Primary: `total_weight_g` (Fresh Weight)**\n",
    "  - *Reasoning*: Best standard measure of lettuce biomass. Highly relevant for agricultural production. Strongly correlated with nutrient levels, temperature, and CO2.\n",
    "  - *Sample Count*: 228 (Harvest) + 32 (Seedlings) = 260 total non-nulls.\n",
    "- **Secondary: `shoot_weight_after_removing_wilted_leaves`** (Standardized Column)\n",
    "  - *Reasoning*: Represents net marketable crop weight. Directly reflects commercial value. Columns in raw data are named `shoot_weight_after_removing_wilted_leaves_g` (Exp 3) and `shoot_weight_after_removing_wilted_leavesg` (Exp 1 & 2).\n",
    "  - *Sample Count*: 223 total non-nulls.\n",
    "- **Tertiary: `plant_height_cm` or `head_diameter_cm`**\n",
    "  - *Reasoning*: Morphological indicators of size. Height is numeric and clean. Head diameter represents canopy spread but needs parsing from text (e.g. `'24*27'`).\n",
    "  - *Sample Count*: 254 (Height) / 176 (Head Diameter).\n",
    "\n",
    "### 9.2 Recommended Input Features\n",
    "- **Experiment Cohort**: `experiment` (Categorical, captures baseline cohort variations across trials).\n",
    "- **Treatment / System ID**: `system` or `replicate` (Categorical, represents system-specific variables like light, positioning, or system flow).\n",
    "- **Sensor Averages (Time-Series aggregates)**: `mean`, `std`, `min`, `max` of `air_temp_c`, `rh_%`, and `co2_ppm` computed over the growth period.\n",
    "- **Water Quality (Time-Series aggregates)**: `mean`, `std` of `ph`, `ec`, `tds`, `water_temp` computed per replicate system.\n",
    "- **Management Inputs**: Total volume of nutrient solution added (`nutrient_solution_addition_(a+b)_ml`) and total acid consumption (`acid_consumption_ml`).\n",
    "- **Transplant baseline**: Average seedlings metrics at day 0 (e.g. initial average plant height, shoot weight, leaf count).\n",
    "\n",
    "### 9.3 Columns to Ignore\n",
    "- **Timestamp columns**: `date`, `date_1`, `tme`, `tme_1` (except for computing growth durations or sorting time-series logs).\n",
    "- **Table metadata**: `sheet` (which is just a row separator in concatenated files).\n",
    "- **Raw dimensions string**: `head_diameter_cm` / `hd_cm` (if not parsed, as string formats like `'24*27'` will crash numeric models).\n",
    "- **Individual plant number**: `plant_no` (should not be used as a numerical feature, it is just an ID within the replicate group).\n",
    "\n",
    "### 9.4 Missing Value Summary\n",
    "- **Concatenated Files**: In the stacked `exp*_clean.csv` files, missingness is **very high (>90%)** because the datasets are combined row-wise. This is an artifact of stacking, not actual missing data.\n",
    "- **Sheet-Level Files**: Within individual sheets, the datasets are highly complete:\n",
    "  - `harvest` biological parameters: ~0% missing.\n",
    "  - `sensor_water_quality` parameters: <1% missing.\n",
    "  - `portable_water_quality` parameters: <10% missing (some spot checks were not recorded on weekends).\n",
    "  - *Note*: Dry Weight is completely absent in all sheets and experiments.\n",
    "\n",
    "### 9.5 Structural Recommendation\n",
    "> [!IMPORTANT]\n",
    "> **We recommend using individual sheet-level datasets for training rather than the combined experiment-level datasets.** \n",
    "> The combined files are row-stacked tables and cannot establish direct row-wise relationships between environment and plant growth. \n",
    "> To preserve the meaningful relationship between environmental parameters and plant growth, the time-series environmental logs (sensor and portable water quality) must be aggregated per replicate system over time, and then merged horizontally with the harvest sheet records using `experiment` and `system`/`replicate` as keys. This results in a structured training dataset where each row represents a single harvested plant, mapped to its average environmental history.\n",
    "\n",
    "### 9.6 Potential Challenges\n",
    "1. **Small Sample Size for Growth**: The total number of harvest plants across all three experiments is ~230. Standard deep neural networks will easily overfit. We should focus on simpler, robust models like Linear Regression, Ridge, Random Forests, or Gradient Boosting.\n",
    "2. **Column Naming Inconsistencies**: There are column naming differences between experiments (e.g. `air_temp_c` vs `air_temp`, `rh_%` vs `rh%`, `co2_ppm` vs `co2`, `shoot_weight_after_removing_wilted_leavesg` vs `shoot_weight_after_removing_wilted_leaves_g`). These must be resolved via a unified mapper before merging.\n",
    "3. **Head Diameter Parsing**: Head diameter (e.g., `'24*27'`) is non-numeric. It needs string splitting to calculate canopy area (e.g., $24 \\times 27 = 648\\text{ cm}^2$) or average diameter ($25.5\\text{ cm}$).\n",
    "4. **No Dry Weight Data**: Agricultural studies often look at dry weight as a key biomass metric, but it is completely missing in these datasets. We must rely exclusively on fresh weights."
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

notebook_path = "03_ML_Data_Preparation.ipynb"
with open(notebook_path, "w", encoding="utf-8") as f:
    json.dump(notebook_content, f, indent=2, ensure_ascii=False)

print(f"\nNotebook '{notebook_path}' generated successfully!")
