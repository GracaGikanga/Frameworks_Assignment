import streamlit as st
from initial import plot_publications
from initial import word_cloud
from initial import top_publications
from initial import plot_papers_by_source

#Show publications Graph
#Streamlit title
st.title("Publications")
#Streamlit description
st.write(
    "This chart shows the number of publications over time." 
    " It helps visualize trends in research activity."
)
#Show the plot
fig, sample_df = plot_publications()
st.pyplot(fig)
#Show sample data
st.write("Sample data")
st.dataframe(sample_df)

#Show WordCloud Graph
#Steamlit title
st.title("Word Cloud")
#Steamlit description
st.write(
    "This shows the most common words used in titles as a word cloud."
   "It helps visualize prevalent themes and topics in the research papers."
)
#Show the plot
fig = word_cloud()  
st.pyplot(fig)

#Top Journals Graph
#Streamlit title
st.title("Top Journals")
#Streamlit description
st.write(
    "This chart shows the top journals ranked by the number of papers published "
    "in the dataset. It helps identify which journals contribute the most publications."
)
#Show the plot and
fig, sample_df = top_publications()
st.pyplot(fig)

# Streamlit app for Papers by Source
#Streamlit titile
st.title("Paper Distribution by Source")
#Streamlit description
st.write(
    "This chart shows the distribution of Published papers and their relevant sources. I helps "
    "to identify the source of most publications."
)
#Call the function and display the plot and sample data
fig, sample_df= plot_papers_by_source()
st.pyplot(fig)
#Show sample data
st.write("Sample data")
st.dataframe(sample_df)
