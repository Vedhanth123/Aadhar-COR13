import pandas as pd

# Read the Gender dataframe
Gender = pd.read_excel('HDFC_modified.xlsx', sheet_name='Gender')

# Print basic information about the dataframe
print(f"Gender dataframe shape: {Gender.shape}")
print(f"Gender columns: {list(Gender.columns)}")

# Print the first row of data
print("\nFirst row data:")
print(Gender.iloc[0].to_dict())
