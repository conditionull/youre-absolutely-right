import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import MODEL_NAME, SYSTEM_PROMPT, MAX_ITER
from functions.call_function import call_function
from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

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

    for _ in range(MAX_ITER):
        response = generate_content(client, messages)
        if not response.function_calls and response.text:
            print(response.text)
            break

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if response.function_calls:
            function_responses = []
            for fc in response.function_calls:
                tool_content = call_function(fc, verbose="--verbose" in sys.argv)
                function_responses.append(tool_content.parts[0])
                try:
                    fn_resp = tool_content.parts[0].function_response.response
                except Exception:
                    raise RuntimeError(
                        "Fatal: missing function response from call_function"
                    )
                if "--verbose" in sys.argv:
                    print(f"-> {fn_resp}")
            messages.append(types.Content(role="user", parts=function_responses))


# helper
def generate_content(client, messages):
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_write_file,
            schema_run_python_file,
            schema_get_file_content,
        ]
    )
    return client.models.generate_content(
        model=MODEL_NAME,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=SYSTEM_PROMPT,
        ),
    )


if __name__ == "__main__":
    main()
