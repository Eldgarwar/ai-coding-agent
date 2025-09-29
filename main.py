import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    print("Hello from ai-coding-agent!\n")
    

    if len(sys.argv) < 2:
        print("No input provided. Exiting now...\n")
        exit(1)
        

    print("I have received your request and am processing it now...")
    args = sys.argv[1]
    ##user_prompt = " ".join(args)
    user_prompt = args
    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
    )
    if "--verbose" in sys.argv:
        print("Verbose mode enabled.")

        # 1. Print the two requested usage_metadata fields
        print("\n--- Usage Metadata ---")
        prompt_tokens = response.usage_metadata.prompt_token_count
        candidates_tokens = response.usage_metadata.candidates_token_count

        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {candidates_tokens}")

    # 2. Print the text response
    print("\n--- Response Text ---")
    print(response.text)



if __name__ == "__main__":
    main()
