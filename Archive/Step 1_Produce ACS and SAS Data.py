#!/usr/bin/env python
# coding: utf-8

# Environment Set-up

# In[1]:


import pandas as pd
# import pyreadstat
from sas7bdat import SAS7BDAT
import numpy as np
from tabulate import tabulate
import os
import datetime
import random
# from typing import List, Union, Optional


# Importing Data

# In[2]:

acs_raw_person  = pd.read_csv("Data/ACS_5YR/2018_2022/csv_pca/psam_p06.csv")
acs_raw_housing = pd.read_csv('Data/ACS_5YR/2018_2022/csv_hca/psam_h06.csv')


# In[3]:


acs_raw = pd.merge(acs_raw_person, acs_raw_housing, on='SERIALNO', how='left')


# In[4]:


with SAS7BDAT('Data/CHIS Dummy/Adult 2022/dummy_adult.sas7bdat') as file:
    chis_raw = file.to_data_frame()


# Data Manipulation Toolbox - DataToolBox

# In[5]:


class DataToolBox:
    def __init__(self, data):
        """
        Initialize the DataToolBox with a dataset.

        :param data: A pandas DataFrame that contains the data to be analyzed and manipulated.
        """
        self.data = data

    def return_data(self):
        """
        Return the current state of the data stored in the toolbox.

        :return: The current pandas DataFrame stored within the tool.
        """
        return self.data

    def data_desc(self):
        """
        Print a description of the current dataset including the number of observations (rows) and variables (columns).
        """
        temp = self.data.shape
        print("---------Current Data State----------")
        print(temp[0], "obs;", temp[1], "vars")
        print("")

    def data_exclude(self, condition: str):
        """
        Exclude observations from the data based on a given condition and updates the dataset.

        :param condition: A string representing the condition to be used for filtering the data.
                          Observations meeting this condition will be excluded.
        """
        temp = self.data.query(condition)
        temp_new_obs = temp.shape[0]
        temp_old_obs = self.data.shape[0]
        temp_diff_obs = temp_old_obs - temp_new_obs

        print("---------Obs Filter-----------------")
        print("applying condition: ", condition)
        print(temp_diff_obs, "/", temp_old_obs, "cases were removed")
        print("new obs #: ", temp_new_obs)
        print("")

        self.data = temp

#     def freq_1way(self, col_name):
#         """
#         Print the frequency count and percentage distribution of a single column, sorted by index,
#         and display it in a formatted table with borders. Rows with a count of zero are not shown.

#         :param col_name: The name of the column for which the frequency distribution is to be calculated.
#         """
#         # Get counts and sort by index
#         counts = self.data[col_name].value_counts(dropna=False).sort_index()
#         # Calculate percentages
#         percentages = (counts / counts.sum()) * 100
#         # Combine counts and percentages into a single DataFrame for better display
#         frequency_df = pd.DataFrame({
#             'Counts': counts,
#             'Percentage': percentages
#         })

#         # Filter out rows with zero counts and reset the index
#         frequency_df = frequency_df[frequency_df['Counts'] > 0].reset_index()

