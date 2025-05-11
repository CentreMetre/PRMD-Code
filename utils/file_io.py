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
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError as e:
        raise e
    except Exception as e:
        raise e


def write_to_file_json(file_path: str, data: dict) -> None:
    """
    Writes the given data to a file in JSON format.

    Args:
        file_path (str): The path to the file where the data will be written.
        data (dict): The data to be written to the file in JSON format.

    Returns:
        None

    Raises:
        Exception: If there is an error while writing to the file.
    """
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file)
    except Exception as e:
        raise Exception(
            f"An error occurred while writing to the file {file_path}."
        ) from e
