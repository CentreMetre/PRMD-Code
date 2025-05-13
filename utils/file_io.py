import json


def read_file(file_path: str) -> str:
    """
    Reads and returns the content of a file at the specified path.

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        str: The content of the file.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        Exception: If any other error occurs while opening or reading the file.
    """
    try:
        with open(file_path, "r") as file:
            content = file.read()
        return content
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e
    except Exception as e:
        raise Exception(f"Error reading file: {file_path}") from e


def read_file_json(file_path: str) -> list:
    """
    Reads and returns the content of a JSON file at the specified path.

    Args:
        file_path (str): The path to the JSON file to be read.

    Returns:
        list: The content of the JSON file as a list of dictionaries.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        Exception: If any other error occurs while opening or reading the file.
    """
    try:
        with open(file_path, "r") as file:
            content = json.load(file)
        return content
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e
    except Exception as e:
        raise Exception(f"Error reading JSON file: {file_path}") from e
