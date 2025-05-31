import pandas as pd

# Read the Gender dataframe
Gender = pd.read_excel('HDFC_modified.xlsx', sheet_name='Gender')

# Print info about the 5th, 6th, 9th, and 10th columns
print("5th column (index 4):", Gender.columns[4])
print("6th column (index 5):", Gender.columns[5])
print("9th column (index 8):", Gender.columns[8])
print("10th column (index 9):", Gender.columns[9])

# Print the first few rows of these columns
print("\nFirst rows data of these columns:")
cols = [Gender.columns[0], Gender.columns[4], Gender.columns[5], Gender.columns[8], Gender.columns[9]]
print(Gender[cols].head())
