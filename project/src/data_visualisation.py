import matplotlib.pyplot as plt
import pandas as pd
from src.data_analysis import count_by_range
from tests.ensuring_data import get_unique_cell_values_with_nan
from src.data_analysis import analyze_column_significant_only

''' Plotting the good and bad for each collumn '''

def plotting_with_good_and_bad(
    df,  
    letter_column, 
    title, 
    xlabel, 
    ylabel = "Count", 
    good_range=(1, 2), 
    bad_range=(3, 5)
):
    '''
    This function creates a bar chart comparing "Good" and "Bad" outcomes based on a given categorical
    column in the dataset. It gets the df to work with, the letter collumn that is the column, the title
    to write in the plot , the xlabel and ylabel to plot (with a default in ylabel as "Count"), and also
    the good and the bad range (with a degault of (1, 2) and (3, 5)). In return it will use this values 
    to plot the bar chart
    '''
    # Getting the "Good" and "Bad" data counts using count_by_range
    good_data = count_by_range(df, ["ILAE_Year1","ILAE_Year2","ILAE_Year3","ILAE_Year4","ILAE_Year5"], letter_column, *good_range)['Count']
    bad_data = count_by_range(df, ["ILAE_Year1","ILAE_Year2","ILAE_Year3","ILAE_Year4","ILAE_Year5"], letter_column, *bad_range)['Count']

    # Combining the data into a single DataFrame for plotting
    combined_data = pd.DataFrame({
        "Good": good_data,
        "Bad": bad_data
    })

    # Ploting side-by-side bars
    combined_data.plot(kind="bar", figsize=(10, 6), color=["skyblue", "salmon"]) #skyblue for the good data and salmon for the bad data
    plt.title(title) #writing the title as the title
    plt.xlabel(xlabel) #writing the xlabel as the xlabel
    plt.ylabel(ylabel) #writing the ylabel as the ylabel
    plt.xticks(rotation=45) #Rotating x-axis labels for better readability.

    # Annotating bars with counts by taking one value from "Good" and one value from "Bad" at the same time.
    #Providing idx (index of the bar) for placement on the x-axis.
    for idx, (good, bad) in enumerate(zip(combined_data['Good'], combined_data['Bad'])):
        # Shifting labels to align correctly with bars. idx: moving the text, good/bad : placing the
        # label above the bar, int : converting the number to an intiger, va : positioning the text
        # on top of the bar, fontsize : setting the text size, color : choosing the label color
        plt.text(idx - 0.2, good + 1, int(good), va='bottom', fontsize=10, color='blue') 
        plt.text(idx + 0.2, bad + 1, int(bad), va='bottom', fontsize=10, color='red')

    plt.legend(["Good (1-2)", "Bad (3-5)"]) #adding a leggend 
    plt.tight_layout() #ensuring labels dont overlap
    plt.show() #displaing the plot

def plot_multiple_columns_with_good_and_bad(
    df,  
    letter_columns, 
    good_range=(1, 2), 
    bad_range=(3, 5)
):
    '''
    This function is a wrapper that calls the plotting_with_good_and_bad function multiple times, 
    once for each column in letter_columns. it gets the data to wotk with, the list of column that
    in a loop will plot them using the plotting_with_good_and_bad function, and the good/bad range
    to place in the plotting_with_good_and_bad function.
    '''
    #looping through each column name and creating a separate plot for each one
    for letter_column in letter_columns:
        #generating a title specific to the column
        title = f"{letter_column}: Distribution - Good (1-2) vs Bad (3-5)"

        # Calling the plotting_with_good_and_bad function and operating it
        plotting_with_good_and_bad(
            df=df,
            letter_column=letter_column,
            title=title,
            xlabel=letter_column,
            ylabel="Count",
            good_range=good_range,
            bad_range=bad_range
        )

