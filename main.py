import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found. Please set it in your .env file.")
        exit(1)

    # This client initialization is correct for v1.12.1
    client = genai.Client(api_key=api_key)
    
    # Use a valid and current model name
    model_name = 'gemini-2.0-flash'

    print("Hello from ai-coding-agent!\n")

    # Improve argument handling to allow multi-word prompts
    args = [arg for arg in sys.argv[1:] if not arg.startswith('--')]
    if not args:
        print("No input provided. Exiting now...\n")
        exit(1)

    user_prompt = " ".join(args)
    print(f"I have received your request and am processing it now...\nPrompt: '{user_prompt}'")

    system_prompt = 'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'
    
    # --- FIX for google-genai v1.12.1 ---
    # The `system_instruction` parameter is not supported in this older version.
    # We must prepend the system instructions to the user prompt directly.
    combined_prompt = f"{system_prompt}\n\n---\n\n{user_prompt}"

    messages = [
        types.Content(role="user", parts=[types.Part(text=combined_prompt)]),
    ]

    try:
        # Call generate_content WITHOUT the unsupported `system_instruction` parameter.
        response = client.models.generate_content(
            model=model_name,
            contents=messages,
        )

        print("\n--- Response Text ---")
        print(response.text)

        if "--verbose" in sys.argv:
            print("\nVerbose mode enabled.")
            print("\n--- Usage Metadata ---")
            if response.usage_metadata:
                prompt_tokens = response.usage_metadata.prompt_token_count
                candidates_tokens = response.usage_metadata.candidates_token_count
                print(f"Prompt tokens: {prompt_tokens}")
                print(f"Response tokens: {candidates_tokens}")
            else:
                print("Usage metadata not available.")

    except Exception as e:
        print(f"\nAn error occurred: {e}")


if __name__ == "__main__":
    main()

