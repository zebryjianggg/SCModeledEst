
# CHIS and ACS Data Modeling Project

This project involves building models using California Health Interview Survey (CHIS) data and applying these models to American Community Survey (ACS) Public Use Microdata Sample (PUMS) data. The workflow includes data import, merging, manipulation, and analysis using a custom `DataToolBox` class for streamlined data operations.

## Table of Contents
- [Project Overview](#project-overview)
- [Data Sources](#data-sources)
- [Dependencies](#dependencies)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contact](#contact)

## Project Overview
This project aims to:
1. Import and merge ACS PUMS person and housing data.
2. Import CHIS data.
3. Utilize a custom `DataToolBox` class for data manipulation.
4. Build and apply predictive models.

## Data Sources
- **ACS PUMS Data**: 2018-2022 ACS 5-Year Estimates
- **CHIS Data**: 2022 Adult Sample

## Dependencies
- Python 3.x
- pandas
- numpy
- tabulate
- sas7bdat

## Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/chis-acs-modeling.git
   cd chis-acs-modeling
   ```

2. **Install the required packages:**
   ```bash
   pip install pandas numpy tabulate sas7bdat
   ```

3. **Data Preparation:**
   - Place the ACS PUMS and CHIS data files in the `Data` directory following the structure:
     ```
     Data/
     ├── ACS_5YR/
     │   └── 2018_2022/
     │       ├── csv_pca/
     │       │   └── psam_p06.csv
     │       └── csv_hca/
     │           └── psam_h06.csv
     └── CHIS Dummy/
         └── Adult 2022/
             └── dummy_adult.sas7bdat
     ```

## Usage
1. **Run the script:**
   ```bash
   python Step 1_Produce ACS and SAS Data.py
   ```

2. **Script Breakdown:**
   - **Import Data:**
     ```python
     acs_raw_person = pd.read_csv("Data/ACS_5YR/2018_2022/csv_pca/psam_p06.csv")
     acs_raw_housing = pd.read_csv('Data/ACS_5YR/2018_2022/csv_hca/psam_h06.csv')
     acs_raw = pd.merge(acs_raw_person, acs_raw_housing, on='SERIALNO', how='left')
     with SAS7BDAT('Data/CHIS Dummy/Adult 2022/dummy_adult.sas7bdat') as file:
         chis_raw = file.to_data_frame()
     ```

   - **DataToolBox Class:**
     ```python
     class DataToolBox:
         def __init__(self, data):
             self.data = data

         def return_data(self):
             return self.data

         def data_desc(self):
             temp = self.data.shape
             print("---------Current Data State----------")
             print(temp[0], "obs;", temp[1], "vars")
             print("")

         def data_exclude(self, condition: str):
             temp = self.data.query(condition)
             temp_new_obs = temp.shape[0]
             temp_old_obs = self.data.shape[0]
             temp_diff_obs = temp_old_obs - temp_new_obs
             print(f"{temp_diff_obs} observations excluded based on condition: {condition}")
             self.data = self.data.query(f"not ({condition})")
     ```

3. **Example Operations:**
   - Return data:
     ```python
     toolbox = DataToolBox(acs_raw)
     toolbox.return_data()
     ```

   - Print data description:
     ```python
     toolbox.data_desc()
     ```

   - Exclude data based on condition:
     ```python
     toolbox.data_exclude('AGEP < 18')
     ```

## Project Structure
```
.
├── Data/xxx
│   ├── ACS_5YR/
│   │   └── 2018_2022/
│   │       ├── csv_pca/
│   │       └── csv_hca/
│   └── CHIS Dummy/
│       └── Adult 2022/
├── Step 1_Produce ACS and SAS Data.py
└── README.md
```

## Contact
For any questions or feedback, please contact [your email].
