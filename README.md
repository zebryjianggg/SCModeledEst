
# ACS and SAS Data Processor

## Description
This project provides a robust toolset for processing American Community Survey (ACS) and SAS datasets. The primary goal is to facilitate easy manipulation and merging of large-scale demographic and housing datasets for analytical purposes.

## Environment Set-up
The project is implemented in Python and requires several libraries. Ensure you have the following installed:

- pandas
- pyreadstat
- sas7bdat
- numpy
- tabulate

You can install these packages using the following command:
```bash
pip install pandas pyreadstat sas7bdat numpy tabulate
```

## Usage
To use this program, ensure you have the ACS and SAS dataset files in the expected directories. Example usage:

1. Load individual ACS person and housing data.
2. Merge these datasets based on a common identifier.
3. Perform your analysis as needed.

Here's a quick start on how to load and merge datasets:
```python
import pandas as pd

# Load datasets
acs_person = pd.read_csv("path_to_person_data.csv")
acs_housing = pd.read_csv("path_to_housing_data.csv")

# Merge datasets
combined_data = pd.merge(acs_person, acs_housing, on='SERIALNO', how='left')
```

## DataToolBox Class
This class provides tools for data manipulation and analysis. Here is a brief overview of its methods:

```python
class DataToolBox:
    def __init__(self, data):
        self.data = data

    def return_data(self):
        return self.data

    def data_desc(self):
        temp = self.data.shape
        print(f"{temp[0]} observations; {temp[1]} variables")

    def data_exclude(self, condition):
        temp = self.data.query(condition)
        self.data = temp
        print(f"Data filtered with condition: {condition}")

    def freq_1way(self, col_name):
        counts = self.data[col_name].value_counts()
        print(counts)
```

### Example usage of DataToolBox:

```python
# Assuming 'combined_data' is a pandas DataFrame
toolbox = DataToolBox(combined_data)

# Get data description
toolbox.data_desc()

# Exclude some data based on a condition
toolbox.data_exclude("age > 50")

# Print frequency of a column
toolbox.freq_1way('age')
```

## Features
- Data loading from CSV files.
- Merging of person and housing datasets.
- Preparation of datasets for analysis using the DataToolBox class.

## Contributing
Contributions to the project are welcome! Please fork the repository and submit a pull request with your additions.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact Information
For further information or support, please contact [your-email@example.com].

## Acknowledgments
- [Contributor 1, if any]
- Any libraries or tools used in the project.
