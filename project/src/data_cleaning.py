import pandas as pd
import numpy as np

#instaling the excel file
df = pd.read_csv("C:/Users/97258/Downloads/Metadata_Release_Anon (1).csv")

#Op_type Cleaning 

def lobe_extraction(df,column):
    """
    the function extracts specific lobe types ('T', 'F', 'O', 'P') from a column in the data and creates a new column
    named 'lobe' to store the values it extracts. the parameters are: df - the input data,
    column (str) - the name of the column from which to extract lobe information. the function returns: 
    the modified data with an additional 'lobe' column containing the extracted values.
    """
    #creating a new column and naming it 'lobe', extracting from the column (Op_Type) only the "T,F,O,P" (as string)
    # to the new colum, making sure that it adds to the 'lobe' column. 
    df["lobe"] = df[column].str.extract(r"(T|F|O|P|)", expand = False)  
    return df 

def clean_lobe_column(df): 
    '''    
    the function filters the data to include only rows where the 'lobe' column contains exactly one of the valid lobe
    values ('T', 'F', 'P', 'O'). the parameter is: df - The input data containing a 'lobe' column. The function returns:
    a new data with rows that match the valid lobe pattern.
    '''
    # defining the valid pattern letters to be: T, F, P, O (as aregular expretion)
    valid_pattern = r'^[TFPO]$'
    
    # filter the df based on the pattern we made as valid_pattern 
    cleaned_data = df[df['lobe'].str.match(valid_pattern, na=False)]
    return cleaned_data

def remove_rows_with_too_many_nans(df, columns, max_allowed_nans):
    """
    this function removes the rows where the number of NaN values in the specified columns is more then the allowed number
    the parameters are: df - The input data, columns (list) - A list of column names to check for NaN values,
    max_allowed_nans (int): The maximum number of NaN values allowed per row in the specified columns. the functio returns:
    a clean data with rows that have less then/the amount of NaNs allowed and the index reset.
    """
    #count the number of NaNs in the specified columns for each row
    nan_counts = df[columns].isna().sum(axis=1)
    
    #remove rows where there are too many NaNs and reset index
    cleaned_df = df.loc[nan_counts <= max_allowed_nans].reset_index(drop=True)
    return cleaned_df

def refill_nan_with_previous(df, columns):
    '''    
    this function fills NaN values in the specified columns by replacing them with the value from the previous column in
    the same row. The parameters are: df - the input data, columns (list) - a list of column names in the correct order
    for the refilling. the function returns: the updated data with NaN values replaced.
    '''
    #iterating through each row in the data
    for index, row in df.iterrows():
        #iterating throughspecific columns by thier indedx
        for col_idx, col_name in enumerate(columns):
             #check if current cell is NaN
            if pd.isna(row[col_name]): 
                #make sure there's a previous column to copy the data from
                if col_idx > 0:  
                    #get the name of the privious column
                    previous_col = columns[col_idx - 1]
                    #replace the NaN with the value from the column before
                    df.at[index, col_name] = row[previous_col]
    return df

def filter_rows_by_conditions(df, number_columns, conditions):
    """
    this function filters rows in the data based on the base of certine rules. the parameters are: df - The input data to filter,
    number_columns (list) - a list of numeric column names to apply the conditions to, conditions (list of tuples) - 
    each tuple contains: 1.value_range (tuple): A range (min, max) to filter values in the numeric columns
    2.min_count (int): The minimum number of columns in a row that must satisfy the range condition. the function returns:
    included_df: the data containing rows that are according to te rules and excluded_df: the data containing rows
    that do not follow the rules.
    """
    # Track indices of the rows that meet the conditions
    included_indices = set()
    #loop through each condition in the condition list
    for value_range, min_count in conditions:
        #define the condition check how many numeric columns in each row fall in the range
        condition = df[number_columns].apply(
            lambda row: ((row >= value_range[0]) & (row <= value_range[1])).sum(), axis=1
        ) >= min_count
        #add indices of rows that meet the condition
        included_indices.update(df[condition].index)
    #create DataFrame of included rows that meet the condition to the set of included indices
    included_df = df.loc[list(included_indices)].reset_index(drop=True) 
    #create DataFrame of excluded rows that do not meet the conditions
    excluded_df = df.drop(index=list(included_indices)).reset_index(drop=True)
    return included_df, excluded_df

#Age Cleaning

def calculate_mean_age(df, column_name, new_column_name):
    """
    this function calculates the mean age for ranges in a specified column and adds the result
    as a new column in the data, taking to consideration special casees. the parameters are:df - The input data, column_name (str) -
    the name of the column containing age ranges or special rules, new_column_name (str) - 
    the name of the new column to store the calculated mean ages. the function returns:
    the updated DataFrame with the new column added.
    """
    #initialize an empty list to store the mean values
    mean_ages = []

    #iterate through each value in the specified column
    for value in df[column_name]:
        if pd.isna(value):
            #if the value is a NaN - append to the result list
            mean_ages.append(np.nan)  # Handle NaN values
        elif value == 'Less than 1': #special case
            mean_ages.append(1) 
        elif value == 'Over 40': #special case
            mean_ages.append(40)  
        else:
            try:
                #split the range and calculate the mean
                parts = value.split(' to ') #spliting the string by the "to"
                #calculate the mean of the two numbers
                mean_ages.append((float(parts[0]) + float(parts[1])) / 2)
            except Exception as e:
                #raise an error if an invalid input is tried
                raise ValueError(f"Invalid value '{value}' encountered in column '{column_name}': {e}")

    #add the new column to the data with the mean age calculated
    df[new_column_name] = mean_ages
    return df
