import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import MODEL_NAME, SYSTEM_PROMPT
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def main():
    if len(sys.argv) < 2:
        print("A prompt must be provided")
        sys.exit(1)

    messages = [
        types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
    ]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_write_file,
            schema_run_python_file,
            schema_get_file_content
        ]
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=SYSTEM_PROMPT
        ),
    )

    if "--verbose" in sys.argv:
        print(f"User prompt: {sys.argv[1]}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    for result in response.function_calls:
        print(f"Calling function: {result.name}({result.args})")


if __name__ == "__main__":
    main()
