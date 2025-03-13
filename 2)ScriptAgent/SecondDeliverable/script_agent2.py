import os
import re
import requests
from dotenv import load_dotenv


class ScriptGenerator:
    def __init__(self):
        """Initialize Groq API credentials."""
        load_dotenv()
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.api_key = os.getenv("GROQ_API_KEY")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def generate_similar_titles(self, title):
        """Generate five similar YouTube titles based on the provided title."""
        prompt = f"""
        Given the YouTube video title: "{title}", generate five alternative engaging YouTube video titles.

        Only return the five generated titles, each on a new line without numbering, explanations, or additional text.
        """

        payload = {
            "model": "mixtral-8x7b-32768",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 100
        }

        response = requests.post(self.api_url, headers=self.headers, json=payload)
        result = response.json()

        if "choices" in result and result["choices"]:
            generated_text = result["choices"][0]["message"]["content"].strip()
            titles = [line.strip() for line in generated_text.split("\n") if line.strip()]

            # Remove extra numbering like "1. " at the start
            clean_titles = [re.sub(r'^\d+\)?\.\s*|\d+\)\s*|"', '', title) for title in titles]

            return clean_titles[:5] if len(clean_titles) >= 5 else clean_titles + ["(Title missing)"] * (5 - len(clean_titles))

        return ["No titles generated."]
    

    def select_final_title(self, titles):
        """Display the generated titles in a formatted way, and select a final one."""
        print("\nGenerated Similar Titles:")
        for idx, title in enumerate(titles, start=1):
            print(f"{idx}. {title}")
        
        # Ask the user to select a title
        while True:
            try:
                choice = int(input("\nEnter the number of your final title: ").strip())
                if 1 <= choice <= len(titles):
                    return titles[choice - 1]
                else:
                    print("Invalid selection. Please enter a number from the list.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def generate_script(self, title):
        """Generate a detailed YouTube script based on the selected title."""
        prompt = f"""
        Title: {title}

        Write a detailed, engaging YouTube script of about 1800-2000 words for a faceless channel.
        - Start with an attention-grabbing introduction.
        - Cover key points in an easy-to-understand way.
        - Use a conversational tone with relatable examples.
        - End with a strong conclusion encouraging audience engagement.

        Script:
        """

        payload = {
            "model": "mixtral-8x7b-32768",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 2000,
            "temperature": 0.9,
            "top_p": 0.85
        }

        response = requests.post(self.api_url, headers=self.headers, json=payload)
        result = response.json()

        if "choices" in result and result["choices"]:
            return result["choices"][0]["message"]["content"].strip()

        return "No script generated."
    

    def save_script(self, script, filename="youtube_script.txt"):
        """Save the generated script to a text file."""
        with open(filename, "w", encoding="utf-8") as file:
            file.write(script)  # Directly saving script as it's a string
        
        print("\n✅ Script saved successfully as 'youtube_script.txt'!")



if __name__ == "__main__":
    script_generator = ScriptGenerator()
    video_title = "Programming is Fun"
    similar_titles = script_generator.generate_similar_titles(video_title)
    final_title = script_generator.select_final_title(similar_titles)
    print(final_title)

    generated_script = script_generator.generate_script(final_title)
    print(generated_script)
    script_generator.save_script(generated_script)