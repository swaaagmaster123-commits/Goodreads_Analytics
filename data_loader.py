import streamlit as st
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"


@st.cache_data
def load_data():

    books = pd.read_csv(DATA_DIR / "books.csv")
    ratings = pd.read_csv(DATA_DIR / "ratings.csv")
    tags = pd.read_csv(DATA_DIR / "tags.csv")
    book_tags = pd.read_csv(DATA_DIR / "book_tags.csv")
    to_read = pd.read_csv(DATA_DIR / "to_read.csv")

    # Prepare books
    books["title"] = books["title"].fillna("Unknown")
    books["authors"] = books["authors"].fillna("Unknown")

    books["average_rating"] = pd.to_numeric(
        books["average_rating"], errors="coerce"
    )

    books["ratings_count"] = pd.to_numeric(
        books["ratings_count"], errors="coerce"
    ).fillna(0)

    books["original_publication_year"] = pd.to_numeric(
        books["original_publication_year"], errors="coerce"
    )

    # Prepare ratings
    ratings["rating"] = pd.to_numeric(
        ratings["rating"], errors="coerce"
    )

    # Prepare book tags
    book_tags["count"] = pd.to_numeric(
        book_tags["count"], errors="coerce"
    ).fillna(0)

    return books, ratings, tags, book_tags, to_read