#         # Print results using tabulate for better formatting
#         print("---------Frequency Distribution for", col_name, "----------")
#         print(
#             tabulate(frequency_df,
#                      headers='keys',
#                      tablefmt='grid',
#                      showindex=False))
#         print("")
    def freq_1way(self, col_name, weight_col=None, include_unweighted=False):
        """
        Print the frequency count and percentage distribution of a single column, sorted by index,
        and display it in a formatted table with borders. Rows with a count of zero are not shown.
        If a weight column is specified, it calculates weighted frequency and percentages.

        :param col_name: The name of the column for which the frequency distribution is to be calculated.
        :param weight_col: Optional. The name of the column to be used for weighting the frequency and percentages.
        :param include_unweighted: Optional. Whether to include unweighted results alongside weighted results.
        """
        if weight_col:
            if weight_col not in self.data.columns:
                print(f"Error: The weight column '{weight_col}' does not exist.")
                return

            # Weighted frequency and percentage
            weighted_counts = self.data.groupby(col_name)[weight_col].sum()
            weighted_percentages = (weighted_counts / weighted_counts.sum()) * 100
            weighted_df = pd.DataFrame({
                'Weighted Counts': weighted_counts,
                'Weighted Percentage': weighted_percentages
            })

            # Unweighted frequency and percentage
            if include_unweighted:
                counts = self.data[col_name].value_counts(dropna=False).sort_index()
                percentages = (counts / counts.sum()) * 100
                unweighted_df = pd.DataFrame({
                    'Unweighted Counts': counts,
                    'Unweighted Percentage': percentages
                })
                frequency_df = pd.concat([unweighted_df, weighted_df], axis=1)
                title = f"Frequency Distribution for {col_name} (Weighted and Unweighted)"
            else:
                frequency_df = weighted_df
                title = f"Frequency Distribution for {col_name} (Weighted)"
        else:
            # Unweighted frequency and percentage
            counts = self.data[col_name].value_counts(dropna=False).sort_index()
            percentages = (counts / counts.sum()) * 100
            frequency_df = pd.DataFrame({
                'Counts': counts,
                'Percentage': percentages
            })
            title = f"Frequency Distribution for {col_name} (Unweighted)"

        # Filter out rows with zero counts and reset the index
        frequency_df = frequency_df[(frequency_df > 0).any(axis=1)].reset_index()
        pd.set_option('display.float_format', '{:.0f}'.format)
        # Print results using tabulate for better formatting
        print("---------", title, "----------")
        print(
            tabulate(frequency_df,
                     headers='keys',
                     tablefmt='grid',
                     showindex=False))
        print("")
        pd.reset_option('display.float_format')

    def freq_2way(self, col_name_1, col_name_2, exclude_equal=False):
        # Fill NaN values with a placeholder (e.g., 'Missing') for visibility in crosstab
        # Make a copy to avoid changing the original data
        temp_data = self.data
        temp_data[col_name_1] = temp_data[col_name_1].fillna('NaN')
        temp_data[col_name_2] = temp_data[col_name_2].fillna('NaN')

        # Generate crosstab data
        crosstab_result = pd.crosstab(temp_data[col_name_1],
                                      temp_data[col_name_2],
                                      rownames=[col_name_1],
                                      colnames=[col_name_2])

        # Reset index to make crosstab a regular DataFrame
        crosstab_result = crosstab_result.reset_index()

        # Melt the DataFrame to get a long format
        melted_crosstab = crosstab_result.melt(
            id_vars=[col_name_1], value_name='COUNT')

        # Filter out rows where COUNT is zero and optionally where values in column A are equal to values in column B
        if exclude_equal:
            melted_crosstab = melted_crosstab[
                (melted_crosstab['COUNT'] > 0)
                & (melted_crosstab[col_name_1] != melted_crosstab[col_name_2])]
            title = f"Two-way Frequency Table for {col_name_1} and {col_name_2} (Unequal Values Only)"
        else:
            melted_crosstab = melted_crosstab[melted_crosstab['COUNT'] > 0]
            title = f"Two-way Frequency Table for {col_name_1} and {col_name_2}"

        # Print results using tabulate for better formatting
        print("---------", title, "----------")
        print(
            tabulate(melted_crosstab,
                     headers='keys',
                     tablefmt='grid',
                     showindex=False))
        print("")

    def freq_multiway(self, columns, exclude_zeros=True, exclude_equal=False):
        # Make a copy to avoid changing the original data
        temp_data = self.data

        # Replace NaN values with a placeholder to ensure they are included as a category
        for col in columns:
            temp_data[col] = temp_data[col].fillna('NaN')

        # Generate crosstab data
        crosstab_result = pd.crosstab(
            index=[temp_data[col] for col in columns[:-1]],
            columns=temp_data[columns[-1]],
            rownames=columns[:-1],
            colnames=[columns[-1]])

        # Reset index to make crosstab a regular DataFrame and flatten MultiIndex
        crosstab_result.reset_index(inplace=True)
        melted_crosstab = pd.melt(
            crosstab_result, id_vars=columns[:-1], value_name='COUNT')

        # Apply filters
        if exclude_zeros:
            melted_crosstab = melted_crosstab[melted_crosstab['COUNT'] > 0]

        if exclude_equal and len(columns) > 1:
            # Check if all elements in each row are equal
            equal_filter = melted_crosstab.apply(lambda row: len(
                set(row[columns[:-1]].tolist() + [row[columns[-1]]])) == 1,
                axis=1)
            melted_crosstab = melted_crosstab[~equal_filter]

        # Sort the results
        melted_crosstab.sort_values(by=columns, inplace=True)

        # Print results using tabulate for better formatting
        title = f"Multi-way Frequency Table for {' ,'.join(columns)}"
        if exclude_equal:
            title += " (Non-equal Values Only)"
        print("---------", title, "----------")
        print(
            tabulate(melted_crosstab,
                     headers='keys',
                     tablefmt='grid',
                     showindex=False))
        print("")

    def data_construct(self, col_name, conditions_str, choices, default=-1):
        """
        Construct a new column in the data based on multiple conditions,
        where choices can be either fixed values or column references.
        Stop checking further conditions once a true condition is met for a row.

        :param col_name: Name of the new column to be added.
        :param conditions_str: A list of conditions (as strings) that determine the value to be assigned.
        :param choices: A list of values or column names to be assigned based on the conditions.
        :param default: The default value or column name to be assigned if none of the conditions are met. Default is -1.
        """
        temp_df = self.data

        # Initialize the new column with NaNs which will be replaced by the default at the end
        temp_df[col_name] = np.nan

        # Loop through each condition and choice, assign only if the column is still NaN
        for condition, choice in zip(conditions_str, choices):
            condition_series = temp_df.eval(condition)
            if isinstance(choice, str) and choice in temp_df.columns:
                # Apply choice from another column
                temp_df.loc[condition_series & temp_df[col_name].isna(),
                            col_name] = temp_df.loc[condition_series, choice]
            else:
                # Apply fixed choice
                temp_df.loc[condition_series & temp_df[col_name].isna(),
                            col_name] = choice

        # Fill remaining NaNs with the default value
        if isinstance(default, str) and default in temp_df.columns:
            temp_df[col_name].fillna(temp_df[default], inplace=True)
        else:
            temp_df[col_name].fillna(default, inplace=True)

        self.data = temp_df

    def copy_column(self, source_col, target_col):
        """
        Copies the values from one column to another, preserving the original column.

        :param source_col: The name of the source column whose values are to be copied.
        :param target_col: The name of the target column to which the values will be copied.
        """
        if source_col in self.data.columns:
            self.data[target_col] = self.data[source_col]
            print(
                f"Values from '{source_col}' were successfully copied to '{target_col}'.")
        else:
            print(
                f"Error: The column '{source_col}' does not exist in the DataFrame.")
    def fill_all_nans(self, fill_value):
        """
        Replace NaN values across all columns of the DataFrame with a specified value.

        :param fill_value: The value to use for replacing NaNs across all columns.
        """
        # Replace NaN values in all columns with the specified fill value
        self.data.fillna(fill_value, inplace=True)
        print(f"All NaN values have been replaced with {fill_value}.")
        
    def select_columns(self, col_list=None, prefixes=None):
        """
        Selects columns based on a list or common prefixes and updates the dataset.

        :param col_list: A list of column names to be retained in the dataset.
        :param prefixes: A list of common prefixes for column names to be retained. If both col_list and prefixes are provided,
                         columns that either match the list or any of the prefixes are retained.
        """
        cols_to_keep = set()

        if col_list:
            # Add columns from col_list to the set of columns to keep
            cols_to_keep.update(col_list)

        if prefixes:
            # Add columns that start with any of the provided prefixes
            for prefix in prefixes:
                cols_to_keep.update(col for col in self.data.columns if col.startswith(prefix))

        if not cols_to_keep:
            # If neither col_list nor prefixes are provided, or no columns match, raise an error
            raise ValueError("Either col_list or prefixes must be provided, and they must match existing columns.")

        # Filter the dataframe to only keep the selected columns
        self.data = self.data[list(cols_to_keep)]
        print(f"Data now contains only the selected columns: {list(cols_to_keep)}")
        
    def export_data(self, file_name, format, include_freq_report=False, max_categories=None, folder_path=None):
        """
        Export the data to a specified format and optionally create a frequency report for each variable.

        :param file_name: Name of the file without the extension.
        :param format: Format of the file to save ('excel', 'csv', 'stata', 'r', 'spss', 'sql').
        :param include_freq_report: Whether to include a frequency report as a separate file.
        :param max_categories: Maximum number of categories to include in the frequency reports for each variable.
        :param folder_path: The directory to save the file. If None, uses the current working directory.
        """
        # Define the file extension based on the format
        extensions = {
            'excel': '.xlsx',
            'csv': '.csv',
            'stata': '.dta',
            'r': '.pkl',  # Using pickle for R, though this is unconventional
            'spss': '.sav',
            'sql': ''  # SQL doesn't have a file extension for exporting; it interacts with databases
        }

        if format not in extensions:
            raise ValueError("Unsupported file format specified.")

        if folder_path is None:
            folder_path = os.getcwd()  # Use the current working directory if no folder path is provided

        # Add a date suffix to the filename
        date_suffix = datetime.datetime.now().strftime("%Y%m%d")
        base_file_path = os.path.join(folder_path, f"{file_name}_{date_suffix}")

        # Check if the file already exists and add a random number if it does
        full_file_path = base_file_path + extensions[format]
        while os.path.exists(full_file_path):
            random_suffix = random.randint(1000, 9999)  # Generate a random four-digit number
            full_file_path = f"{base_file_path}_{random_suffix}" + extensions[format]

        # Export data to the chosen format
        if format == 'excel':
            self.data.to_excel(full_file_path, index=False)
        elif format == 'csv':
            self.data.to_csv(full_file_path, index=False)
        elif format == 'stata':
            self.data.to_stata(full_file_path)
