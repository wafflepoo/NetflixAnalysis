import streamlit as st
import pandas as pd
import itertools

# --------------------------------------------------
# Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Netflix Data Analysis",
    layout="wide"
)

# --------------------------------------------------
# Title & Introduction
# --------------------------------------------------
st.title("Netflix Data Analysis Dashboard")
st.markdown(
    """
    This interactive dashboard explores Netflix content trends using the Netflix Titles dataset.
    It highlights key KPIs, temporal patterns, and cast insights in a clear and recruiter-friendly way.
    """
)

st.markdown("---")

# --------------------------------------------------
# Load & Prepare Data
# --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/netflix_titles.csv")

    # Date cleaning
    df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
    df["year_added"] = df["date_added"].dt.year
    df["month_added"] = df["date_added"].dt.month

    # Title length
    df["title_length"] = df["title"].str.len()

    return df


df = load_data()

# --------------------------------------------------
# KPIs SECTION
# --------------------------------------------------
st.subheader("Key Metrics")

most_popular_year = int(df["year_added"].value_counts().idxmax())
most_popular_month = int(df["month_added"].value_counts().idxmax())
longest_title = df.loc[df["title_length"].idxmax(), "title"]

# Actor processing
cast = df["cast"].dropna().str.split(", ")
all_actors = list(itertools.chain.from_iterable(cast))
actor_counts = pd.Series(all_actors).value_counts()
most_common_actor = actor_counts.idxmax()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Peak Year", most_popular_year)
col2.metric("Peak Month", most_popular_month)
col3.metric("Longest Title", longest_title)
col4.metric("Top Actor", most_common_actor)

st.markdown("---")

# --------------------------------------------------
# CHARTS SECTION
# --------------------------------------------------
st.subheader("Content Trends Over Time")

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("Content Added per Year")
    year_counts = df["year_added"].value_counts().sort_index()
    st.bar_chart(year_counts)

with col_right:
    st.markdown("Content Added per Month")
    month_counts = df["month_added"].value_counts().sort_index()
    st.line_chart(month_counts)

st.markdown("---")

# --------------------------------------------------
# TOP ACTORS SECTION
# --------------------------------------------------
st.subheader("Top 10 Actors on Netflix")

top_actors = actor_counts.head(10)
st.bar_chart(top_actors)

# Export Top Actors
st.markdown("Export Top Actors")

top_actors_df = top_actors.reset_index()
top_actors_df.columns = ["Actor", "Appearances"]

csv_actors = top_actors_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download top actors (CSV)",
    data=csv_actors,
    file_name="netflix_top_actors.csv",
    mime="text/csv",
)

st.markdown("---")

# --------------------------------------------------
# INTERACTIVITY SECTION
# --------------------------------------------------
st.subheader("Interactive Exploration")

col_filter1, col_filter2 = st.columns(2)

with col_filter1:
    content_type = st.selectbox(
        "Select content type",
        df["type"].dropna().unique()
    )

with col_filter2:
    selected_year = st.selectbox(
        "Select year added",
        sorted(df["year_added"].dropna().unique())
    )

filtered_df = df[
    (df["type"] == content_type) &
    (df["year_added"] == selected_year)
]

st.markdown("Filtered Dataset Preview")
st.dataframe(filtered_df.head(10))

# Export filtered dataset
st.markdown("Export Filtered Results")

csv_filtered = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download filtered data (CSV)",
    data=csv_filtered,
    file_name=f"netflix_filtered_{content_type}_{selected_year}.csv",
    mime="text/csv",
)

st.markdown("---")

# --------------------------------------------------
# RAW DATA SECTION
# --------------------------------------------------
st.subheader("Raw Data Preview")

with st.expander("Show raw dataset"):
    st.dataframe(df.head(20))

# Export full dataset
st.markdown("Export Full Dataset")

csv_full = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download full dataset (CSV)",
    data=csv_full,
    file_name="netflix_full_cleaned_dataset.csv",
    mime="text/csv",
)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown(
    """
    ---
    Author: Alissa Missaoui  
    Tools: Python, Pandas, Streamlit  
    Purpose: Demonstrate data analysis, visualization, and dashboarding skills
    """
)
