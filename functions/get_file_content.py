import os
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

        return file_content_trunc + f'...File "{joined_path}" truncated at {MAX_CHARS} characters' if len(file_content) > MAX_CHARS else file_content