# =============================================================================
#         elif format == 'r':
#             self.data.to_pickle(full_file_path)
#         elif format == 'spss':
#             import pyreadstat  # Requires 'pyreadstat' module for SPSS
#             pyreadstat.write_sav(self.data, full_file_path)
# =============================================================================
# =============================================================================
#         elif format == 'sql':
#             self.data.to_sql(name='table_name', con=engine, if_exists='replace', index=False)
# =============================================================================

        # Optionally generate a frequency report
        if include_freq_report:
            freq_full_path = full_file_path.replace(extensions[format], '_freq_report.xlsx')

            with pd.ExcelWriter(freq_full_path) as writer:
                for column in self.data.columns:
                    freq_df = self.export_freq_1way(column, max_categories=max_categories)
                    freq_df.to_excel(writer, sheet_name=column, index=False)

            print(f"Frequency report has been saved to {freq_full_path}")

    def export_freq_1way(self, col_name, max_categories=None):
        """
        Generate a DataFrame of frequency counts and percentages for a column, with an optional limit on categories.
        Specifically designed for exporting data.

        :param col_name: Column name for frequency calculation.
        :param max_categories: Maximum number of categories to include. If more categories are present, only the top categories by count are shown.
        :return: DataFrame with frequency counts and percentages.
        """
        counts = self.data[col_name].value_counts(dropna=False)
        if max_categories is not None and len(counts) > max_categories:
            counts = counts.nlargest(max_categories)
        percentages = (counts / counts.sum()) * 100
        frequency_df = pd.DataFrame({
            'Counts': counts,
            'Percentage': percentages
        }).reset_index().rename(columns={'index': 'Category'})
        return frequency_df


