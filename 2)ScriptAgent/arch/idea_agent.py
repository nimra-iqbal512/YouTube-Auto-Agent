from langchain_groq import ChatGroq
from googleapiclient.discovery import build
import re

# API Keys
YOUTUBE_API_KEY = "youtube_api_key"
GROQ_API_KEY = "groq_api_key"

youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# Initialize Groq AI
llm = ChatGroq(temperature=0.7, groq_api_key=GROQ_API_KEY, model_name="Gemma2-9b-It")

def clean_title(title):
    """Remove hashtags, special symbols, and extra spaces from the title."""
    title = re.sub(r'[#@!$%^&*(){}\[\]:;"\'|<>?/\\+=~`]', '', title)  # Remove special characters
    title = re.sub(r'\s+', ' ', title).strip()  # Remove extra spaces
    return title

def get_top_trending_titles(category):
    """Fetch top 5 trending YouTube videos related to the given category and clean titles."""
    request = youtube.search().list(
        part="snippet",
        maxResults=5,  
        q=category,
        type="video",
        order="viewCount"
    )
    response = request.execute()

    return [clean_title(item["snippet"]["title"]) for item in response.get("items", [])]
