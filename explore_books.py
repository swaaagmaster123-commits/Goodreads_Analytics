import streamlit as st


def render(books):

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

    st.write(f"Results found: {len(filtered):,}")

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