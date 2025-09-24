# Load the data
import pandas as pd
from pandas.core.interchange.dataframe_protocol import Column

try: 
    # load into pandas
    df = pd.read_csv('metadata.csv', nrows=100)
# save the subset to a new file

 
    df.to_csv ('first_100.csv',index=False)
    #Print 10 rows
    print('metadata columns',df.columns)
    #Print first 5 rows
    print('first 5 rows:',df.iloc[: ,:5])
    #Check df dimensions
    print('Dimensions:\n',df.shape)
    #Identify data types of each column
    print('Data types for each column:\n',df.dtypes)

    # Generate basic statistics for numerical columns
    print('Basic statistics:\n',df.describe)

     # Part 2
    # Check missing values
    missing_count = df.isnull().sum()
    print('Missing values per column:\n',missing_count)
    
    # --- Fill numeric columns ---
    num_cols = df.select_dtypes(include=["number"]).columns
    df[num_cols] = df[num_cols].fillna(0)
    print("Filled numeric columns with 0:\n", df[num_cols], "\n")

    # --- Fill non-numeric columns ---
    non_num_cols = df.select_dtypes(exclude=["number"]).columns
    df[non_num_cols] = df[non_num_cols].fillna("none")
    print("Filled non-numeric columns with 'none':\n", df[non_num_cols], "\n")

    #Drop duplicates
    df.drop_duplicates(inplace=True)

        #Save to data to a new file
    df.to_csv('New_data.csv', index=False)
    print('Success!Data cleaned and saved')

    #Prepare Data for Analysis
    #Filter date columns
    #converting objects to datatypes

    # Converting all columns to datetime
    for col in df.columns:
        try:
            df[col] = pd.to_datetime(df[col])
        except (ValueError, TypeError):
            pass

    # Now extract datetime columns
    date_columns_df = df.select_dtypes(include=['datetime64[ns]'])
    print("\n📅 Columns detected as datetime:\n", date_columns_df)

    # Create a new DataFrame with just the years
    year_columns = date_columns_df.apply(lambda x: x.dt.year)
    print("\n📅 Extracted years:\n", year_columns)

    # Part 3: Data Analysis and Visualization
    # Perform Basuc Analysis
    # Convert publish_time to datetime
    #add a year Column
    #df["pub_year"] = pd.to_datetime(df["publish_time"], errors="coerce").dt.year

    df["publish_time"] = pd.to_datetime(df["publish_time"], errors="coerce")

    # Extract the year
    df["pub_year"] = df["publish_time"].dt.year

    # Count papers per year
    papers_per_year = df["pub_year"].value_counts().sort_index()
    print("📊 Papers per year:\n", papers_per_year)

    #identifying top journal publications
    import pandas as pd

    # Count how many papers per journal
    journal_counts = df["journal"].value_counts()

    # Show the top 10 journals
    print("📊 Top 10 journals by number of papers:\n", journal_counts.head(5))

    
except FileNotFoundError:
    print("File not found. Please check the file path.")
except pd.errors.EmptyDataError:
    print("The file is empty.")
except pd.errors.ParserError:
    print("The file could not be parsed as CSV.")

