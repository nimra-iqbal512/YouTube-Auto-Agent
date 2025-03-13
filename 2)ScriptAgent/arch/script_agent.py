import os
import re
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage
from dotenv import load_dotenv

# Load API keys from environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "key")  

# Initialize LLM
llm = ChatGroq(temperature=0.7, groq_api_key=GROQ_API_KEY, model_name="Gemma2-9b-It")

def clean_title(title):
    """Removes hashtags, special symbols, and extra spaces from a title."""
    return re.sub(r'[^\w\s]', '', title).strip()

def generate_related_ideas(selected_title):
    """Generate exactly 5 related YouTube video ideas with correct numbering."""
    prompt = f"Generate exactly 5 engaging YouTube video ideas based on the title: '{selected_title}'. Number them from 1 to 5."

    response = llm.invoke([SystemMessage(content=prompt)])

    # Extract ideas from response
    ideas = response.content.split("\n")
    ideas = [idea.strip() for idea in ideas if idea.strip()]  # Remove empty lines

    # Remove introductory text if present
    if ideas and ("Here are" in ideas[0] or "Based on the title" in ideas[0]):
        ideas.pop(0)  # Remove introduction if detected

    cleaned_ideas = []
    for idea in ideas:
        # Remove multiple leading numbers like "1. 1." or "2. 2."
        idea = re.sub(r'^\d+\.\s*\d+\.\s*', '', idea)  
        # Remove a single leading number like "1. "
        idea = re.sub(r'^\d+\.\s*', '', idea)  
        # Remove stray dashes or bullet points at the start
        idea = re.sub(r'^[-•]\s*', '', idea)
        cleaned_ideas.append(idea)

    # Filter out any empty or incomplete ideas
    cleaned_ideas = [idea for idea in cleaned_ideas if len(idea) > 10]  # Only keep meaningful ideas

    # Ensure exactly 5 ideas
    cleaned_ideas = cleaned_ideas[:5]

    # Apply correct numbering
    formatted_ideas = [f"{i+1}. {cleaned_ideas[i]}" for i in range(len(cleaned_ideas))]
    
    return formatted_ideas

def select_existing_title(available_titles):
    """Handles user selection of an existing title and generates related ideas correctly."""
    print("\nChoose an option:")
    print("1. Select a title from the Idea Agent")
    print("2. Enter a custom title")
    
    user_choice = input("Enter 1 or 2: ").strip()
    
    if user_choice == "1":
        print("\nTop 5 Trending YouTube Video Titles:")
        for i, title in enumerate(available_titles, 1):
            print(f"{i}. {title}")
        
        try:
            title_index = int(input("\nEnter the number of the title you want to use: ").strip()) - 1
            if 0 <= title_index < len(available_titles):
                selected_title = available_titles[title_index]
            else:
                print("Invalid selection. Exiting...")
                return None
        except ValueError:
            print("Invalid input. Exiting...")
            return None
    else:
        selected_title = input("\nEnter your custom title: ").strip()

    related_ideas = generate_related_ideas(selected_title)

    print("\nTop 5 Related Ideas:")
    for idx, idea in enumerate(related_ideas, start=1):
        print(f"{idx}. {idea}")

    # Ask user to select from related ideas
    try:
        idea_index = int(input("\nSelect a title from the related ideas (1-5): ").strip()) - 1
        if 0 <= idea_index < len(related_ideas):
            selected_idea = related_ideas[idea_index]
        else:
            print("Invalid selection. Using the original title.")
            selected_idea = selected_title
    except ValueError:
        print("Invalid input. Using the original title.")
        selected_idea = selected_title

    # Generate a script based on the final selected idea
    return generate_script(selected_idea)

def generate_script(title):
    """Generate a detailed and engaging YouTube video script for faceless content."""
    prompt = f"""
    Write a YouTube video script for the title: "{title}" tailored for a **faceless channel**.
    - The tone should be engaging, mysterious, and professional.
    - Start with a **hook** that captures curiosity.
    - Use **clear narration** with smooth transitions.
    - Include at least **three key points** with facts or storytelling.
    - Keep the sentences short and effective for AI voiceover.
    - End with a strong **call to action** encouraging likes, comments, and subscriptions.
    - No unnecessary filler words; make every line impactful.
    """
    
    response = llm.invoke([SystemMessage(content=prompt)])
    script = response.content.strip()
    
    print("\nGenerated Script:\n", script)
    return script

