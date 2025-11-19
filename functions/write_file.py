import os

from google import genai
from google.genai import types


def write_file(working_directory, file_path, content):
    joined_path = os.path.abspath(os.path.join(working_directory, file_path))
    working_path = os.path.abspath(working_directory)

    if os.path.commonpath([working_path, joined_path]) != working_path:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        with open(joined_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: Failed to write file {joined_path}: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write to the requested file in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Write to the provided file_path, relative to the working directory. If not provided, the process will cancel.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Write the content that was provided here.",
            ),
        },
    ),
)
