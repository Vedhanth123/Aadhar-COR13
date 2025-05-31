import pandas as pd

# Read the Gender dataframe
Gender = pd.read_excel('HDFC_modified.xlsx', sheet_name='Gender')

# Print info about the 14th column (index 13)
if len(Gender.columns) > 13:
    print("14th column (index 13):", Gender.columns[13])
    print("\nData for this column:")
    print(Gender[['Category', Gender.columns[13]]].head())
    
    # Print additional information about column type and values
    print("\nColumn data type:", Gender[Gender.columns[13]].dtype)
    print("Min value:", Gender[Gender.columns[13]].min())
    print("Max value:", Gender[Gender.columns[13]].max())
    print("Mean value:", Gender[Gender.columns[13]].mean())
else:
    print(f"There are only {len(Gender.columns)} columns in the dataframe. Can't access column 14.")
    print("Available columns:")
    for i, col in enumerate(Gender.columns):
        print(f"{i}: {col}")
