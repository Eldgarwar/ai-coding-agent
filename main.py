import sys
import os
from google import genai
from google.genai import types# pyright: ignore[reportMissingImports] 
from dotenv import load_dotenv# pyright: ignore[reportMissingImports] 

from prompts import system_prompt
from call_function import call_function, available_functions


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, verbose)


def generate_content(client, messages, verbose):
    """
    Repeatedly calls the Gemini API to generate content and handle tool calls
    until a final response is received or the maximum iterations are reached.
    """
    MAX_ITERATIONS = 20
    for i in range(MAX_ITERATIONS):
        if verbose:
            print(f"\n--- Iteration {i + 1} ---")
        try:
            # Call the model with the entire conversation history
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )

            if not response.candidates:
                print("No response candidates found. Exiting.")
                break

            # The model's response (which may include function calls) is in the first candidate
            candidate = response.candidates[0]
            # Add the model's response to the conversation history to maintain context
            messages.append(candidate.content)

            if verbose:
                print("Prompt tokens:", response.usage_metadata.prompt_token_count)
                print(
                    "Response tokens:", response.usage_metadata.candidates_token_count
                )

            # Check if the model's turn contains a function call
            if any(part.function_call for part in candidate.content.parts):
                # Process each function call requested by the model
                for part in candidate.content.parts:
                    if part.function_call:
                        function_call_result = call_function(
                            part.function_call, verbose
                        )

                        if verbose:
                            # Safely access the response for logging
                            if (
                                function_call_result.parts
                                and function_call_result.parts[0].function_response
                            ):
                                print(
                                    f"-> {function_call_result.parts[0].function_response.response}"
                                )

                        # Add the function call result (as a 'tool' role message) to the history
                        messages.append(function_call_result)
            else:
                # If there are no function calls, the model has provided the final answer.
                final_text = "".join(
                    part.text for part in candidate.content.parts if part.text
                )
                print(f"\n✨ Final Response:\n{final_text}")
                break  # Exit the loop

        except Exception as e:
            print(f"An error occurred during generation: {e}")
            break
    else:
        # This block executes if the loop completes without 'break'
        print(f"\nMaximum iterations ({MAX_ITERATIONS}) reached. Exiting.")


if __name__ == "__main__":
    main()