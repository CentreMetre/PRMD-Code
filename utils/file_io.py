import json
import os


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
        raise e
    except Exception as e:
        raise e


def write_to_json_file(file_path: str, data: dict) -> None:
    """

    Args:
        file_path: the full path, including file name, path to the [;ace] to write the json file.
        data: The reading data.

    Returns:

    """

    full_path = os.path.join(dir_path, file_name + ".json")

    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    print(full_path)

    with open(full_path, 'w') as f:
        json.dump(readings, f, indent=4)