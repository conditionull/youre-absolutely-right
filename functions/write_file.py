import os

def write_file(working_directory, file_path, content):
    joined_path = os.path.abspath(os.path.join(working_directory, file_path))
    working_path = os.path.abspath(working_directory)

   
    try:
        if not os.path.exists(joined_path):
            with open(joined_path, 'w') as f:
                f.write(content)
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        else:
            return f"Error: File already exists: {joined_path}"
    except Exception as e:
        return f"Error: Failed to write file {joined_path}: {e}"
    
    if os.path.commonpath([working_path, joined_path]) != working_path:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

