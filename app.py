import streamlit as st
import pandas as pd
import plotly.express as px
import openai
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.badges import badge

# Set page configuration
st.set_page_config(page_title="Social Media Analyzer with GPT", page_icon="\ud83d\udcca", layout="wide")

# Data validation function
def validate_data(df):
    required_columns = ["post_id", "post_type", "likes", "shares", "comments", "avg_sentiment_score"]
    if not all(col in df.columns for col in required_columns):
        raise ValueError("Missing required columns in data")
    if df.isnull().values.any():
        st.warning("Data contains null values")

# Predefined Q&A
Frequently_asked_questions = {
    "What is the post type with the highest total engagement?": "Reels have the highest total engagement, as they generally receive more likes, shares, and comments compared to other post types.",
    "Which post type has the highest average engagement rate?": "Based on the data, static images have the highest average engagement rate because of their strong performance in shares and comments relative to likes.",
    "What is the sentiment trend in the data?": "The sentiment trend shows a mix of positive and negative sentiment. Posts like static images and carousels tend to have neutral to positive sentiments, while some reels have a slightly negative sentiment score.",
    "How do reels compare to static images in terms of virality?": "Reels have a higher virality score compared to static images, as they receive more shares and comments relative to likes.",
    "What is the average engagement rate for all posts?": "The average engagement rate across all posts is approximately 130.1%, indicating strong interactions relative to likes.",
    "Which post had the lowest sentiment score, and why?": "Post ID 3 (a reel) had the lowest sentiment score of -0.7, possibly due to negative comments or audience reactions.",
    "What is the relationship between post type and sentiment score?": "Static images and carousels generally have more neutral or slightly positive sentiment scores, while reels show a wider range, including negative scores.",
    "Which metric is most critical for determining post virality?": "Shares are the most critical metric for determining virality, as they are weighted more heavily in the virality score formula.",
    "How many posts have a positive sentiment score?": "Based on the data, 3 out of 5 posts have a positive sentiment score (above 0).",
    "What is the most common post type in the dataset?": "Reels are the most common post type, making up the majority of the dataset."
}

# GPT analysis function
def ask_gpt(query, data_summary):
    try:
        openai.api_key = "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"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a data analyst."},
                {"role": "user", "content": f"Here is the social media data summary: {data_summary}. {query}"}
            ]
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        st.error(f"Error in GPT analysis: {str(e)}")
        return None

# Cache data loading
@st.cache_data
def load_data():
    return pd.DataFrame([
        [1, "reel", 148, 49, 13, 0.45],
        [2, "reel", 338, 63, 44, -0.41],
        [3, "reel", 392, 26, 17, -0.7],
        [4, "static_image", 238, 98, 136, 0.19],
        [5, "carousel", 120, 34, 10, 0.30],
    ], columns=["post_id", "post_type", "likes", "shares", "comments", "avg_sentiment_score"])

# Main app
try:
    # Load and validate data
    data = load_data()
    validate_data(data)

    # Calculate metrics
    data["total_engagement"] = data["likes"] + data["shares"] + data["comments"]
    data["engagement_rate"] = data["total_engagement"] / data["likes"] * 100
    data["virality_score"] = (data["shares"] * 2 + data["comments"]) / data["likes"] * 100

    # UI Elements
    st.title("\ud83d\udcf1 Social Media Analyzer with GPT")
    badge("github", "https://github.com/Harsh-from-teenShikari/social")
    add_vertical_space(2)

    # Sidebar filters
    st.sidebar.header("\ud83d\udcca Filter Options")
    post_types = st.sidebar.multiselect(
        "Select Post Types",
        options=data["post_type"].unique(),
        default=data["post_type"].unique()
    )

    # Filter data
    filtered_data = data[data["post_type"].isin(post_types)]

    # Metrics
    if not filtered_data.empty:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("\ud83d\udcdd Total Posts", len(filtered_data))
        with col2:
            st.metric("\ud83d\udcca Avg. Engagement", f"{filtered_data['total_engagement'].mean():.0f}")
        with col3:
            st.metric("\ud83d\udcc8 Engagement Rate", f"{filtered_data['engagement_rate'].mean():.1f}%")
        with col4:
            st.metric("\ud83d\ude0a Avg. Sentiment", f"{filtered_data['avg_sentiment_score'].mean():.2f}")

        # Visualizations
        st.header("\ud83d\udcca Visual Analytics")
        fig = px.bar(filtered_data, x="post_type", y="total_engagement",
                    color="post_type", title="Total Engagement by Post Type",
                    template="plotly_white")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        # Predefined Q&A Section
        st.header("\ud83d\udcd6 Frequent Insights")
        for question, answer in Frequently_asked_questions.items():
            with st.expander(question):
                st.write(answer)

        # GPT Section
        st.header("\ud83d\udcac Ask the Data Analyst (Powered by GPT)")
        data_summary = filtered_data.describe().to_string()

        col1, col2 = st.columns([4, 1])
        with col1:
            query = st.text_input("Ask a question about the data:")
        with col2:
            if st.button("Analyze"):
                if query:
                    with st.spinner("Analyzing..."):
                        answer = ask_gpt(query, data_summary)
                        if answer:
                            st.markdown(f"### \ud83e\udd16 Answer: {answer}")
                else:
                    st.warning("Please enter a question.")
    else:
        st.warning("No data available for the selected filters.")

except Exception as e:
    st.error(f"An error occurred: {str(e)}")
