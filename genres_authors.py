import streamlit as st
import plotly.express as px


def render(books, tags, book_tags):

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

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    st.subheader("Explore a Genre")

    tag_list = sorted(
        tags["tag_name"].dropna().unique().tolist()
    )

    if not tag_list:
        st.warning("No tags available.")
        return

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