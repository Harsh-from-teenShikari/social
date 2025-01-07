import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Social Media Analyzer", page_icon="📊", layout="wide")

# Sample dataset
@st.cache_data
def load_data():
    return pd.DataFrame([
        [1, "reel", 148, 49, 13, 0.45],
        [2, "reel", 338, 63, 44, -0.41],
        [3, "reel", 392, 26, 17, -0.7],
        [4, "static_image", 238, 98, 136, 0.19],
        [5, "carousel", 120, 34, 10, 0.30],
    ], columns=["post_id", "post_type", "likes", "shares", "comments", "avg_sentiment_score"])

# Predefined Q&A for interactive analysis
fake_ai_responses = {
    "What is the most popular post type?": "Based on the analysis, the most popular post type is 'Reel' with an average engagement rate of 65%.",
    "How can we improve engagement rates?": "Improving engagement rates can be achieved by posting more Reels and engaging captions. Posts with a higher sentiment score tend to perform better.",
    "What is the overall sentiment of posts?": "The average sentiment score of the dataset is 0.16, indicating a neutral tone overall. However, Reels tend to have more negative sentiment due to controversial topics.",
    "Which posts are most likely to go viral?": "Posts with a higher 'virality score' tend to be Reels with engaging content. The top viral post had a virality score of 80%.",
    "How can we reduce negative sentiment?": "Reducing negative sentiment can be done by avoiding controversial topics and focusing on positive, uplifting content."
}

# Load data
data = load_data()

# Calculate metrics
data["total_engagement"] = data["likes"] + data["shares"] + data["comments"]
data["engagement_rate"] = data["total_engagement"] / data["likes"] * 100
data["virality_score"] = (data["shares"] * 2 + data["comments"]) / data["likes"] * 100

# UI Elements
st.title("📱 Social Media Analyzer")
st.header("📊 Visual Analytics")
fig = px.bar(data, x="post_type", y="total_engagement", color="post_type", title="Total Engagement by Post Type")
st.plotly_chart(fig, use_container_width=True)

# Ask the Data Analyst Section
st.header("💬 Ask the Data Analyst (Powered by AI)")
question = st.selectbox(
    "Select a question to ask:",
    list(fake_ai_responses.keys())
)

if st.button("Analyze"):
    st.markdown(f"### 🤖 Answer: {fake_ai_responses[question]}")
