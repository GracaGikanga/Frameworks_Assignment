# Load the data
import pandas as pd
import string 
from pandas.core.interchange.dataframe_protocol import Column

try: 
    # load into pandas
    df = pd.read_csv('metadata.csv', nrows=100)

# save the subset to a new file
    df.to_csv ('first_100.csv',index=False)
    #Print first 5 rows
    print('first 5 rows:',df.head(4))
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
    # Look for COVID-related terms in title or abstract
    keywords = "covid|covid-19|coronavirus|sars-cov-2|2019-ncov|ncov"

    covid_mask = (
    df["title"].str.contains(keywords, case=False, na=False) |
    df["abstract"].str.contains(keywords, case=False, na=False) |
    df["journal"].str.contains(keywords, case=False, na=False) |
    df["source_x"].str.contains(keywords, case=False, na=False)
)

    covid_papers = df[covid_mask]

    covid_journals = covid_papers["journal"].value_counts()
    print("📊 Top journals publishing COVID-19 research:\n", covid_journals.head(5))


    # Convert publish_time to datetime
    df["publish_time"] = pd.to_datetime(df["publish_time"], errors="coerce")

    covid_era_papers = df[df["publish_time"].dt.year >= 2020]

    # Count top journals in this period
    journals_2020 = covid_era_papers["journal"].value_counts().head(10)
    print("\n📊 Top journals (2020 onwards):\n", journals_2020)

    # Filter papers published from 2020 onwards
    covid_era_papers = df[df["publish_time"].dt.year >= 2020]
    
    #FFREQUENTLY USED WORDS IN TITLES
    # Take titles, drop missing ones
    titles = df["title"].dropna().str.lower()

    # Remove punctuation
    titles = titles.str.replace(f"[{string.punctuation}]", "", regex=True)

    #Define Stopwords
    stop_words = {"and", "of", "the", "in", "on", "for", "with", "using", "to", "a", "an","on","from","using","by"}

    words = []
    for title in titles:
        for word in title.split():
            if word not in stop_words:
                words.append(word)
    
    # Count word frequencies
    word_counts = pd.Series(words).value_counts()

    print("📊 Most frequent words in titles:\n", word_counts.head(20))



except FileNotFoundError:
    print("File not found. Please check the file path.")
except pd.errors.EmptyDataError:
    print("The file is empty.")
except pd.errors.ParserError:
    print("The file could not be parsed as CSV.")