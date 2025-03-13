import idea_agent
import script_agent

def main():
    # Ask for category ONCE
    category = input("Enter a category (e.g., tech, gaming, finance): ").strip()
    
    # Get trending titles (passing category correctly)
    trending_titles = idea_agent.get_top_trending_titles(category)  

    print("\nTop 5 Trending YouTube Video Titles:")
    for idx, title in enumerate(trending_titles, start=1):
        print(f"{idx}. {title}")

    # Ask user to select or enter a custom title
    print("\nChoose an option:")
    print("1. Select a title from the Idea Agent")
    print("2. Enter a custom title")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        try:
            title_index = int(input("Enter the number of the title you want to use: ")) - 1
            if 0 <= title_index < len(trending_titles):
                selected_title = trending_titles[title_index]
            else:
                print("Invalid selection. Exiting...")
                return
        except ValueError:
            print("Invalid input. Exiting...")
            return
    elif choice == "2":
        selected_title = input("Enter your custom title: ").strip()
    else:
        print("Invalid choice. Exiting...")
        return

    # Generate 5 more related ideas (Fixed function call)
    related_ideas = script_agent.generate_related_ideas(selected_title)  # FIXED!

    print("\nTop 5 Related Ideas:")
    for idx, idea in enumerate(related_ideas, start=1):
        print(f"{idx}. {idea}")

    # Ask the user to select a final title from the related ideas
    try:
        new_title_index = int(input("\nSelect a title from the related ideas (1-5): ")) - 1
        if 0 <= new_title_index < len(related_ideas):
            final_selected_title = related_ideas[new_title_index]
        else:
            print("Invalid selection. Using the original title.")
            final_selected_title = selected_title
    except ValueError:
        print("Invalid input. Using the original title.")
        final_selected_title = selected_title

    # Generate script based on the final selected title
    script_agent.generate_script(final_selected_title)

if __name__ == "__main__":
    main()