def plot_lobe_distribution_per_pathology(df, pathology_column, lobe_column):
    '''
    This function, will generate pie charts showing the distribution of lobes for each pathology.
    it will gett the data to work with and two column names using the sceond one to show the distribuition
    of it for each value in the first column (for our purpose they will be pathology column and lobe column)
    '''
    # Using the get_unique_cell_values_with_nan function to get the unique pathologies
    unique_pathologies = get_unique_cell_values_with_nan(df, pathology_column)

    # Creating a loop for ploting a pie chart for each pathology
    for pathology in unique_pathologies:
        if pd.isna(pathology):  #Skipping the NaN values
            continue

        # Filtering the data to only include rows where df[pathology_column] == pathology
        filtered_data = df[df[pathology_column] == pathology]

        # Counting the occurrences of each lobe
        lobe_counts = filtered_data[lobe_column].value_counts()

        # Generating the pie chart
        plt.figure(figsize=(6, 6))
        plt.pie(
            lobe_counts, #the count for each lobe
            labels=lobe_counts.index, #displays lobes as labels
            autopct='%1.1f%%', #Showing percentage values on each slice
            colors=["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"],  #Assigning custom colors for each one
        )
        plt.title(f"Lobe Distribution for Pathology: {pathology}") #Setting the title of the chart
        plt.show() #Displaing the pie chart

def visualize_binomial_p_values(results, title="P-Values from Binomial Test"):
    """
    this function makes visualizes p-values from a binomial test using a scatter plot. the parameters are:
    results (list of dict): A list of dictionaries containing analysis results, each dictionary should have:
        - "column" (str) - The category name.
        - "P-value" (float) - The p-value from the binomial test.
        - "Significant" (bool) - Whether the result is statistically significant.
    - title (str, optional) - The title of the plot. Default is "P-Values from Binomial Test".
    the function does not have returns just prints a scatter plot
    """
    #checking if the list is empty and returning a message
    if not results:
        print("No significant results to visualize.")
        return #exit the function early

    #extract data for visualization
    categories = [str(res["column"]) for res in results]  # Convert to strings
    p_values = [res["P-value"] for res in results]
    significance = ["red" if res["Significant"] else "blue" for res in results]

    # Debugging output
    print("Categories:", categories)
    print("P-values:", p_values)

    # Plot p-values
    plt.figure(figsize=(12, 6))
    plt.scatter(categories, p_values, color=significance, s=100, label="P-value")

    #Highlight significance threshold
    plt.axhline(y=0.05, color="orange", linestyle="--", label="Significance Threshold (p=0.05)")

    #settings
    plt.title(title, fontsize=16)
    plt.xlabel("Categories", fontsize=12)
    plt.ylabel("P-value", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.ylim(0, 1)  # P-values range from 0 to 1
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()

def plot_general_analyze_results_all(df, columns):
    """
    this function runs significance analysis on multiple columns and plots the p-values from the
    binomial test. the parameters are: df - the input DataFrame containing the data, columns (list) -
    a list of column names (categorical columns) to analyze. hte function does not return anything, 
    just prints plot.
    """
    list_columns = ["ILAE_Year1", "ILAE_Year2", "ILAE_Year3", "ILAE_Year4", "ILAE_Year5"]

    for column in columns:

        #calculate "good" and "bad" counts
        good_count = count_by_range(df, list_columns, column, 1, 2)
        bad_count = count_by_range(df, list_columns, column, 3, 5)

        #perform the analysis
        results  = analyze_column_significant_only(good_count, bad_count, column,2)

        #if there are results, plot them
        if results:
            #prepare data for visualization
            categories = [str(res["column"]) for res in results]
            p_values = [res["P-value"] for res in results]
            significance = ["red" if res["P-value"] < 0.05 else "blue" for res in results]

            #Plot all p-values
            plt.figure(figsize=(12, 6))
            plt.scatter(categories, p_values, color=significance, s=100, label="P-value")

            #Highlight significance threshold
            plt.axhline(y=0.05, color="orange", linestyle="--", label="Significance Threshold (p=0.05)")

            #settings
            plt.title(f"P-Values for {column}", fontsize=16)
            plt.xlabel("Categories", fontsize=12)
            plt.ylabel("P-value", fontsize=12)
            plt.xticks(rotation=45, ha="right")
            plt.ylim(0, 1)  # P-values range from 0 to 1
            plt.legend()
            plt.grid(axis="y", linestyle="--", alpha=0.7)

            plt.tight_layout()
            plt.show()
        else:
            print(f"No results to plot for column: {column}")





