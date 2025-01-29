import numpy as np
import pandas as pd
from src.data_cleaning import lobe_extraction
from src.data_cleaning import clean_lobe_column
from src.data_cleaning import remove_rows_with_too_many_nans
from src.data_cleaning import refill_nan_with_previous
from src.data_cleaning import filter_rows_by_conditions
from src.data_cleaning import calculate_mean_age




def test_lobe_extraction():
    '''
    This test will check that the lobe_extraction function works as needed. 
    It will be given a list with containig different values and will be expected 
    to return a new column with only the lobe values
    '''
    # Creating the exam data and saving it 
    data = {"Op_Type": ["T Lx", "FOP", "O Lx", "P", None]}
    df = pd.DataFrame(data)
    
    # Creating the expected output for the 'lobe' column
    expected_lobe = ["T", "F", "O", "P", None]
    
    # Runing the function on the data created
    result_df = lobe_extraction(df, "Op_Type")
    
    # Checking if the 'lobe' column matches the expected output
    assert list(result_df["lobe"]) == expected_lobe, "Test failed: lobe extraction is incorrect."
    print("test_lobe_extraction passed")


def test_clean_lobe_column():
    '''
    This function will check if the clean_lobe_column works as expected.
    It will be given a data with the valid and invalid values (for the lobe column)
    and take out the invalid values while leaving the valid values in the column
    '''
    # Creating the exam data and saving it 
    data = {
        "lobe": ["T", "F", "X", None, "P", "O", "TF", ""],
        "other_column": [1, 2, 3, 4, 5, 6, 7, 8],  # Extra column to see it remains unchanged
    }
    df = pd.DataFrame(data)
    
    # Expected output: Only rows where 'lobe' is "T", "F", "P", or "O"
    expected_data = ["T", "F", "P", "O"]

    
    # Run the function
    result_df = clean_lobe_column(df)
    
    # Assertion: Check if the 'lobe' column in the cleaned DataFrame matches the expected values
    assert list(result_df["lobe"]) == expected_data, "Test failed: Cleaned lobe column is incorrect."
    print("test_clean_lobe_column passed!")




def test_remove_rows_with_too_many_nans():
    '''
    This test verifies that remove_rows_with_too_many_nans() correctly removes rows
    containing too many NaN values in specified columns while preserving the other rows.
    It will call the function to clean the data and check if it cleaned it as expected)
    '''
    # Creating the data and saving it as df
    data = {
        "col1": [1, None, 3, None, 5],
        "col2": [None, None, 3, 4, None],
        "col3": [1, 2, None, None, None],
        "other_col": [10, 20, 30, 40, 50],  # Extra column to ensure it's preserved
    }
    df = pd.DataFrame(data)
    
    # Specifying columns to check and the maximum allowed NaNs (only 1)
    columns_to_check = ["col1", "col2", "col3"]
    max_allowed_nans = 1  
    
    # Creating the expected_data  
    expected_data = {
        "col1": [1, 3],
        "col2": [None, 3],
        "col3": [1, None],
        "other_col": [10, 30],
    }
    expected_df = pd.DataFrame(expected_data)
    
    # Runing the function
    result_df = remove_rows_with_too_many_nans(df, columns_to_check, max_allowed_nans)
    
    # Checking if the resulting data matches the expected data frame
    pd.testing.assert_frame_equal(result_df, expected_df, check_dtype=False, check_exact=False)
    print("test_remove_rows_with_too_many_nans passed!")





def test_refill_nan_with_previous():
    '''
    This test checks whether refill_nan_with_previous() correctly fills NaN 
    values with the previous row’s value in the specified columns.
    It will give the gunction a data to refill the NaN's and will check if the
    function returned the data as expected 
    '''
    # Creating the data and saving it as df
    data = {
        "col1": [1.0, None, 3.0, 4.0],
        "col2": [None, 2, None, 4.0],
        "col3": [1.0, 2.0, None, None],
    }
    df = pd.DataFrame(data)
    
    # Columns to process
    columns = ["col1", "col2", "col3"]
    
    # Creating the expected data frame and saving it as expected_df
    expected_data = {
        "col1": [1.0, None, 3.0, 4.0],      
        "col2": [1.0, 2.0, 3.0, 4.0],   
        "col3": [1.0, 2.0, 3.0, 4.0],        
    }
    expected_df = pd.DataFrame(expected_data, dtype=float) 
    
    # Runing the function
    result_df = refill_nan_with_previous(df, columns)
    
    # Assertion
    pd.testing.assert_frame_equal(result_df, expected_df, check_dtype=True)
    print("test_refill_nan_with_previous passed!")




