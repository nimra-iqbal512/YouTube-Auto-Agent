import os
import requests
import re
from dotenv import load_dotenv

class ScriptGenerator:
    def __init__(self):
        """Initialize Hugging Face API credentials."""
        load_dotenv()
        self.api_url = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
        self.headers = {"Authorization": f"Bearer {os.getenv('HUGGING_FACE_TOKEN')}"}

    def generate_similar_titles(self, title):
        """Generate five similar YouTube titles based on the provided title."""
        prompt = f"""
        Given the YouTube video title: "{title}", generate five alternative engaging YouTube video titles.

        Only return the five generated titles, each on a new line without numbering, explanations, or additional text.
        """

        response = requests.post(self.api_url, headers=self.headers, json={"inputs": prompt})
        result = response.json()

        if isinstance(result, list) and result:
            generated_text = result[0].get("generated_text", "").strip()
            
            # Extract lines, ignoring the first two lines
            lines = [t.strip() for t in generated_text.split("\n") if t.strip()]
            filtered_titles = lines[2:]  # Skip the first two lines

            # Remove any numbering at the start (e.g., "1.", "2.")
            clean_titles = [re.sub(r"^\d+\.\s*", "", title) for title in filtered_titles]

            return clean_titles[:5] if len(clean_titles) >= 5 else clean_titles + ["(Title missing)"] * (5 - len(clean_titles))
        
        return ["No titles generated."]
    
    def select_final_title(self, titles):
        """Display the generated titles in a formatted way."""
        print("\nGenerated Similar Titles:")
        for idx, title in enumerate(titles, start=1):
            print(f"{idx}. {title}")
        
        # Ask the user to select a title
        while True:
            try:
                choice = int(input("\nEnter the number of your chosen title: ").strip())
                if 1 <= choice <= len(titles):
                    return titles[choice - 1]
                else:
                    print("Invalid selection. Please enter a number from the list.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")


    def generate_script(self, prompt):
        """Generate a script based on the given prompt using the Hugging Face API."""
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 2000,
                "temperature": 0.9,
                "do_sample": True,
                "top_p": 0.85,
                "repetition_penalty": 1.2
            }
        }
        response = requests.post(self.api_url, headers=self.headers, json=payload)
        return response.json()

    def save_script(self, script, filename="youtube_script.txt"):
        """Save the generated script to a file."""
        generated_text = script[0]["generated_text"] if isinstance(script, list) and script else "No script generated."
        
        with open(filename, "w", encoding="utf-8") as file:
            file.write(generated_text)
        
        print("Script saved successfully!")

if __name__ == "__main__":
    script_generator = ScriptGenerator()
    similar_titles = script_generator.generate_similar_titles("Programing is Fun")
    final_title = script_generator.select_final_title(similar_titles)
    print(final_title)
    

    example_prompt = f"""
    Title: {final_title}
    
    Write a detailed, engaging YouTube script, of about 1800-2000 words. 
    Include an introduction, main points each with explanation, and a conclusion. 
    Use conversational language and provide examples.
    
    Script:
    """
    generated_script = script_generator.generate_script(example_prompt)
    script_generator.save_script(generated_script)
