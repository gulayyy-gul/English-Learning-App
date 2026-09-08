import streamlit as st

# Page settings
st.set_page_config(
    page_title="English Learning App",
    page_icon="📚",
    layout="wide"
)

# Title
st.title("📚 English Learning App")
st.write("Learn English step by step with your personal learning assistant.")

# Student Profile
st.header("👤 Student Profile")

name = st.text_input("Your Name")

level = st.selectbox(
    "English Level",
    ["Beginner", "Elementary"]
)

daily_time = st.selectbox(
    "Daily Learning Time",
    ["15 minutes", "30 minutes", "45 minutes", "60 minutes"]
)

if st.button("🚀 Start Learning"):
    if name:
        st.success(f"Welcome, {name}! 👋")
        st.write(f"Your level: **{level}**")
        st.write(f"Daily study time: **{daily_time}**")
    else:
        st.warning("Please enter your name.")
