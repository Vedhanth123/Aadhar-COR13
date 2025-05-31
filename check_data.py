import pandas as pd
pd.set_option('display.max_columns', None)

# Read the Gender dataframe
Gender = pd.read_excel('HDFC_modified.xlsx', sheet_name='Gender')

# Print simplified information
print("Gender dataframe shape:", Gender.shape)
print("\nFirst two columns of the Gender dataframe:")
print(Gender.iloc[:, :2])
