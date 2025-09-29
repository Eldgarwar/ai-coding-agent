from functions import run_python_file

def run_tests():
    """Runs all specified test cases for run_python_file."""

    print("--- Running main.py with no args ---")
    result = run_python_file("calculator", "main.py")
    print(result)
    print("\n" + "="*30 + "\n")

    print("--- Running main.py with args '3 + 5' ---")
    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print(result)
    print("\n" + "="*30 + "\n")

    print("--- Running tests.py ---")
    result = run_python_file("calculator", "tests.py")
    print(result)
    print("\n" + "="*30 + "\n")

    print("--- Attempting to run a file outside the working directory ---")
    result = run_python_file("calculator", "../main.py")
    print(result)
    print("\n" + "="*30 + "\n")

    print("--- Attempting to run a non-existent file ---")
    result = run_python_file("calculator", "nonexistent.py")
    print(result)
    print("\n" + "="*30 + "\n")


if __name__ == "__main__":
    run_tests()