def test_filter_rows_by_conditions():
    '''
    This test verifies that the function filter_rows_by_conditions() correctly 
    filters rows based on the predefined condition. It will give the function a data
    to clean, the check if the cleaning has been done as expected.
    '''
    # Creating the data then saving it as df
    data = {
        "ILAE_Year1": [1, 3, 2, 4, 5],
        "ILAE_Year2": [2, 3, 1, 5, 4],
        "ILAE_Year3": [1, 2, 3, 4, 5],
        "ILAE_Year4": [2, 3, 4, 5, 1],
        "ILAE_Year5": [1, 2, 3, 4, 5],
    }
    df = pd.DataFrame(data)

    # Defining the conditions: 4 values in (1, 2) or (3, 5)
    conditions = [((1, 2), 4), ((3, 5), 4)]

    # Calling the function
    included_df, excluded_df = filter_rows_by_conditions(
        df, ["ILAE_Year1", "ILAE_Year2", "ILAE_Year3", "ILAE_Year4", "ILAE_Year5"], conditions
    )

    # Creating the expected results (included and excluded data)
    expected_included = pd.DataFrame({
        "ILAE_Year1": [1, 4, 5],
        "ILAE_Year2": [2, 5, 4],
        "ILAE_Year3": [1, 4, 5],
        "ILAE_Year4": [2, 5 ,1],
        "ILAE_Year5": [1, 4, 5],
    }).reset_index(drop=True)

    expected_excluded = pd.DataFrame({
        "ILAE_Year1": [3, 2],
        "ILAE_Year2": [3, 1],
        "ILAE_Year3": [2, 3],
        "ILAE_Year4": [3, 4],
        "ILAE_Year5": [2, 3],
    }).reset_index(drop=True)

    # Checking the results
    try:
        pd.testing.assert_frame_equal(included_df, expected_included)
        pd.testing.assert_frame_equal(excluded_df, expected_excluded)
        print("test_filter_rows_by_conditions passed! ")
    except AssertionError as e:
        print("Test failed! ")
        print(e)






def test_calculate_mean_age():
    '''
    This test verifies that the function calculate_mean_age() correctly extracts mean age 
    values from different age range formats and assigns them to a new column, while taking in 
    consideration special cases. It will give the function a data to create from it a new column
    with the mean ages and will check if it returned a column as expected
    '''
    # Createing a new data and saving it as df
    test_data = {
        "age_range": [
            "1 to 5",
            "10 to 20",
            "Less than 1",
            "Over 40",
            "1.5 to 4.0",
            np.nan,  # NaN value
        ]
    }
    df = pd.DataFrame(test_data)
    
    # Creating the expected output and saving it as expected_df
    expected_data = {
        "age_range": [
            "1 to 5",
            "10 to 20",
            "Less than 1",
            "Over 40",
            "1.5 to 4.0",
            np.nan,
        ],
        "mean_age": [
            3.0,  # (1 + 5) / 2
            15.0,  # (10 + 20) / 2
            1.0,  # "Less than 1"
            40.0,  # "Over 40"
            2.75, # (1.5 + 4) / 2
            np.nan,  # NaN remains NaN
        ]
    }
    expected_df = pd.DataFrame(expected_data)
    
    # Running the function
    result_df = calculate_mean_age(df, "age_range", "mean_age")
    
    # Checking the results matches the expected output
    pd.testing.assert_frame_equal(result_df, expected_df, check_dtype=False)
    print("test_calculate_mean_age passed!")



