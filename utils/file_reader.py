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
