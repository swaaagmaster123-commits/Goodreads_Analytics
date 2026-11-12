import streamlit as st
import plotly.express as px


def render(ratings):

    st.header("⭐ Ratings Analysis")

    rating_counts = (
        ratings["rating"]
        .dropna()
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