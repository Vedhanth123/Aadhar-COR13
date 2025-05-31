import pandas as pd

# Load the Gender dataframe
Gender = pd.read_excel('HDFC_modified.xlsx', sheet_name='Gender')

# Display column names and indices
print("Columns in Gender dataframe:")
for i, col in enumerate(Gender.columns):
    print(f"Index {i}: {col}")

# Check columns 14 and 15 specifically (indices 14 and 15)
print("\nData in columns 14 and 15:")
print(Gender[Gender.columns[14:16]])

# Display basic statistics
print("\nStatistics for Average Residence columns:")
print(Gender[Gender.columns[14:16]].describe())

# Display data types
print("\nData types:")
print(Gender[Gender.columns[14:16]].dtypes)
