# DataToolBox Class

The `DataToolBox` class is designed to provide a set of tools and methods for analyzing and manipulating a pandas DataFrame. It allows you to perform various operations on the data, such as filtering, frequency analysis, and constructing new columns based on conditions.


## Initialization

```python
__init__(self, data)

data (pandas.DataFrame): A required parameter that represents the pandas DataFrame to be analyzed and manipulated. This DataFrame is stored as an attribute of the DataToolBox instance.

## Methods

### return_data(self, )

Returns the current state of the data stored in the toolbox.

Returns: The current pandas DataFrame stored within the tool.

### data_desc(self, )

Prints a description of the current dataset, including the number of observations (rows) and variables (columns).

### data_exclude(self, condition)

Excludes observations from the data based on a given condition and updates the dataset.

Parameters:

### freq_1way(self, col_name)

Prints the frequency count and percentage distribution of a single column, sorted by index, and displays it in a formatted table with borders. Rows with a count of zero are not shown.

Parameters:

### freq_2way(self, col_name_1, col_name_2, exclude_equal)

Prints a two-way frequency table (crosstab) between two columns in a formatted table with borders, excluding rows where the count is zero, and optionally excluding rows where values in column A are equal to column B.

Parameters:

### freq_multiway(self, columns, exclude_zeros, exclude_equal)

Prints a multi-way frequency table (crosstab) between given columns in a formatted table with borders, excluding rows where the count is zero, and optionally excluding rows where all values in specified columns are equal.

Parameters:

### data_construct(self, col_name, conditions_str, choices, default)

Constructs a new column in the data based on multiple conditions, where choices can be either fixed values or column references. It stops checking further conditions once a true condition is met for a row.

Parameters:

- default (int or str, optional): The default value or column name to be assigned if none of the conditions are met. Default is -1. Default is -1.


Please note that all input parameters that expect column names should be provided as strings. The data_construct method expects conditions_str to be a list of strings representing the conditions, and choices to be a list of either fixed values or column names (as strings).
