import os
import re
from googleapiclient.discovery import build
from dotenv import load_dotenv

class YouTubeTrending:
    def __init__(self):
        """Initialize YouTube API client."""
        load_dotenv()
        api_key = os.getenv("YOUTUBE_API_KEY")
        self.youtube = build("youtube", "v3", developerKey=api_key)
    
    def get_top_trending_titles(self, category, max_results=5):
        """Fetch top trending YouTube videos titles related to the given category. Titles should be in English, and contains no hahstags"""
        titles = []
        next_page_token = None
        
        while len(titles) < max_results:
            request = self.youtube.search().list(
                part="snippet",
                maxResults=max_results,
                q=category,
                type="video",
                order="viewCount",
                pageToken=next_page_token
            )
            response = request.execute()
            
            for item in response.get("items", []):
                title = item["snippet"]["title"]
                clean_title = re.sub(r"#\S+", "", title).strip()
                if clean_title.isascii():
                    titles.append(clean_title)
                    if len(titles) >= max_results:
                        break
            
            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break
        
        return titles

    def display_trending_titles(self, category):
        """Display the top trending video titles."""
        trending_titles = self.get_top_trending_titles(category)
        print("\nTop Trending YouTube Video Titles:")
        for idx, title in enumerate(trending_titles, start=1):
            print(f"{idx}. {title}")

# if __name__ == "__main__":
#     category = input("Enter a category (e.g., tech, gaming, finance): ").strip()
#     yt_trending = YouTubeTrending()
#     yt_trending.display_trending_titles(category)
