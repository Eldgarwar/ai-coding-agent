from functions import get_files_info

def run_tests():
    """Runs all specified test cases for get_files_info."""

    print("Result for current directory:")
    print(get_files_info("calculator", "."))
    print("\n" + "="*30 + "\n")

    print("Result for 'pkg' directory:")
    print(get_files_info("calculator", "pkg"))
    print("\n" + "="*30 + "\n")
    
    print("Result for '/bin' directory:")
    print(get_files_info("calculator", "/bin"))
    print("\n" + "="*30 + "\n")

    print("Result for '../' directory:")
    print(get_files_info("calculator", "../"))
    print("\n" + "="*30 + "\n")


if __name__ == "__main__":
    run_tests()