# In[ ]:


acs_working = acs_raw

conditions = [
    acs_raw['SERIALNO'].str[4:6] == 'GQ',  # Condition for 'GQ'
    acs_raw['SERIALNO'].str[4:6] == 'HU'   # Condition for 'HU'
]

choices = [1, 0]

acs_working['INGRPQ'] = np.select(conditions, choices, default = -1)

# ACS Processing

# In[ ]:


acs = DataToolBox(acs_working)
acs.data_desc()
acs.data_exclude('INGRPQ == 0')
acs.data_exclude('AGEP >= 18')
acs.fill_all_nans(-9)


# CHIS Processing

# In[ ]:


chis = DataToolBox(chis_raw)
chis.data_desc()


# In[ ]:


acs.data_construct("sc_sex", ['SEX == 1', "SEX == 2"], [1,2])
chis.data_construct('sc_sex', ["SRSEX == 1", "SRSEX == 2"], [1,2])

acs.freq_2way('SEX', "sc_sex")
chis.freq_2way('SRSEX', "sc_sex")


# In[ ]:


acs.freq_1way('sc_sex', "PWGTP", include_unweighted=True)


# In[ ]:


acs.data_construct("sc_age_cont", ['AGEP <=99'], ['AGEP'])
chis.data_construct('sc_age_cont', ['SRAGE < 99', 'SRAGE >= 99'], ['SRAGE', 99])

