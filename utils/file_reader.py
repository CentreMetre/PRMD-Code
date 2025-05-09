"""
=========================
This module provides utility functions for reading files.
Functions:
----------
- read_file(file_path): Opens a file at the specified path and returns its content as a string.
Exceptions:
-----------
- FileNotFoundError: Raised if the specified file does not exist.
- Exception: Raised for any other errors encountered while opening or reading the file.
File Reader Utility Module
========================

"""


def read_file(file_path):
    """
    Open a file and return its content.
    :param file_path: Path to the file to be opened.
    :return: Content of the file.
    :raises FileNotFoundError: If the file does not exist.
    :raises Exception: If there is an error opening the file.
    """
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError as e:
        raise e
    except Exception as e:
        raise e
