import os
import re


def path_normalizer(path: str):
    """
    Convert paths with \\ to /

    Args:
        path (str): string
    """
    result = re.sub('\\\\', '/', path)
    return result


def is_dir(path=''):
    return os.path.isdir(path)
