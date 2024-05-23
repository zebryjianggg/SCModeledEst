
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

## Features
- Data loading from CSV files.
- Merging of person and housing datasets.
- Preparation of datasets for analysis.

## Contributing
Contributions to the project are welcome! Please fork the repository and submit a pull request with your additions.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact Information
For further information or support, please contact [your-email@example.com].

## Acknowledgments
- [Contributor 1, if any]
- Any libraries or tools used in the project.
