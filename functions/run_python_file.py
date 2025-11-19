import os
import subprocess

from google import genai
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    joined_path = os.path.abspath(os.path.join(working_directory, file_path))
    working_path = os.path.abspath(working_directory)

    if not os.path.isfile(joined_path):
        return f'Error: File "{file_path}" not found'

    if os.path.commonpath([working_path, joined_path]) != working_path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not joined_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        result = subprocess.run(
            ["python3", f"{joined_path}"], text=True, timeout=30, capture_output=True
        )

        if result.returncode == 0:
            return f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
        if not result.stdout and not result.stderr:
            return f"No output produced."
        return f"Process exited with code {result.returncode}"

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run the requested file in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Run (exec) the file of your choice, relative to the working directory. If not provided, the process will cancel.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Run the provided file_path, relative to the working directory. If not provided, the process will cancel.",
            ),
        },
    ),
)
