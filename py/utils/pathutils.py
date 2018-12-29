import os
import logging


def get_subdirs(path):
    """Return the subdirectories of a directory

    Parameters:
    -----------
    path : str
        directory to return subdirs from

    Returns:
    --------
    None if no directory is given
    List of subdirectories
    """
    log = logging.getLogger(__name__ + "." + "get_subdirs")
    if not os.path.isdir(path):
        log.debug(str(path) + " is no valid directory!")
        return None
    dirs = next(os.walk(path))[1]
    dirs.sort()
    log.debug(str(len(dirs)) + " subdirectories identified in " + str(path))
    return dirs


def get_files(path):
    """Return the files in a directory

    Parameters:
    -----------
    path : str
        directory to return files from

    Returns:
    --------
    None if no directory is given
    List of files
    """
    log = logging.getLogger(__name__ + "." + "get_files")
    if not os.path.isdir(path):
        log.debug(str(path) + " is no valid directory!")
        return None
    files = next(os.walk(path))[2]
    files.sort()
    log.debug(str(len(files)) + " files identified in " + str(path))
    return files
