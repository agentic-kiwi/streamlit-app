from chains.basic_qa import ask_question
from chains.conversational import chat_with_memory
from chains.parallel_analysis import analyze_from_multiple_perspectives
from chains.structured_analysis import analyze_topic
from config.gemini_setup import get_gemini_model, get_topic

def show_menu():
    print("\nMenu:")
    print("1. Ask a Basic Question")
    print("2. Structured Analysis")
    print("3. Parallel Analysis")
    print("4. Conversational Chat")
    print("5. Exit")

def main():
    """Main Application Loop."""
    topic = get_topic()
    print(f"🤖 Welcome to your AI Learning assistant!")
    print(f"Your current topic is: {topic}")

    while True:
        show_menu()
        choice = input("Choose an option (1-5): ")

        if choice == '1':
                question = input("Enter your question: ")
                response = ask_question(question)
                print(f"Response: {response}")

        elif choice == '2':
                question = input("Enter a topic for structured analysis: ")
                response = analyze_topic(question)
                print(f"Structured Analysis Response: {response}")

        elif choice == '3':
                question = input("Enter a topic for parallel analysis: ")
                results = analyze_from_multiple_perspectives(question)
                for perspective, response in results.items():
                    print(f"{perspective.capitalize()} perspective:")
                    print(response.content)
                    print()

        elif choice == '4':
                print("Starting conversational chat. Type 'exit' to end.")
                while True:
                    question = input("You: ")
                    if question.lower() == 'exit':
                        break
                    response = chat_with_memory(question)
                    print(f"Tutor: {response}")

        elif choice == '5':
                print("Exiting the program.")
                break

        else:
                print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
    
