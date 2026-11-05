import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Configuration
st.set_page_config(
    page_title="Goodreads Analytics",
    page_icon="📚",
    layout="wide"
)

# Data folder
DATA_DIR = Path(__file__).parent / "data"

# Load CSV files
@st.cache_data
def load_data():

    books = pd.read_csv(DATA_DIR / "books.csv")
    ratings = pd.read_csv(DATA_DIR / "ratings.csv")
    tags = pd.read_csv(DATA_DIR / "tags.csv")
    book_tags = pd.read_csv(DATA_DIR / "book_tags.csv")
    to_read = pd.read_csv(DATA_DIR / "to_read.csv")

    return books, ratings, tags, book_tags, to_read


# Check data
try:
    books, ratings, tags, book_tags, to_read = load_data()

except Exception as e:

    st.error("Error loading CSV files")

    st.write("Please check the data folder.")

    st.code(str(e))

    st.stop()


# Prepare data
books["title"] = books["title"].fillna("Unknown")

books["authors"] = books["authors"].fillna("Unknown")

books["average_rating"] = pd.to_numeric(
    books["average_rating"], errors="coerce"
)

books["ratings_count"] = pd.to_numeric(
    books["ratings_count"], errors="coerce"
).fillna(0)

ratings["rating"] = pd.to_numeric(
    ratings["rating"], errors="coerce"
)

books["original_publication_year"] = pd.to_numeric(
    books["original_publication_year"], errors="coerce"
)


# General statistics
total_books = books["id"].nunique()

total_users = ratings["user_id"].nunique()

total_ratings = len(ratings)

average_rating = ratings["rating"].mean()


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


# Main title
st.title("📚 Goodreads Analytics")

st.caption("Discover, Analyze and Explore Books")

st.divider()


# ==========================================
# PAGE 1 : OVERVIEW
# ==========================================

