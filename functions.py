import os
import config
import subprocess # Required for running external commands

# --- This function remains unchanged ---
def get_files_info(working_directory, directory="."):
    """Lists the contents of a specified directory within a working directory."""
    try:
        full_path = os.path.join(working_directory, directory)
        abs_full_path = os.path.abspath(full_path)
        abs_working_dir = os.path.abspath(working_directory)
        if not abs_full_path.startswith(abs_working_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(abs_full_path):
            return f'Error: "{directory}" is not a directory'
        output_lines = []
        for item_name in os.listdir(abs_full_path):
            item_path = os.path.join(abs_full_path, item_name)
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            output_lines.append(f"- {item_name}: file_size={file_size} bytes, is_dir={is_dir}")
        return "\n".join(output_lines)
    except Exception as e:
        return f"Error: {e}"

# --- This function remains unchanged ---
def get_file_content(working_directory, file_path):
    """Reads the content of a specified file within a working directory."""
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_full_path = os.path.abspath(full_path)
        abs_working_dir = os.path.abspath(working_directory)
        if not abs_full_path.startswith(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(abs_full_path, 'r', encoding='utf-8') as f:
            content = f.read(config.MAX_FILE_READ_CHARS + 1)
        if len(content) > config.MAX_FILE_READ_CHARS:
            truncated_content = content[:config.MAX_FILE_READ_CHARS]
            return f'{truncated_content}[...File "{file_path}" truncated at {config.MAX_FILE_READ_CHARS} characters]'
        return content
    except UnicodeDecodeError:
        return f'Error: Cannot read "{file_path}" as it is not a valid text file.'
    except Exception as e:
        return f"Error: {e}"

# --- This function remains unchanged ---
def write_file(working_directory, file_path, content):
    """Writes or overwrites content to a specified file within a working directory."""
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_full_path = os.path.abspath(full_path)
        abs_working_dir = os.path.abspath(working_directory)
        if not abs_full_path.startswith(abs_working_dir):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        parent_dir = os.path.dirname(abs_full_path)
        os.makedirs(parent_dir, exist_ok=True)
        with open(abs_full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"

# --- NEW FUNCTION ADDED BELOW ---
def run_python_file(working_directory, file_path, args=[]):
    """
    Executes a Python file in a controlled environment.

    Args:
        working_directory (str): The directory where the command should be run.
        file_path (str): The relative path to the Python file to execute.
        args (list): A list of string arguments to pass to the script.

    Returns:
        str: The captured stdout, stderr, and exit code, or an error message.
    """
    try:
        # 1. Security & Validation Checks
        full_path = os.path.join(working_directory, file_path)
        abs_full_path = os.path.abspath(full_path)
        abs_working_dir = os.path.abspath(working_directory)

        if not abs_full_path.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(abs_full_path):
            return f'Error: File "{file_path}" not found.'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        # 2. Execute the file using subprocess
        command = ["python", abs_full_path] + args
        completed_process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=working_directory
        )

        # 3. Format the output
        output_lines = []
        if completed_process.stdout:
            output_lines.append(f"STDOUT:\n{completed_process.stdout.strip()}")
        
        if completed_process.stderr:
            output_lines.append(f"STDERR:\n{completed_process.stderr.strip()}")

        if completed_process.returncode != 0:
            output_lines.append(f"Process exited with code {completed_process.returncode}")

        if not output_lines:
            return "No output produced."

        return "\n".join(output_lines)

    except subprocess.TimeoutExpired:
        return f"Error: Execution of '{file_path}' timed out after 30 seconds."
    except Exception as e:
        # 4. Catch any other exceptions
        return f"Error: executing Python file: {e}"

