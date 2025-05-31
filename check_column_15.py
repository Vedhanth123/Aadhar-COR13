import pandas as pd

# Read the Gender dataframe
Gender = pd.read_excel('HDFC_modified.xlsx', sheet_name='Gender')

# Print info about the 15th column (index 14)
if len(Gender.columns) > 14:
    print("15th column (index 14):", Gender.columns[14])
    print("\nData for this column:")
    print(Gender[['Category', Gender.columns[14]]].head())
    
    # Print additional information about column type and values
    print("\nColumn data type:", Gender[Gender.columns[14]].dtype)
    print("Min value:", Gender[Gender.columns[14]].min())
    print("Max value:", Gender[Gender.columns[14]].max())
    print("Mean value:", Gender[Gender.columns[14]].mean())
else:
    print(f"There are only {len(Gender.columns)} columns in the dataframe. Can't access column 15.")
    print("Available columns:")
    for i, col in enumerate(Gender.columns):
        print(f"{i}: {col}")