# =============================================================================
# acs.freq_2way('AGEP','sc_age_cont', exclude_equal=True)
# chis.freq_2way('SRAGE', 'sc_age_cont', exclude_equal=True)
# 
# =============================================================================

# In[ ]:


acs.data_construct('sc_age_cat', [
    'AGEP < 18', 'AGEP >= 18 & AGEP < 25', 'AGEP >= 25 & AGEP < 35',
    'AGEP >= 35 & AGEP < 45', 'AGEP >= 45 & AGEP < 55',
    'AGEP >= 55 & AGEP <= 64', 'AGEP >= 65'
], list(range(7)))
chis.data_construct('sc_age_cat', [
    'SRAGE < 18', 'SRAGE >= 18 & SRAGE < 25', 'SRAGE >= 25 & SRAGE < 35',
    'SRAGE >= 35 & SRAGE < 45', 'SRAGE >= 45 & SRAGE < 55',
    'SRAGE >= 55 & SRAGE <= 64', 'SRAGE >= 65'
], list(range(7)))
# =============================================================================
# acs.freq_2way('AGEP', 'sc_age_cat')
# chis.freq_2way('SRAGE', 'sc_age_cat')
# =============================================================================

acs.freq_1way('sc_age_cat', "PWGTP", include_unweighted=True)



# In[ ]:


acs.data_construct('sc_hisp', ['HISP == 1', 'HISP != 1'], [1, 2])
acs.freq_2way('HISP', 'sc_hisp')

chis.data_construct('sc_hisp', ['SRH == 1', 'SRH != 1'], [1, 2])
chis.freq_2way('SRH', 'sc_hisp')

acs.freq_1way('sc_hisp', "PWGTP", include_unweighted=True)
# In[ ]:


acs.data_construct('sc_race_ethi', [
    'HISP == 1', 'RAC1P == 1', 'RAC1P == 2', 'RAC1P == 3 | RAC1P == 4 |RAC1P == 5',
    'RAC1P == 6', 'RAC1P == 7', 'RAC1P == 8 | RAC1P == 9'
], [1, 2, 3, 4, 5, 6, 7])

chis.copy_column('OMBSRREO','sc_race_ethi')

acs.freq_multiway(['sc_hisp', 'RAC1P','sc_race_ethi'])
chis.freq_2way('OMBSRREO', 'sc_race_ethi')


# In[ ]:


acs.data_construct('sc_cit', ['CIT == 1|CIT == 2|CIT==3', 'CIT ==4', 'CIT==5'],
                   [1, 2, 3])
