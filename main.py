import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai

client = genai.Client(api_key=api_key)


def main():
    print("Hello from ai-coding-agent!")

    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents='Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.'
    )
    # 1. Print the text response
    print("\n--- Response Text ---")
    print(response.text)

    # 2. Print the two requested usage_metadata fields
    print("\n--- Usage Metadata ---")
    prompt_tokens = response.usage_metadata.prompt_token_count
    candidates_tokens = response.usage_metadata.candidates_token_count

    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {candidates_tokens}")

if __name__ == "__main__":
    main()
