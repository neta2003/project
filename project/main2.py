''' Importing Phase :'''
import pandas as pd

from tests.test_data_cleaning import test_lobe_extraction
from tests.test_data_cleaning import test_clean_lobe_column
from tests.test_data_cleaning import test_remove_rows_with_too_many_nans
from tests.test_data_cleaning import test_refill_nan_with_previous
from tests.test_data_cleaning import test_filter_rows_by_conditions
from tests.test_data_cleaning import test_calculate_mean_age
from src.data_cleaning import lobe_extraction 
from src.data_cleaning import clean_lobe_column
from src.data_cleaning import remove_rows_with_too_many_nans
from src.data_cleaning import refill_nan_with_previous
from src.data_cleaning import filter_rows_by_conditions
from src.data_cleaning import calculate_mean_age

from tests.ensuring_data import get_unique_general

from tests.test_data_analysis import test_count_by_range
from tests.test_data_analysis import test_analyze_column_significant_only
from tests.test_data_analysis import test_check_commonality_with_comparison
from src.data_analysis import general_analyze
from src.data_analysis import check_commonality_with_comparison

from src.data_visualisation import plot_multiple_columns_with_good_and_bad
from src.data_visualisation import plot_lobe_distribution_per_pathology
from src.data_visualisation import plot_general_analyze_results_all


# Reading the data
df = pd.read_csv("C:/Users/97258/Downloads/Metadata_Release_Anon (1).csv")


# Testing the data_cleaning functions
test_lobe_extraction()
print()
test_clean_lobe_column()
print()
test_remove_rows_with_too_many_nans()
print()
test_refill_nan_with_previous()
print()
test_filter_rows_by_conditions()
print()
test_calculate_mean_age()

# Testing the data_analisys functions
test_count_by_range()
test_analyze_column_significant_only()
test_check_commonality_with_comparison()

# Running the data_cleaning functions
df = lobe_extraction(df,"Op_Type") 
df = clean_lobe_column(df) 
df_all = remove_rows_with_too_many_nans(df, ["ILAE_Year1","ILAE_Year2","ILAE_Year3","ILAE_Year4","ILAE_Year5"],1)
general_df = refill_nan_with_previous(df_all,["ILAE_Year1","ILAE_Year2","ILAE_Year3","ILAE_Year4","ILAE_Year5"])
df, excluded_df = filter_rows_by_conditions(general_df,["ILAE_Year1","ILAE_Year2","ILAE_Year3","ILAE_Year4","ILAE_Year5"],[((1, 2), 4), ((3, 5), 4)])
df = calculate_mean_age(df,"Binned_Onset_Age","mean_age")


# Ensuring the data
list_of_columns = ("lobe","Pathology","mean_age","ILAE_Year1","ILAE_Year2","ILAE_Year3","ILAE_Year4","ILAE_Year5")
get_unique_general(df,list_of_columns)
print()
print()


# Running the data_analysis functions
general_analyze(df,["mean_age", "Pathology", "lobe"]) # Calling the function that will operate the analysis for each column
print()
common = check_commonality_with_comparison(general_df, excluded_df, threshold=0.17)


# Running the data_visualization functions
plot_multiple_columns_with_good_and_bad(df,[["Pathology"],["lobe"],["mean_age"]],)
plot_lobe_distribution_per_pathology(df, pathology_column="Pathology", lobe_column="lobe")
columns_to_analyze = ["lobe", "Pathology","mean_age"]
plot_general_analyze_results_all(df, columns_to_analyze)

