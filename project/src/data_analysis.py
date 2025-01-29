import pandas as pd
from scipy.stats import binomtest
import matplotlib as plt

df = pd.read_csv("C:/Users/97258/Downloads/Metadata_Release_Anon (1).csv")

'''Analisys for the cleaned data'''

def count_by_range(df, number_columns, letter_column, lower_range, upper_range):
    """
    this function counts rows in the data where values in specified numeric columns fall within a given range 
    and calculates the percentage of occurrences for each unique value in another column. the parameters are:
    df - the input DataFrame to analyze, number_columns (list) - a list of numeric column names to evaluate,
    letter_column (str) - the name of the column containing categorical values to count, lower_range (float)-
    the lower limit of the range, upper_range (float) - the upper limit of the range. the function returns:
    a data with the count and percentage of rows for each unique value in the letter_column that fits the
    conditions.
    """
    #define the condition to count how many rows are within the range
    condition = df[number_columns].apply(lambda row: ((row >= lower_range) & (row <= upper_range)).sum(), axis=1) >= 4

    #filter rows that follow the condition
    filtered_df = df[condition]

    #count the occurrences of each unique value in letter_column
    letter_counts = filtered_df[letter_column].value_counts()

    #count the total occurrences of each unique value in the entire dataset
    total_counts = df[letter_column].value_counts()

    #calculate percentages
    percentages = (letter_counts / total_counts * 100).fillna(0)

    #combine counts and percentages into a  new dataframe
    result = pd.DataFrame({
        'Count': letter_counts.astype(int),
        'Percentage': percentages
    }).sort_index()
    return result

def analyze_column_significant_only(good_data, bad_data, column, return_type=1):
    """
    this function analyzes the significance of differences between good and bad counts for a specific column
    using a binomial test. the parameters are: good_data - DataFrame containing good counts for each category
    in the column, bad_data - DataFrame containing bad counts for each category in the column, column (str) -
    the column being analyzed (lobe or pathology), return_type (int) - Determines the behavior of the function:
         1: Print significant results and return only significant results.
         Other: Return all results, including non-significant ones.
    the function returns: list[dict] - a list of dictionaries, where each dictionary contains:
         - "column": The category being analyzed.
         - "Good Count": Count of good data for the category.
         - "Bad Count": Count of bad data for the category.
         - "P-value": The p-value from the binomial test.
         - "Significant": Boolean indicating if the result is significant (p < 0.05).
    """
    #make sure the catagories match between good_data and bad_data
    our_column = good_data.index.intersection(bad_data.index) 
    results = [] #initializing an empty list to put results

    #loop through each catagory in column
    for type in our_column:
        #get a good and bad count for the catagory
        good_count = good_data.loc[type, 'Count']
        bad_count = bad_data.loc[type, 'Count']
        #the total count for the catagory
        total_count = good_count + bad_count

        #perform binomial test
        stat = binomtest(k=int(good_count), n=int(total_count), p=0.5, alternative='two-sided')
        p_value = stat.pvalue

        #determine if there is significance
        significant = p_value < 0.05
        #storing the results in a dictionary
        result = {
            "column": type, #name of catagory
            "Good Count": good_count, #count of the good data
            "Bad Count": bad_count, #count of the bad data
            "P-value": p_value, #the p-value from the test
            "Significant": significant, #is true when p<0.05
        }
        #adding result to list
        results.append(result)

        #print only significant results when return_type is 1
        if significant and return_type == 1:
            print(f"Found significant difference between good and bad counts for {column} {type}.")
            print(f"Good Count: {good_count}, Bad Count: {bad_count}")
            print(f"P-value: {p_value:.10f}")
            print("-" * 50)

    #filter results - if return_type is 1 include only significant results
    if return_type == 1:
        results = [res for res in results if res["Significant"]]
    return results


# A function that calls and runs all the analyze functions for each column
def general_analyze(df,columns):
    """
    this function runs the analysis for each specified column by calling helper functions to calculate
    good and bad counts and analyzing their significance. the parameters are: df - the input data to analyze,
    columns (list) - a list of column names (categorical columns) to analyze. the function has no returns
    """
    #defining the list of columns 
    list = ["ILAE_Year1","ILAE_Year2","ILAE_Year3","ILAE_Year4","ILAE_Year5"]
     #iterate through each column specified in the columns list
    for column in columns:
        #calculate good count, where at least four values are 1 or\and 2
        good_count = count_by_range(df,list,column,1,2)
        #calculate bad count, where at least four values are in the range 3-5
        bad_count = count_by_range(df,list,column,3,5)
        #make the significance analysis for good and bad data for the current column
        analyze_column_significant_only(good_count,bad_count,column)

'''Analysis for the excluded data'''

def check_commonality_with_comparison(df, excluded_df, threshold=0.8):
    """
    this function identifies categorical values that are still in the data even after filtering,
    based on a threshold. the parameters are: df - the original data before filtering, excluded_df -
    the data containing excluded rows (filtered-out data), threshold (float, optional) - the
    percentage of the original occurrences required for a value to be considered "common" after filtering.
    default is 0.8 (80%). the function returns: dict: a dictionary where keys are column names and values
    are the common values that meet the threshold.

    the function prints:the number of rows before and after filtering and details of values that meet
    the threshold condition.
    """
    #initiating a dictionary to store values that match the conditions
    common_values = {}
    #the number of rows in the data before the filtering
    total_rows_before = len(df)
    total_rows_after = len(excluded_df)
    #calculate the minimum count that means a value is "common" 
    threshold_count_before = total_rows_before * threshold  # Threshold based on original DataFrame
    #printing the basic statistics
    print(f"Original number of rows: {total_rows_before}")
    print(f"Filtered number of rows: {total_rows_after}")
    #iterate over each column in the original data
    for column in df.columns:
        if df[column].dtype == 'object':  # Check only categorical columns (strings)
            #count unique values before filtering (in the original data)
            value_counts_before = df[column].value_counts()
            
            #count unique values after filtering (in the excluded data)
            value_counts_after = excluded_df[column].value_counts()
            #comparing value counts befor and after filtering
            for value, count_before in value_counts_before.items():
                count_after = value_counts_after.get(value, 0) #defult 0 if missing
                
                #check if the count of this value after filtering meets the threshold percentage of the original count
                if count_after >= threshold_count_before:
                    #storing the common vaalue in the dictionary
                    common_values[column] = value
                    #printing the ditales of common
                    print(f"Common value found in '{column}': {value}")
                    print(f"Before filtering: {count_before} occurrences")
                    print(f"After filtering: {count_after} occurrences")
                    print("-" * 50)
    
    #if there are common values found, print them
    if common_values:
        print("Common values found across the DataFrame after filtering:")
        for column, value in common_values.items():
            print(f"{column}: {value}")
    else:
        print("No common values found based on the threshold")
    return common_values