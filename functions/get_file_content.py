import os

from google import genai
from google.genai import types

from functions.config import MAX_CHARS


def get_file_content(working_directory, file_path):
    joined_path = os.path.abspath(os.path.join(working_directory, file_path))
    working_path = os.path.abspath(working_directory)

    if not os.path.isfile(joined_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    if os.path.commonpath([working_path, joined_path]) != working_path:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    with open(joined_path, "r") as f:
        file_content_trunc = f.read(MAX_CHARS)
        f.seek(0)
        file_content = f.read()
        if len(file_content) == 0:
            return f'Error: The provided file: "{joined_path}" is empty'

        return (
            file_content_trunc
            + f'...File "{joined_path}" truncated at {MAX_CHARS} characters'
            if len(file_content) > MAX_CHARS
            else file_content
        )


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Lists file content in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list file content from, relative to the working directory. If not provided, lists the contents in the working directory itself.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Write to the provided file_path, relative to the working directory. If not provided, the process will cancel.",
            ),
        },
    ),
)
