import streamlit as st
from streamlit_player import st_player

st.set_page_config(
    layout="wide",
    page_title = 'Tweet Scrapping Tool',
    page_icon = '🐦',
)


st.title("🐦Tweet Scrapping")
st.write("Twitter scraping involves collecting data or scraping data from Twitter's website using web scraping techniques. It can be used for various purposes such as sentiment analysis, social media monitoring, trend analysis, and more.")
st_player("")

st.header("😶Sentiment Analysis")
st.write(""""Sentiment analysis is a method for comprehending and interpreting the emotions or viewpoints expressed in a text. 
It entails analyzing the text's language to determine whether it conveys a positive😀, negative😔, or neutral😐 sentiment. 
Businesses and individuals can use this information to better comprehend how people feel about their products, services, or topics of interest, and 
to make more informed decisions.""")
st.header("💻Technologies Uesd")
st.write("""*📎Python*,\n
*📎Snscrape*,\n
*📎MongoDB*,\n 
*📎Streamlit*,\n 
*📎NLP*,\n
""")