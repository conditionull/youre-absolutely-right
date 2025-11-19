import os

from google import genai
from google.genai import types


def get_files_info(working_directory, directory="."):

    joined_path = os.path.abspath(os.path.join(working_directory, directory))
    working_path = os.path.abspath(working_directory)

    if not os.path.isdir(joined_path):
        return f'Error: "{joined_path}" is not a directory'

    if os.path.commonpath([working_path, joined_path]) != working_path:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    content_info = []
    for content in os.listdir(joined_path):
        full_path = os.path.join(joined_path, content)
        content_info.append(
            f"{content}: file_size: {os.path.getsize(full_path)} bytes, is_dir={os.path.isdir(full_path)}"
        )
    return "\n".join(content_info)


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
