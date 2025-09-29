import os

def get_files_info(working_directory, directory="."):
    """
    Lists the contents of a specified directory within a working directory.

    Args:
        working_directory (str): The absolute path to the permitted parent directory.
        directory (str): A relative path from the working_directory to list.

    Returns:
        str: A formatted string of the directory contents or an error message.
    """
    try:
        # 1. Construct the full path and resolve it to an absolute path
        full_path = os.path.join(working_directory, directory)
        abs_full_path = os.path.abspath(full_path)
        abs_working_dir = os.path.abspath(working_directory)

        # 2. Security Check: Ensure the path is within the working directory
        if not abs_full_path.startswith(abs_working_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # 3. Validation: Check if the path is a directory
        if not os.path.isdir(abs_full_path):
            return f'Error: "{directory}" is not a directory'

        # 4. Get directory contents and format the output string
        output_lines = []
        for item_name in os.listdir(abs_full_path):
            item_path = os.path.join(abs_full_path, item_name)
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            output_lines.append(f"- {item_name}: file_size={file_size} bytes, is_dir={is_dir}")

        return "\n".join(output_lines)

    except Exception as e:
        # 5. Catch any other potential OS errors (e.g., permissions)
        return f"Error: {e}"