# ETL Pipeline: Istanbul Housing and Earthquake Data

This README documents **my contribution to our university group project: the ETL pipeline**. It explains how I collected the raw data, cleaned and transformed it, connected the datasets geographically, and exported CSV files for the rest of the group.

**ETL** stands for **Extract, Transform, Load**. My role was to prepare the data, **not** to perform the group's statistical analysis.

## 1. Input datasets

I worked with three input files:

| Input file | What it contains | Size |
| --- | --- | ---: |
| `data/istanbul_apartment_prices_2026.csv` | Apartment asking prices, district, neighborhood, area, rooms, building information | 24,767 listings, 30 columns |
| `data/koeri_earthquakes_filtered_2026-11-02.csv` | Historical earthquake times, coordinates, magnitudes, depths and regions in the Istanbul/Marmara study area | 2,936 events, 13 columns |
| `data/turkey_district_coordinates.json` | Reference latitude and longitude for Turkish districts; I extracted Istanbul's districts | 39 Istanbul districts |

The coordinate reference came from [turkey-cities-districts-json](https://github.com/BuNickTamYirmiHarfli/turkey-cities-districts-json). The housing data includes listings from **38 districts**, with no listings for **Şile**. The earthquake records cover **2020–2025**; housing listings are from **2026**.

## 2. Code structure

```text
real-estate-project/
├── data/                         # Original input files
├── ETL/
│   ├── extract.py                # Read input CSV and JSON files
│   ├── transform.py              # Clean data and create geographic features
│   ├── load.py                   # Export processed CSV files
│   └── data exploration.py       # Earlier checks and investigations
├── main.py                       # Runs ETL in order
├── requirements.txt             # Python dependencies
└── output/                       # Generated CSV files
    ├── clean_housing.csv
    ├── clean_earthquakes.csv
    ├── district_earthquake_statistics.csv
    └── final_analysis.csv
```

`main.py` calls the functions in this sequence:

```text
Extract raw data
      ↓
Clean housing and earthquake records
      ↓
Attach district reference coordinates
      ↓
Calculate nearby earthquake statistics by district
      ↓
Merge those statistics with housing listings
      ↓
Validate and export CSVs
```

## 3. Extract: `ETL/extract.py`

I used `pd.read_csv()` to load the two CSV files into Pandas DataFrames and Python's `json` module to read the district coordinate reference. The `extract_data()` function returns **three DataFrames** to `main.py`.

This stage only **reads** the raw files. It does not modify them.

## 4. Transform: `ETL/transform.py`

### A. Housing cleaning

1. Selected **12 useful original columns**, including `listing_id`, `price`, `district`, `neighborhood`, `rooms`, `gross_sqm`, `net_sqm`, `building_age`, `floor`, `total_floors`, `bathroom_count`, and `price_per_sqm`.
2. Checked missing values, duplicate rows, duplicate listing IDs, and data types.
3. Filled missing values using each column's **median**:
   - `floor`: 1,917 missing values
   - `total_floors`: 1 missing value
   - `bathroom_count`: 235 missing values
4. **Flagged** prices below **500,000 TRY** or above **100,000,000 TRY** as `suspicious_price`. **138 listings** were flagged. I did **not** remove them or assume they were definitely wrong.
5. Checked that apartment area was positive and verified the recorded price per square meter using:

   `price_per_sqm ≈ price / net_sqm`

   All **24,767 listings** agreed within **1 TRY/m²**. The checking columns include `valid_area`, `calculated_price_per_sqm`, `price_difference`, and `valid_price_per_sqm`.

**Why these choices?** Median filling preserves rows but produces estimated values. Flagging unusual prices preserves information and allows the analysis team to decide how to treat outliers. The price-per-square-meter check verifies arithmetic consistency, **not** whether each asking price is truthful.

### B. Earthquake cleaning

1. Selected eight original columns: `EventID`, `OriginTime`, `Latitude`, `Longitude`, `Depth_km`, `Magnitude`, `MagnitudeType`, and `Region`.
2. Converted `OriginTime` from text to a proper datetime and added `year` and `month` columns.
3. Verified that all **2,936 events** lie inside our chosen study-area bounding box: latitude **40.5–41.6** and longitude **27.7–30.3**.
4. Flagged **260 events** with depth less than or equal to zero using `invalid_depth`. I replaced their `Depth_km` values with missing (`NaN`) for depth calculations, but **kept the earthquake events**.

The source's original depth values remain in the raw CSV. Treating nonpositive depths as unknown is an **analysis decision**, not proof of measurement error.

### C. Geographic transformation

The two main datasets did **not** share a direct join key:

- Housing records identify a **district**.
- Earthquake records provide **latitude and longitude**.

To connect them, I:

1. Used the third reference dataset to get a latitude and longitude for each Istanbul district.
2. Checked district names: **all 38 housing districts matched** the coordinate reference (which also contains Şile).
3. Used a **left merge on `district`** to attach reference coordinates to every apartment without losing any housing rows.
4. Wrote a `calculate_distance()` function using the **Haversine formula** and an approximate Earth radius of **6,371 km**.
5. For each district, looped through the earthquake records and calculated statistics for events within **20 km of the district reference point**.

This created four features for each district:

| Feature | Meaning |
| --- | --- |
| `earthquake_count_20km` | Number of recorded earthquake epicenters within 20 km |
| `average_magnitude_20km` | Average recorded magnitude of those events |
| `max_magnitude_20km` | Maximum recorded magnitude of those events |
| `average_depth_20km` | Average available positive recorded depth of those events |

6. Used another **left merge on `district`** to attach these four district-level features to every housing listing.

**Important:** The coordinates are **district reference points, not exact apartment locations**. The 20 km radius is an exploratory choice, not an official boundary or hazard threshold. The same earthquake may be counted for more than one district.

## 5. Validate: `main.py`

I checked that:

- The final merge retained **24,767 apartment records**.
- The saved final CSV has **24,767 unique `listing_id` values**.
- The housing data covers **38 districts**.
- All apartment rows have district coordinates and a nonmissing nearby earthquake count.
- The exported CSV can be read again successfully.

**Final combined dataset:** **24,767 rows × 23 columns**.

## 6. Load: `ETL/load.py`

I used `DataFrame.to_csv(index=False)` to write four files to the `output/` folder:

| Output file | Rows | Intended use |
| --- | ---: | --- |
| `clean_housing.csv` | 24,767 | Housing data after the selected cleaning steps |
| `clean_earthquakes.csv` | 2,936 | Event-level earthquake records with cleaned dates and flagged depths |
| `district_earthquake_statistics.csv` | 38 | One row per housing district, with four nearby-earthquake indicators |
| **`final_analysis.csv`** | **24,767** | **Main combined file for the group**, with apartment features and district earthquake indicators |

The original input files in `data/` are not overwritten.

## 7. How to run my ETL pipeline

From the repository root (the folder containing `main.py`), with **Python 3.11** installed:

```powershell
py -3.11 -m pip install -r requirements.txt
py -3.11 main.py
```

`requirements.txt` needs `pandas`. The Python modules `math`, `json`, and `os` are built in.

The successful run reports:

```text
EXTRACT COMPLETED
Housing records: 24767
Earthquake records: 2936

TRANSFORM COMPLETED
Cleaned housing records: 24767
Cleaned earthquake records: 2936
Districts analyzed: 38
Final dataset shape: (24767, 23)

VALIDATION COMPLETED
All four datasets saved successfully!
```

## 8. Important notes for teammates

- **Use `output/final_analysis.csv`** for analyses that need both housing and earthquake variables. Use the other outputs for housing-only, earthquake-only, or district-only work.
- **138 suspicious asking prices are still included**, with a flag. Consider whether results change when they are excluded.
- **260 earthquake depths were made missing**; don't assume all depth values are available.
- The earthquake indicators are identical for all listings in the same district. There are **only 38 distinct district-level earthquake summaries**, not 24,767 independent earthquake measurements. Statistical models should account for district-level grouping.
- The earthquake indicators measure **recorded historical activity**, **not official seismic hazard**, predicted earthquake damage, or building safety. They must not be used to label districts objectively "high risk" or "low risk".
- The data cannot establish that earthquake activity **causes** differences in housing prices, and the housing and earthquake datasets cover different time periods.
- `price_per_sqm` is calculated from `price` and `net_sqm`; it is not an independent measurement.

**My contribution ends with the prepared data and the reproducible ETL code.** The remaining statistical modeling, tests, charts, and interpretation are separate parts of the group project.
