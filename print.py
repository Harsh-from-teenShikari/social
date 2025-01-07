import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.badges import badge

# Set page configuration
st.set_page_config(page_title="Social Media Analyzer", page_icon="📊", layout="wide")

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
    "Which post has the highest engagement?": "Post ID 61 (Reel) has the highest engagement with 661 total interactions.",
    "What is the average sentiment score across all posts?": "The average sentiment score across all posts is approximately 0.05.",
    "How many posts have a negative sentiment score?": "There are 48 posts with a negative sentiment score.",
    "Which post type has the highest average virality score?": "Carousel posts have the highest average virality score, indicating they are shared more frequently relative to likes."
}

# Fake GPT analysis function
def ask_gpt_fake(query):
    fake_answers = {
        "What post type has the highest engagement rate?": "Reels have the highest engagement rate, averaging 87.5%.",
        "Which post type is least popular?": "Static images are the least popular, with lower total engagement compared to other post types.",
        "What is the average sentiment score for carousels?": "The average sentiment score for carousel posts is -0.04.",
        "Which post has the lowest sentiment score?": "Post ID 73 (Static Image) has the lowest sentiment score of -0.96.",
        "What is the post with the highest virality score?": "Post ID 52 (Carousel) has the highest virality score of 160.9%.",
    }
    return fake_answers.get(query, "I don't have an answer for that question.")

