import streamlit as st
import plotly.express as px


def render(books, ratings):

    st.header("General Overview")

    total_books = books["id"].nunique()
    total_users = ratings["user_id"].nunique()
    total_ratings = len(ratings)
    average_rating = ratings["rating"].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Books", f"{total_books:,}")
    col2.metric("Total Users", f"{total_users:,}")
    col3.metric("Total Ratings", f"{total_ratings:,}")
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