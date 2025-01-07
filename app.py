import streamlit as st
import pandas as pd
import plotly.express as px
import openai
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.badges import badge

# Set page configuration
st.set_page_config(page_title="Social Media Analyzer with GPT", page_icon="📊", layout="wide")

# Load the data
data = pd.DataFrame([
    [1, "reel", 148, 49, 13, 0.45],
    [2, "reel", 338, 63, 44, -0.41],
    [3, "reel", 392, 26, 17, -0.7],
    [4, "static_image", 238, 98, 136, 0.19],
    [5, "carousel", 120, 34, 10, 0.30],
], columns=["post_id", "post_type", "likes", "shares", "comments", "avg_sentiment_score"])

# Calculate additional metrics
data["total_engagement"] = data["likes"] + data["shares"] + data["comments"]
data["engagement_rate"] = data["total_engagement"] / data["likes"] * 100
data["virality_score"] = (data["shares"] * 2 + data["comments"]) / data["likes"] * 100

# Function to connect to OpenAI API
def ask_gpt(query, data_summary):
    openai.api_key = "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"
    prompt = f"You are a data analyst. Here is the social media data summary: {data_summary}. Answer the following question: {query}"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Header with badges
st.title("📱 Social Media Analyzer with GPT")
badge("https://github.com/Harsh-from-teenShikari/social")
add_vertical_space(2)

# Sidebar filters
st.sidebar.header("📊 Filter Options")
st.sidebar.write("Use the filters below to customize the analysis.")
post_types = st.sidebar.multiselect("Select Post Types", data["post_type"].unique(), default=data["post_type"].unique())
filtered_data = data[data["post_type"].isin(post_types)]

# Overall Performance Metrics
st.header("📈 Overall Performance Analysis")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📝 Total Posts", len(filtered_data))
with col2:
    st.metric("📊 Avg. Engagement", f"{filtered_data['total_engagement'].mean():.0f}")
with col3:
    st.metric("📈 Engagement Rate", f"{filtered_data['engagement_rate'].mean():.1f}%")
with col4:
    st.metric("😊 Avg. Sentiment", f"{filtered_data['avg_sentiment_score'].mean():.2f}")

# Visualizations
st.header("📊 Visual Analytics")
fig = px.bar(filtered_data, x="post_type", y="total_engagement", color="post_type", title="Total Engagement by Post Type", template="plotly_white")
fig.update_layout(showlegend=False)
st.plotly_chart(fig, use_container_width=True)

# Interactive GPT Section
st.header("💬 Ask the Data Analyst (Powered by GPT)")
st.markdown("### 🤖 Chat with the AI to get insights from your data!")
data_summary = filtered_data.d
