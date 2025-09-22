# Load the data
import pandas as pd
df = pd.read_csv('metadata.csv')

# Basic info
print(df.shape)
print(df.info())
print(df.dtypes)


# Check missing values
print(df.isnull().sum())

