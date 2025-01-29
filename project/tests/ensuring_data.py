import pandas as pd


''' Checking That Every Column We Need, Had Only The Correct Values '''
def get_unique_cell_values_with_nan(df, column_name):
    '''
    This function will extract the unique values from a specified column in a df, including NaN  values.
    it will be given the Data to work with and the name of the column, and will return a set of the unique values 
    that are in this column
    '''
    #checking that the column given is in the df
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in the DataFrame.") 

    # Retrieving all the unique values that are in the column including Nan
    unique_values = df[column_name].unique()

    # Returning the unique values in a set (for comodity...)
    return set(unique_values)

def get_unique_general(df,column_list):
    '''
    This function will handle multiple columns in the df while using the get_unique_cell_values_with_nan function.
    It will be given the data to work with and the list of columns we want to extract from them the unique values,
    returning a dictionary of the unique values for each column choosen, and printing it
    '''

    #Creating a dictionary to story the unique values for each column
    results = {} 

    #going through every column in the list given
    for column in column_list:

        unique_values = get_unique_cell_values_with_nan(df, column) #retrieving the unique values using the function before 
        results[column] = unique_values #saving the unique values in the dictionary with the column name as the key
        print(f"Unique values in column '{column}':") #printing the name of the column
        print(unique_values) #printing the inique values
        print()  # printing a line break for cleanliness
    
    #Returning the dictionary
    return results
    






