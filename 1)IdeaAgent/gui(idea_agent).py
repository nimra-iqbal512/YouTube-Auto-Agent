import os
import tkinter as tk
from tkinter import ttk, messagebox
import googleapiclient
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load API Keys from environment variables
load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# Predefined YouTube categories
CATEGORY_IDS = {
    "Film & Animation": "1",
    "Autos & Vehicles": "2",
    "Music": "10",
    "Pets & Animals": "15",
    "Sports": "17",
    "Short Movies": "18",
    "Travel & Events": "19",
    "Gaming": "20",
    "People & Blogs": "22",
    "Comedy": "23",
    "Entertainment": "24",
    "News & Politics": "25",
    "How-to & Style": "26",
    "Education": "27",
    "Science & Tech": "28",
}

# List of regions (Country Codes)
REGIONS = ["US", "IN", "PK", "GB", "CA", "AU", "FR", "DE", "BR", "JP"]

def get_category_id(category_name):
    """Returns the category ID for the given category name, or None if not found."""
    return CATEGORY_IDS.get(category_name)

def get_top_trending_titles(region_code, category_name):
    category_id = get_category_id(category_name)
    if category_id is None:
        print("Invalid category name. Please select a valid category.")
        return []

    # Fetch top 5 trending YouTube videos related to the given category
    request = youtube.videos().list(
        part="snippet",
        chart="mostPopular",
        maxResults=5,
        regionCode=region_code,
        videoCategoryId=category_id
    )

    try:
        response = request.execute()
        return [item["snippet"]["title"] for item in response.get("items", [])]
    except googleapiclient.errors.HttpError as e:
        print(f"API Error: {e}")
        return []


# Function to fetch videos when button is clicked
def fetch_videos():
    selected_region = region_var.get()
    selected_category = category_var.get()

    if not selected_region or not selected_category:
        messagebox.showwarning("Input Error", "Please select both region and category.")
        return

    trending_titles = get_top_trending_titles(selected_region, selected_category)

    # Display results in a messagebox
    result_text = f"Top 5 {selected_category} videos in {selected_region}:\n\n"
    result_text += "\n".join(f"{idx+1}. {title}" for idx, title in enumerate(trending_titles))

    messagebox.showinfo("Trending Videos", result_text)

# Create main window
root = tk.Tk()
root.title("YouTube Trending Videos")
root.geometry("600x350")

# Welcome message
welcome_label = tk.Label(root, text="Welcome to YouTube Trending Video Finder!", font=("Arial", 12, "bold"))
welcome_label.pack(pady=10)

# Region selection dropdown
tk.Label(root, text="Select Region:").pack()
region_var = tk.StringVar()
region_dropdown = ttk.Combobox(root, textvariable=region_var, values=REGIONS, state="readonly")
region_dropdown.pack(pady=5)

# Category selection dropdown
tk.Label(root, text="Select Category:").pack()
category_var = tk.StringVar()
category_dropdown = ttk.Combobox(root, textvariable=category_var, values=list(CATEGORY_IDS.keys()), state="readonly")
category_dropdown.pack(pady=5)

# Fetch videos button
fetch_button = tk.Button(root, text="Get Trending Videos", command=fetch_videos, bg="blue", fg="white")
fetch_button.pack(pady=10)

# Run the GUI application
root.mainloop()
