import streamlit as st

from data_loader import load_data

from overview import render as render_overview
from explore_books import render as render_explore
from ratings_analysis import render as render_ratings
from genres_authors import render as render_genres
from recommendations import render as render_recommendations


# Configuration
st.set_page_config(
    page_title="Goodreads Analytics",
    page_icon="📚",
    layout="wide"
)


# Load Data
try:

    books, ratings, tags, book_tags, to_read = load_data()

except Exception as e:

    st.error("Error loading CSV files")
    st.write("Please check the data folder.")
    st.code(str(e))
    st.stop()


# Sidebar
st.sidebar.title("📚 Goodreads Analytics")

st.sidebar.write("Book Data Analysis Platform")

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Explore Books",
        "Ratings Analysis",
        "Genres & Authors",
        "Recommendations"
    ]
)


# Main Title
st.title("📚 Goodreads Analytics")

st.caption("Discover, Analyze and Explore Books")

st.divider()


# Navigation
if page == "Overview":

    render_overview(books, ratings)


elif page == "Explore Books":

    render_explore(books)


elif page == "Ratings Analysis":

    render_ratings(ratings)


elif page == "Genres & Authors":

    render_genres(books, tags, book_tags)


elif page == "Recommendations":

    render_recommendations(books, book_tags)


# Footer
st.divider()

st.caption(
    "Goodreads Analytics | Python | Streamlit | Pandas | Plotly"
)