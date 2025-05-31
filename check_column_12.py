import pandas as pd

# Read the Gender dataframe
Gender = pd.read_excel('HDFC_modified.xlsx', sheet_name='Gender')

# Print info about the 12th column (index 11)
print("12th column (index 11):", Gender.columns[11])
print("\nData for this column:")
print(Gender[['Category', Gender.columns[11]]].head())

# Print additional information about column type and values
print("\nColumn data type:", Gender[Gender.columns[11]].dtype)
print("Min value:", Gender[Gender.columns[11]].min())
print("Max value:", Gender[Gender.columns[11]].max())
print("Mean value:", Gender[Gender.columns[11]].mean())
