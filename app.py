import streamlit as st
import pandas as pd
import plotly.express as px
import openai
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.badges import badge

# Set page configuration
st.set_page_config(page_title="Social Media Analyzer with GPT", page_icon="📊", layout="wide")

# Data validation function
def validate_data(df):
    required_columns = ["post_id", "post_type", "likes", "shares", "comments", "avg_sentiment_score"]
    if not all(col in df.columns for col in required_columns):
        raise ValueError("Missing required columns in data")
    if df.isnull().values.any():
        st.warning("Data contains null values")

# Predefined Q&A
Frequently_asked_questions = {
    "What is the most popular post type?": "Reels tend to have the highest engagement rates, making them the most popular post type.",
    "How is engagement rate calculated?": "Engagement rate is calculated as the sum of likes, shares, and comments divided by the total number of likes, multiplied by 100.",
    "What is a good sentiment score?": "A sentiment score above 0.5 is considered positive, while scores below -0.5 are considered negative.",
    "What does the virality score represent?": "Virality score represents how likely a post is to be shared. It is calculated as (shares * 2 + comments) / likes * 100.",
}

# GPT analysis function
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
    st.title("📱 Social Media Analyzer with GPT")
    badge("github", "https://github.com/Harsh-from-teenShikari/social")
    add_vertical_space(2)
    
    # Sidebar filters
    st.sidebar.header("📊 Filter Options")
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
            st.metric("📝 Total Posts", len(filtered_data))
        with col2:
            st.metric("📊 Avg. Engagement", f"{filtered_data['total_engagement'].mean():.0f}")
        with col3:
            st.metric("📈 Engagement Rate", f"{filtered_data['engagement_rate'].mean():.1f}%")
        with col4:
            st.metric("😊 Avg. Sentiment", f"{filtered_data['avg_sentiment_score'].mean():.2f}")
        
        # Visualizations
        st.header("📊 Visual Analytics")
        fig = px.bar(filtered_data, x="post_type", y="total_engagement",
                    color="post_type", title="Total Engagement by Post Type",
                    template="plotly_white")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # Predefined Q&A Section
        st.header("📖 frequent Insights")
        for question, answer in Frequently_asked_questions.items():
            with st.expander(question):
                st.write(answer)

        # GPT Section
        st.header("💬 Ask the Data Analyst (Powered by GPT)")
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
                            st.markdown(f"### 🤖 Answer: {answer}")
                else:
                    st.warning("Please enter a question.")
    else:
        st.warning("No data available for the selected filters.")

except Exception as e:
    st.error(f"An error occurred: {str(e)}")