if page == "Overview":

    st.header("General Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Books",
        f"{total_books:,}"
    )

    col2.metric(
        "Total Users",
        f"{total_users:,}"
    )

    col3.metric(
        "Total Ratings",
        f"{total_ratings:,}"
    )

    col4.metric(
        "Average Rating",
        f"{average_rating:.2f} / 5"
    )

    st.divider()

    left, right = st.columns(2)

    with left:

        st.subheader("Top 10 Highest Rated Books")

        popular = books[
            books["ratings_count"] >= 1000
        ]

        top_books = popular.nlargest(
            10, "average_rating"
        )

        fig = px.bar(
            top_books,
            x="average_rating",
            y="title",
            orientation="h",
            title="Top Rated Books",
            labels={
                "average_rating": "Average Rating",
                "title": "Book"
            }
        )

        fig.update_layout(
            yaxis={"categoryorder": "total ascending"}
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        st.subheader("Books by Publication Year")

        years = books.dropna(
            subset=["original_publication_year"]
        )

        years = years[
            (years["original_publication_year"] >= 1900) &
            (years["original_publication_year"] <= 2020)
        ]

        year_count = (
            years.groupby("original_publication_year")
            .size()
            .reset_index(name="Number of Books")
        )

        fig = px.line(
            year_count,
            x="original_publication_year",
            y="Number of Books",
            title="Publication Trend"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader("Most Rated Books")

    most_rated = books.nlargest(
        10, "ratings_count"
    )

    st.dataframe(
        most_rated[
            [
                "title",
                "authors",
                "average_rating",
                "ratings_count"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


# ==========================================
# PAGE 2 : EXPLORE BOOKS
# ==========================================

elif page == "Explore Books":

    st.header("🔎 Explore Books")

    search = st.text_input(
        "Search by title or author",
        placeholder="Enter book title or author..."
    )

    min_rating = st.slider(
        "Minimum Average Rating",
        min_value=0.0,
        max_value=5.0,
        value=0.0,
        step=0.1
    )

    filtered = books[
        books["average_rating"].fillna(0) >= min_rating
    ]

    if search:

        filtered = filtered[
            filtered["title"].str.contains(
                search,
                case=False,
                na=False
            )
            |
            filtered["authors"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

    st.write(
        f"Results found: {len(filtered):,}"
    )

    st.dataframe(
        filtered[
            [
                "title",
                "authors",
                "original_publication_year",
                "average_rating",
                "ratings_count"
            ]
        ].head(200),
        use_container_width=True,
        hide_index=True
    )

    st.caption("Maximum 200 results displayed.")


# ==========================================
# PAGE 3 : RATINGS ANALYSIS
# ==========================================

elif page == "Ratings Analysis":

    st.header("⭐ Ratings Analysis")

    rating_counts = (
        ratings["rating"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    rating_counts.columns = [
        "Rating",
        "Number of Ratings"
    ]

    fig = px.bar(
        rating_counts,
        x="Rating",
        y="Number of Ratings",
        title="Distribution of Ratings",
        text="Number of Ratings"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Average User Rating",
            f"{ratings['rating'].mean():.2f} / 5"
        )

    with col2:

        st.metric(
            "Unique Users",
            f"{ratings['user_id'].nunique():,}"
        )

    st.subheader("Ratings Details")

    st.dataframe(
        rating_counts,
        use_container_width=True,
        hide_index=True
    )


# ==========================================
# PAGE 4 : GENRES AND AUTHORS
# ==========================================

elif page == "Genres & Authors":

    st.header("🏷️ Genres & Authors Analysis")

    st.subheader("Most Popular Tags")

    popular_tags = book_tags.merge(
        tags,
        on="tag_id",
        how="left"
    )

    popular_tags = (
        popular_tags.groupby("tag_name")["count"]
        .sum()
        .sort_values(ascending=False)
        .head(15)
        .reset_index()
    )

    fig = px.bar(
        popular_tags,
        x="count",
        y="tag_name",
        orientation="h",
        title="Top 15 Popular Tags"
    )

    fig.update_layout(
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    st.subheader("Top Authors")

    author_counts = (
        books["authors"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    author_counts.columns = [
        "Author",
        "Number of Books"
    ]

    fig = px.bar(
        author_counts,
        x="Number of Books",
        y="Author",
        orientation="h",
        title="Top 10 Authors"
    )

    fig.update_layout(
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    st.subheader("Explore a Genre")

    tag_list = sorted(
        tags["tag_name"].dropna().unique().tolist()
    )

    selected_tag = st.selectbox(
        "Choose a genre or tag",
        tag_list
    )

    tag_id = tags.loc[
        tags["tag_name"] == selected_tag,
        "tag_id"
    ].iloc[0]

    selected_books = book_tags[
        book_tags["tag_id"] == tag_id
    ]

    selected_books = selected_books.merge(
        books,
        left_on="goodreads_book_id",
        right_on="id",
        how="inner"
    )

    selected_books = selected_books.sort_values(
        "count",
        ascending=False
    )

    st.dataframe(
        selected_books[
            [
                "title",
                "authors",
                "average_rating",
                "count"
            ]
        ].head(20),
        use_container_width=True,
        hide_index=True
    )


# ==========================================
# PAGE 5 : RECOMMENDATIONS
# ==========================================

elif page == "Recommendations":

    st.header("💡 Book Recommendations")

    st.write(
        "Choose a book and discover similar books."
    )

    book_options = books[
        ["id", "title"]
    ].drop_duplicates()

    selected_book = st.selectbox(
        "Choose a book",
        book_options["title"].tolist()
    )

    selected_id = book_options.loc[
        book_options["title"] == selected_book,
        "id"
    ].iloc[0]

    selected_tags = book_tags[
        book_tags["goodreads_book_id"] == selected_id
    ]

    if selected_tags.empty:

        st.warning(
            "No tags available for this book."
        )

    else:

        common_tags = selected_tags.nlargest(
            10,
            "count"
        )["tag_id"].tolist()

        similar = book_tags[
            book_tags["tag_id"].isin(common_tags)
        ]

        recommendations = (
            similar.groupby("goodreads_book_id")["count"]
            .sum()
            .reset_index()
        )

        recommendations = recommendations[
            recommendations["goodreads_book_id"] != selected_id
        ]

        recommendations = recommendations.nlargest(
            10,
            "count"
        )

        recommendations = recommendations.merge(
            books,
            left_on="goodreads_book_id",
            right_on="id",
            how="inner"
        )

        st.subheader("Recommended Books")

        st.dataframe(
            recommendations[
                [
                    "title",
                    "authors",
                    "average_rating",
                    "count"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    st.info(
        "Recommendations are based on shared tags."
    )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "Goodreads Analytics | Python | Streamlit | Pandas | Plotly"
)