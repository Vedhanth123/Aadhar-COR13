import pandas as pd

# Read the Gender dataframe
Gender = pd.read_excel('HDFC_modified.xlsx', sheet_name='Gender')

# Print info about the 13th column (index 12)
if len(Gender.columns) > 12:
    print("13th column (index 12):", Gender.columns[12])
    print("\nData for this column:")
    print(Gender[['Category', Gender.columns[12]]].head())
    
    # Print additional information about column type and values
    print("\nColumn data type:", Gender[Gender.columns[12]].dtype)
    print("Min value:", Gender[Gender.columns[12]].min())
    print("Max value:", Gender[Gender.columns[12]].max())
    print("Mean value:", Gender[Gender.columns[12]].mean())
else:
    print(f"There are only {len(Gender.columns)} columns in the dataframe. Can't access column 13.")
    print("Available columns:")
    for i, col in enumerate(Gender.columns):
        print(f"{i}: {col}")
