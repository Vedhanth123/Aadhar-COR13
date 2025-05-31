import pandas as pd

# Load the Gender dataframe
Gender = pd.read_excel('HDFC_modified.xlsx', sheet_name='Gender')

# Display the full Gender dataframe
print("Gender dataframe full content:")
print(Gender)

# Check the Category values to understand what the rows represent
print("\nUnique values in the Category column:")
print(Gender['Category'].unique())
