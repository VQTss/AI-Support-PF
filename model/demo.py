import pandas as pd
from openpyxl import Workbook
# Load the CSV file
file_path = './data/CrispConvoTracking - Sheet13 (1).csv'
df = pd.read_csv(file_path)

# Define a mock API function that analyzes the content and returns a structured JSON-like format
def api_analytics(content):
    # This is a placeholder function. In a real-world scenario, this function would make an API call
    # to an external service which performs the analysis and returns the structured data.
    return {
        "Bug": "The form background is not becoming transparent as expected, even after applying custom CSS code.",
        "Feature": "The ability to add custom CSS code to the form in Omnisend through PageFly.",
        "UX/UI": "The user is requesting help with changing the background image of the left column and adding a newsletter form on the right page, as well as making the header and footer not appear on the password page. Additionally, the user is seeking assistance with making the form background transparent for better user experience."
    }

# Apply the mock API function to the 'Content' column
# Note: In a real-world scenario, you would replace this with actual API calls
analyzed_content = df['Content'].apply(api_analytics)


# print(analyzed_content.head())


# Convert the results to a DataFrame
analyzed_df = pd.DataFrame(analyzed_content.tolist())

print("Analyzed DataFrame Head:", analyzed_df.head())

# Combining the analyzed content with the original DataFrame
df_combined = pd.concat([df, analyzed_df], axis=1)
# print("Combined DataFrame Columns:", df_combined.columns)

# # Selecting and renaming the required columns for the new Excel file
# output_columns = ['Ticket URL', 'Bug', 'Feature', 'UX/UI']
# output_df = df_combined[output_columns].copy()
# output_df.insert(0, 'No.', range(1, 1 + len(output_df)))

# # Save the output dataframe to an Excel file
# output_file_path = './result/analyzed_content.xlsx'
# output_df.to_excel(output_file_path, index=False)

# output_file_path
