from idea_agent import YouTubeTrending
from script_agent import ScriptGenerator

def get_user_title_choice(titles):
    """Ask the user to select a trending title or enter a custom title."""
    print("\nDo you want to select a trending title or enter a custom title?")
    print("1. Select from trending titles")
    print("2. Enter a custom title")
    
    choice = input("Enter your choice (1 or 2): ").strip()
    
    if choice == "1":
        print("\nSelect a title:")
        for idx, title in enumerate(titles, start=1):
            print(f"{idx}. {title}")
        
        while True:
            try:
                selected_index = int(input("Enter the number of your chosen title: ").strip())
                if 1 <= selected_index <= len(titles):
                    return titles[selected_index - 1]
                else:
                    print("Invalid selection. Please enter a number from the list.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
    
    elif choice == "2":
        return input("Enter your custom title: ").strip()
    
    else:
        print("Invalid choice. Defaulting to a custom title.")
        return input("Enter your custom title: ").strip()

def main():
    # Idea generation
    category = input("Enter a category (e.g., tech, gaming, finance): ").strip()
    yt_trending = YouTubeTrending()
    titles = yt_trending.get_top_trending_titles(category)
    
    print("\nTop Trending YouTube Video Titles:")
    for idx, title in enumerate(titles, start=1):
        print(f"{idx}. {title}")
    
    final_title = get_user_title_choice(titles)
    # print(f"\nSelected Title: {final_title}")

    
    # script generation
    script_generator = ScriptGenerator()
    similar_titles = script_generator.generate_similar_titles(final_title)
    final_script_title = script_generator.select_final_title(similar_titles)
    print("final", final_script_title)

    example_prompt = f"""
    Title: {final_script_title}
    
    Write a detailed, engaging YouTube script, of about 1800-2000 words. 
    Include an introduction, main points each with explanation, and a conclusion. 
    Use conversational language and provide examples.
    
    Script:
    """
    generated_script = script_generator.generate_script(example_prompt)
    script_generator.save_script(generated_script)


if __name__ == "__main__":
    main()
