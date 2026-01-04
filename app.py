import streamlit as st
import pandas as pd

# Title
st.title("Netflix Data Analysis 🎬📊")

# Load dataset
df = pd.read_csv("data/netflix_titles.csv")

# Show raw data
st.subheader("Dataset Preview")
st.dataframe(df.head(10))

# Most common release year
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df['year_added'] = df['date_added'].dt.year
most_popular_year = df['year_added'].value_counts().idxmax()
st.write(f"Year with most content added: {most_popular_year}")

# Most common month
df['month_added'] = df['date_added'].dt.month
most_popular_month = df['month_added'].value_counts().idxmax()
st.write(f"Month with most content added: {most_popular_month}")

# Movie with longest title
df['title_length'] = df['title'].str.len()
longest_title = df.loc[df['title_length'].idxmax(), 'title']
st.write(f"Movie with the longest title: {longest_title}")

# Actor/actress that appears most
cast = df['cast'].dropna().str.split(', ')
import itertools
all_actors = list(itertools.chain.from_iterable(cast))
actor_counts = pd.Series(all_actors).value_counts()
most_common_actor = actor_counts.idxmax()
st.write(f"Actor/Actress who appears the most: {most_common_actor}")
