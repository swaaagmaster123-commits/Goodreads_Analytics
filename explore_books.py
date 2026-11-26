import streamlit as st
import pandas as pd


def render(data):

    st.title("📚 Explore Books")
    st.write("Search and discover books from Goodreads.")

    # Get books data
    books = data["books"].copy()

    # Check if data is available
    if books.empty:
        st.warning("No books available.")
        return

    # Convert columns to correct types
    books["average_rating"] = pd.to_numeric(
        books["average_rating"], errors="coerce"
    )

    books["original_publication_year"] = pd.to_numeric(
        books["original_publication_year"], errors="coerce"
    )

    # Search section
    st.subheader("🔎 Search for a book")

    search = st.text_input(
        "Enter book title or author",
        placeholder="Search by title or author..."
    )

    filtered_books = books.copy()

    # Search by title or author
    if search:
        filtered_books = filtered_books[
            filtered_books["title"].fillna("").str.contains(
                search, case=False
            )
            |
            filtered_books["authors"].fillna("").str.contains(
                search, case=False
            )
        ]

    # Language filter
    st.subheader("⚙️ Filters")

    languages = sorted(
        books["language_code"].dropna().unique().tolist()
    )

    selected_languages = st.multiselect(
        "Select language",
        languages
    )

    if selected_languages:
        filtered_books = filtered_books[
            filtered_books["language_code"].isin(selected_languages)
        ]

    # Rating filter
    min_rating = st.slider(
        "Minimum average rating",
        min_value=0.0,
        max_value=5.0,
        value=0.0,
        step=0.5
    )

    filtered_books = filtered_books[
        filtered_books["average_rating"] >= min_rating
    ]

    # Sorting
    sort_option = st.selectbox(
        "Sort books by",
        [
            "Highest rating",
            "Most rated",
            "Publication year",
            "Title"
        ]
    )

    if sort_option == "Highest rating":
        filtered_books = filtered_books.sort_values(
            "average_rating", ascending=False
        )

    elif sort_option == "Most rated":
        filtered_books = filtered_books.sort_values(
            "ratings_count", ascending=False
        )

    elif sort_option == "Publication year":
        filtered_books = filtered_books.sort_values(
            "original_publication_year", ascending=False
        )

    elif sort_option == "Title":
        filtered_books = filtered_books.sort_values(
            "title", ascending=True
        )

    # Results
    st.divider()
    st.subheader("📖 Search Results")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Books found", len(filtered_books))

    with col2:
        if not filtered_books.empty:
            average = filtered_books["average_rating"].mean()
            st.metric(
                "Average rating",
                f"{average:.2f} / 5"
            )
        else:
            st.metric("Average rating", "0")

    if filtered_books.empty:
        st.warning("No books found. Try changing your filters.")
        return

    # Display books
    display_columns = [
        "title",
        "authors",
        "original_publication_year",
        "average_rating",
        "ratings_count",
        "language_code"
    ]

    st.dataframe(
        filtered_books[display_columns],
        use_container_width=True,
        hide_index=True
    )

    # Book details
    st.divider()
    st.subheader("📘 Book Details")

    selected_index = st.selectbox(
        "Choose a book",
        filtered_books.index,
        format_func=lambda x: str(
            filtered_books.loc[x, "title"]
        )
    )

    selected_book = filtered_books.loc[selected_index]

    col1, col2 = st.columns([1, 2])

    with col1:
        image_url = selected_book.get("image_url")

        if pd.notna(image_url) and str(image_url).startswith("http"):
            st.image(image_url, width=200)
        else:
            st.info("No image available.")

    with col2:
        st.markdown(f"### {selected_book['title']}")
        st.write("*Author:*", selected_book["authors"])
        st.write(
            "*Publication year:*",
            selected_book["original_publication_year"]
        )
        st.write(
            "*Average rating:*",
            selected_book["average_rating"]
        )
        st.write(
            "*Number of ratings:*",
            selected_book["ratings_count"]
        )
        st.write(
            "*Language:*",
            selected_book["language_code"]
        )