import pandas as pd

# Read the Gender dataframe
Gender = pd.read_excel('HDFC_modified.xlsx', sheet_name='Gender')

# Print info about the 7th and 11th columns
print("7th column (index 6):", Gender.columns[6])
print("11th column (index 10):", Gender.columns[10])

# Print the first few rows of these columns
print("\nFirst rows data of columns 7 and 11:")
cols = [Gender.columns[0], Gender.columns[6], Gender.columns[10]]
print(Gender[cols].head())
