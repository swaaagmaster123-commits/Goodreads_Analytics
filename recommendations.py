import streamlit as st


def render(books, book_tags):

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