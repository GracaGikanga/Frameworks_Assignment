# Load the data
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import string 
from wordcloud import WordCloud

try: 
    # load into pandas
    df = pd.read_csv('metadata.csv', nrows= 50000)

# save the subset to a new file
    df.to_csv ('first_50000.csv',index=False)
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
    df.to_csv('First_7000_cleaned.csv',index=False)
    print('Success!Data cleaned and saved')

    #Prepare Data for Analysis
    #Filter date columns
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

    # Filter papers published from 2020 onwards
    covid_era_papers = df[df["publish_time"].dt.year >= 2020]
    print("\n📅 Papers from 2020 onwards:\n", covid_era_papers.shape[0])

    # Drop rows where journal is missing
    covid_era_papers = covid_era_papers.dropna(subset=["journal"])

    # Count top journals in this period
    journals_2020 = covid_era_papers["journal"].value_counts().head(5)
    print("\n📊 Top journals (2020 onwards):\n", journals_2020)

    
    
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

    #CREATE VISUALS
    # Number of publications Over time
    # Plotting Publication over time
    # Plot

    def plot_publications():
        df = pd.read_csv("New_data.csv")

        # Convert publish_time to datetime
        df["publish_time"] = pd.to_datetime(df["publish_time"], errors="coerce")
    
        #Years
        df["pub_year"] = df["publish_time"].dt.year
        #Count papers per year
        papers_per_year = df["pub_year"].value_counts().sort_index()

        fig, ax = plt.subplots(figsize=(8,5))
        ax.plot(papers_per_year.index, papers_per_year.values, marker="o")
        ax.set_xlabel("Year")
        ax.set_ylabel("Papers published")
        ax.set_title("Publications Over Time")
        ax.grid(True)

        return fig

    #Bar Chart On Top Publishing Journals
    def top_publications():
        df = pd.read_csv("First_50000.csv")
        print(df.shape)
        # Drop missing or 'none' journals
        df = df.dropna(subset=["journal"])
        df = df[df["journal"].str.lower() != "none"]

        # --- Get top journals overall ---
        top_journals = df["journal"].value_counts().head(10)

        # --- Plot ---
        fig, ax = plt.subplots(figsize=(10,6))
        top_journals.plot(kind="bar", ax=ax, color="lightcoral", edgecolor="black")

        ax.set_xlabel("Journal")
        ax.set_ylabel("Number of Papers")
        ax.set_title("Top Journals (All Papers)")
        ax.tick_params(axis="x", rotation=45)

        plt.tight_layout()
        return fig


    # Create wordcloud
    def word_cloud():
        df = pd.read_csv("New_data.csv")
        # Prepare titles
        titles = df["title"].dropna().str.lower()
        titles = titles.str.replace(f"[{string.punctuation}]", "", regex=True)

        # Define stopwords
        stop_words = {"and", "of", "the", "in", "on", "for", "with", "using", "to", "a", "an", "from", "by"}

        # Collect words
        words = []
        for title in titles:
            for word in title.split():
                if word not in stop_words:
                    words.append(word)


        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color="white",
            stopwords=stop_words,
            colormap="viridis"  # you can try "plasma", "inferno", "coolwarm", etc.
        ).generate(" ".join(words))  # join list of words into a big string


        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        ax.set_title("WordCloud of Paper Titles", fontsize=16)

        return fig 


        #Plotting distribution of paper counts by source
        #Filtering papers by source
        papers_per_source = df["source_x"].value_counts()
        print("📊 Papers per source:\n", papers_per_source.head(10))

        plt.figure(figsize=(10,6))
        papers_per_source.plot(kind="bar")

        plt.xlabel("Source")
        plt.ylabel("Number of Papers")
        plt.title("Distribution of Papers by Source")
        plt.xticks(rotation=45, ha="right")  # rotate labels for readability
        plt.tight_layout()
        plt.show()


    


except FileNotFoundError:
    print("File not found. Please check the file path.")
except pd.errors.EmptyDataError:
    print("The file is empty.")
except pd.errors.ParserError:
    print("The file could not be parsed as CSV.")