# Cache data loading
@st.cache_data
def load_data():
    return pd.DataFrame([
        [1, "reel", 148, 49, 13, 0.45],
        [2, "reel", 338, 63, 44, -0.41],
        [3, "reel", 392, 26, 17, -0.7],
        [4, "static_image", 238, 98, 136, 0.19],
        [5, "carousel", 120, 34, 10, 0.30],
        [6, "static_image", 354, 77, 22, 0.3],
        [7, "reel", 265, 99, 31, 0.88],
        [8, "static_image", 366, 23, 44, -0.33],
        [9, "static_image", 488, 87, 128, 0.06],
        [10, "static_image", 283, 99, 191, 0.77],
        [11, "static_image", 371, 52, 30, -0.68],
        [12, "reel", 452, 8, 81, -0.56],
        [13, "static_image", 358, 30, 53, 0.75],
        [14, "reel", 124, 76, 144, -0.29],
        [15, "reel", 89, 14, 132, 0.5],
        [16, "static_image", 173, 64, 184, -0.51],
        [17, "carousel", 227, 65, 149, 0.75],
        [18, "reel", 139, 73, 153, -0.45],
        [19, "carousel", 75, 44, 53, 0.02],
        [20, "static_image", 264, 31, 170, 0.37],
        [21, "reel", 448, 44, 189, -0.11],
        [22, "reel", 475, 34, 72, 0.49],
        [23, "reel", 193, 5, 123, -0.86],
        [24, "static_image", 311, 28, 79, -0.89],
        [25, "reel", 225, 29, 50, -0.79],
        [26, "static_image", 132, 92, 58, -0.32],
        [27, "carousel", 291, 32, 48, -0.64],
        [28, "carousel", 232, 31, 149, -0.22],
        [29, "static_image", 222, 26, 120, 0.25],
        [30, "reel", 482, 58, 104, -0.95],
        [31, "carousel", 251, 91, 194, 0.31],
        [32, "reel", 160, 88, 120, 0.17],
        [33, "reel", 388, 33, 88, 0.08],
        [34, "static_image", 321, 50, 150, -0.63],
        [35, "static_image", 466, 99, 187, -0.15],
        [36, "carousel", 50, 82, 19, -0.76],
        [37, "static_image", 284, 20, 195, 0.87],
        [38, "reel", 272, 14, 12, -0.2],
        [39, "reel", 226, 74, 181, 0.79],
        [40, "carousel", 135, 60, 153, -0.34],
        [41, "reel", 270, 59, 122, -0.38],
        [42, "static_image", 497, 34, 162, -0.55],
        [43, "reel", 465, 64, 15, 0.96],
        [44, "static_image", 128, 89, 39, 0.33],
        [45, "static_image", 489, 37, 123, -0.89],
        [46, "static_image", 89, 24, 127, 0.65],
        [47, "carousel", 362, 81, 50, -0.99],
        [48, "carousel", 375, 73, 31, -0.12],
        [49, "reel", 292, 60, 11, -0.78],
        [50, "static_image", 366, 70, 30, -0.67],
        [51, "static_image", 408, 14, 94, 0.24],
        [52, "carousel", 151, 97, 137, 0.59],
        [53, "reel", 262, 35, 72, 0.6],
        [54, "carousel", 327, 67, 85, -0.79],
        [55, "carousel", 382, 90, 162, -0.33],
        [56, "static_image", 181, 26, 27, -0.7],
        [57, "static_image", 488, 76, 194, 0.72],
        [58, "static_image", 276, 79, 169, 0.7],
        [59, "reel", 185, 42, 30, 0.52],
        [60, "static_image", 261, 6, 134, -0.09],
        [61, "reel", 439, 32, 190, -0.19],
        [62, "reel", 492, 58, 141, 0.69],
        [63, "reel", 155, 52, 180, -0.56],
        [64, "carousel", 445, 53, 193, 0.22],
        [65, "reel", 136, 19, 37, -0.28],
        [66, "static_image", 470, 84, 90, -0.11],
        [67, "reel", 85, 43, 176, -0.07],
        [68, "carousel", 372, 82, 159, 0.88],
        [69, "carousel", 418, 28, 152, -0.84],
        [70, "carousel", 251, 71, 47, 0.27],
        [71, "carousel", 140, 76, 53, 0.78],
        [72, "static_image", 105, 90, 65, -0.59],
        [73, "static_image", 292, 8, 40, -0.96],
        [74, "reel", 414, 69, 80, -0.84],
        [75, "carousel", 374, 98, 58, -0.08],
        [76, "carousel", 427, 68, 140, 0.79],
        [77, "static_image", 96, 82, 141, 0.58],
        [78, "carousel", 166, 17, 13, 0.12],
        [79, "carousel", 263, 61, 81, 0.1],
        [80, "reel", 415, 54, 20, -0.05],
        [81, "carousel", 481, 24, 96, -0.23],
        [82, "reel", 295, 85, 167, -0.23],
        [83, "reel", 472, 11, 138, 0.84],
        [84, "reel", 362, 25, 32, -0.54],
        [85, "reel", 395, 8, 194, 0.7],
        [86, "carousel", 126, 86, 96, 0.79],
        [87, "reel", 398, 13, 149, 0.1],
        [88, "carousel", 136, 45, 178, -0.41],
        [89, "carousel", 293, 73, 193, -0.76],
        [90, "reel", 264, 9, 143, 0.58],
        [91, "static_image", 165, 82, 113, -0.36],
        [92, "static_image", 457, 9, 160, 0.11],
        [93, "carousel", 184, 86, 141, -0.57],
        [94, "reel", 240, 35, 97, -0.73],
        [95, "carousel", 326, 99, 56, -0.31],
        [96, "static_image", 183, 39, 79, 0.87],
        [97, "reel", 427, 94, 175, 0.35],
        [98, "reel", 277, 39, 48, 0.68],
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
            st.metric("🖍 Total Posts", len(filtered_data))
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
        col1, col2 = st.columns([4, 1])
        with col1:
            query = st.text_input("Ask a question about the data:")
            answer_placeholder = st.empty()  # Placeholder for the answer output
            with col2:
                if st.button("Analyze"):
                    if query:
                        with st.spinner("Analyzing..."):
                            answer = ask_gpt(query, data_summary)
                            if answer:
                                answer_placeholder.markdown(f"### 🤖 Answer: {answer}")
                            else:
                                st.warning("Please enter a question.")

    else:
        st.warning("No data available for the selected filters.")

except Exception as e:
    st.error(f"An error occurred: {str(e)}")
st.header("🎯 Content Strategy Recommendations")
st.markdown("""
Here are some tips based on your data analysis:
- 🧲 **Focus on reels** for higher engagement.
- 😊 **Monitor sentiment scores** to ensure positive interactions.
- 📸 **Experiment with carousels** to diversify content.
- 📈 **Track post performance** regularly for optimization.
""")
