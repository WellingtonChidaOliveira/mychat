import os
import sys
import logging
from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Ensure the API key is set in the environment variables
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logging.error("OPENAI_API_KEY environment variable not set.")
    sys.exit(1)

client = OpenAI(api_key=api_key)

def create_chat_completion(messages):
    """
    Create a chat completion using OpenAI's API.

    Args:
        messages (list): List of message dictionaries.

    Returns:
        response (dict): API response or None if an error occurred.
    """
    try:
        response = client.chat.completions.create(
            messages=messages,
            model="gpt-4o",
        )
        return response
    except Exception as e:
        logging.error(f"Error creating chat completion: {e}")
        return None

def main():
    """
    Main function to handle user input and bot responses.
    """
    context_messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    try:
        while True:
            user_input = input("User: ")
            if user_input.lower() == "exit":
                break

            context_messages.append({"role": "user", "content": user_input})
            chat_completion = create_chat_completion(messages=context_messages)

            if chat_completion:
                bot_response = chat_completion.choices[0].message.content
                print("Bot:", bot_response)
                context_messages.append({"role": "assistant", "content": bot_response})
            else:
                logging.warning("Failed to get a response from the bot.")
    except KeyboardInterrupt:
        logging.info("Exiting gracefully...")

if __name__ == "__main__":
    main()