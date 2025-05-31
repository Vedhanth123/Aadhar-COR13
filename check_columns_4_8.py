import pandas as pd

# Read the Gender dataframe
Gender = pd.read_excel('HDFC_modified.xlsx', sheet_name='Gender')

# Print info about the 4th and 8th columns
print("4th column (index 3):", Gender.columns[3])
print("8th column (index 7):", Gender.columns[7])

# Print the first few rows of these columns
print("\nFirst rows data of columns 4 and 8:")
cols = [Gender.columns[0], Gender.columns[3], Gender.columns[7]]
print(Gender[cols].head())
