import pandas as pd
from src.data_analysis import count_by_range
from src.data_analysis import analyze_column_significant_only
from src.data_analysis import check_commonality_with_comparison


# Test function
def test_count_by_range():
    '''
    This function will test the behavior and correctness of the count_by_range function.
    It will create a new data frame and will run the function and check if the results
    are as expected
    '''
    
    # Creating a sample DataFrame
    data = {
        'col1': [3, 2, 1, 3, 2],
        'col2': [2, 2, 1, 3, 4],
        'col3': [4, 2, 1, 2, 3],
        'col4': [1, 3, 2, 3, 4],
        'col5': [2, 1, 2, 3, 1],
        'letter_col': ['A', 'B', 'A', 'A', 'B']
    }

    # Reading the data frame and saving it as df
    df = pd.DataFrame(data)
    
    # Using the function and saving it in the results
    result = count_by_range(df, ['col1', 'col2', 'col3', 'col4', 'col5'], 'letter_col', 2, 4)

    # Creating and saving the expected result
    expected_result = pd.DataFrame({
        'Count': [2, 2], #number of saved data
        'Percentage': [66.66666666666666, 100.000000] #percentsge of the data in the specific letter
    }, index=['A', 'B'])

    # Checking if the results equals to the expected results
    if result.equals(expected_result):
        print("test_count_by_range Passed!")
    else:
        print("Test Failed!")
        print("Expected:")
        print(expected_result)
        print("Got:")
        print(result)




# Test function for analyze_column_significant_only
def test_analyze_column_significant_only():
    '''
    This function will check if the analyze_column_significant_only function runs correctly
    It will be given a good data and a bad data, then run the function on them, checking if the results 
    equals to what we expected 
    '''
    # Creating a good data and a bad data
    good_data = pd.DataFrame({
        'Count': [5, 15, 8, 12],
    }, index=['A', 'B', 'C', 'D'])

    bad_data = pd.DataFrame({
        'Count': [10, 20, 8, 2],
    }, index=['A', 'B', 'C', 'D'])

    # Naming the column to analyze
    column = 'Test Column'

    # Running the function
    results = analyze_column_significant_only(good_data, bad_data, column)

    # Check if we got any significant result as expected
    if len(results) == 1:
        print("test_analyze_column_significant_only passed!")
    else:
        print("Test failed.")



def test_check_commonality_with_comparison():
    '''
    This test checks if the function check_commonality_with_comparison() correctly identifies 
    common values between two Data's (df and excluded_df) based on a given threshold.
    it will give to the function two dataws, the main one and the excluded dad and will expect to 
    get in return if there is a common value in the excluded data as expected
    '''
    # Creating the main data and saving it as df
    data = {
        'Category': ['A', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'A'],  # Categorical column
        'Values': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],  # Numeric column
        'Category2': ['X', 'X', 'Y', 'Z', 'X', 'Y', 'Y', 'X', 'Z', 'Z']  # Another categorical column
    }
    df = pd.DataFrame(data)

    # Creatint the excluded data with some rows filtered out and saving it as excluded_data
    excluded_data = {
        'Category': ['A', 'B', 'C', 'B', 'A', 'A'],  # Filtered version of Category
        'Values': [1, 2, 3, 6, 7, 9],  # Filtered numeric column
        'Category2': ['X', 'X', 'Z', 'X', 'Y', 'Z']  # Filtered version of Category2
    }
    excluded_df = pd.DataFrame(excluded_data)

    # Defining the threshold
    threshold = 0.3  # 30%

    # Calling the function
    common_values = check_commonality_with_comparison(df, excluded_df, threshold)

    # ECreating the expected result
    expected_common_values = {
        'Category': 'A',    # 'A' appears frequently enough in both DataFrames
        'Category2': 'X'    # 'X' meets the threshold count
    }

    # Validating the results
    if common_values == expected_common_values:
        print("test_check_commonality_with_comparison Passed!")
    else:
        print("Test Failed!")
        print("Expected:")
        print(expected_common_values)
        print("Got:")
        print(common_values)

# Run the test
#test_check_commonality_with_comparison()