chis.copy_column('CITIZEN2', "sc_cit")

acs.freq_2way('CIT', 'sc_cit')
chis.freq_2way('CITIZEN2', 'sc_cit')

acs.freq_1way('sc_cit')
chis.freq_1way('sc_cit')


# In[ ]:


acs.data_construct('sc_edu', [
    'SCHL >= 4 & SCHL <= 11', 'SCHL >= 12 & SCHL <= 14',
    'SCHL >= 15 & SCHL <= 17', 'SCHL >= 18 & SCHL <= 19', 'SCHL == 20',
    'SCHL == 21', 'SCHL == 22', 'SCHL == 23', 'SCHL == 24',
    'SCHL >= 1 & SCHL <= 3', 'SCHL == -9'
], [1, 2, 3, 4, 6, 7, 9, 8, 10, 91, 91])

chis.copy_column('AHEDUC', 'sc_edu')

# acs.freq_2way("SCHL", 'sc_edu')
# chis.freq_2way("AHEDUC", 'sc_edu')

acs.freq_1way('sc_edu')
chis.freq_1way('sc_edu')


# In[ ]:


acs.copy_column('HICOV', "sc_ins")
chis.copy_column('INS', "sc_ins")

acs.freq_1way('sc_ins')
chis.freq_1way('sc_ins')


# In[ ]:


acs.data_construct('sc_emp', ['ESR == 1|ESR ==4', 'ESR == 2|ESR ==5','ESR == 3|ESR ==6' ], [1,2, 3])
chis.data_construct('sc_emp', ['WRKST == 1|WRKST == 2', 'WRKST == 3', 'WRKST == 4|WRKST == 5'], [1,2,3])


acs.freq_2way('ESR', 'sc_emp')
chis.freq_2way('WRKST', 'sc_emp')

acs.freq_1way('sc_emp')
chis.freq_1way('sc_emp')


# In[ ]:


# acs.freq_1way('TEN')

acs.data_construct('sc_housing', ['TEN == 1 | TEN == 2', 'TEN == 3 | TEN == 4'], [1,2])
chis.copy_column('SRTENR', "sc_housing")
# acs.freq_2way('TEN', "sc_housing")

acs.freq_1way('sc_housing')
chis.freq_1way('sc_housing')


# In[ ]:


acs.data_construct('sc_poverty', ['POVPIP <= 99', 'POVPIP >= 100 & POVPIP <= 199',
                   'POVPIP >= 200 & POVPIP <= 299', 'POVPIP >= 300'], [1, 2, 3, 4])
chis.copy_column('POVLL', 'sc_poverty')

acs.freq_1way('sc_poverty')
chis.freq_1way('sc_poverty')


# In[ ]:


acs.copy_column('MAR', 'sc_marit')
chis.data_construct('sc_marit', ['AH43 == 1', 'AH43 == 3', 'AH43 == 4',
                    'AH43 == 5', 'AH43 == 2|AH43 == 6'], [1, 2, 3, 4, 5])

chis.freq_2way('AH43', 'sc_marit')

acs.freq_1way('sc_marit')
chis.freq_1way('sc_marit')


# In[ ]:


chis.select_columns(prefixes= ['sc_', 'RAKEDW'])
acs.select_columns(prefixes=['sc', 'PWGTP', 'PUMA10', 'PUMA20', 'REGION', 'ST'])


# In[ ]:


acs.export_data('acs', 'csv', include_freq_report=True, max_categories=20, folder_path='Data/Output Data')
chis.export_data('chis', 'csv', include_freq_report=True, max_categories=20, folder_path='Data//Output Data')


# In[ ]:


acs.export_data('acs', 'stata', include_freq_report=True, max_categories=20, folder_path='Data/Output Data')
chis.export_data('chis', 'stata', include_freq_report=True, max_categories=20, folder_path='Data//Output Data')


# In[ ]:


acs_model = acs.return_data()


# In[ ]:


import pysurveys as ps


# In[ ]:




