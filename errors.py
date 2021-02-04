class Error(Exception):
    pass

class LoginError(Error):
    """
    Raised when there is an error while logging in.
    """
    def __init__(self):
        pass

class DatabaseError(Error):
    """
    Raised when there is an error in the database.
    """
    def __init__(self):
        pass

class BackupError(Error):
    """
    Raised when there is an error while backing up.
    """
    def __init__(self):
        pass

class BackupFailed(Error):
    """
    Raised when the backup fails.
    """
    def __init__(self):
        pass

class QuitError(Error):
    """
    Raised when closing the database fails.
    """
    def __init__(self):
        pass

class AddError(Error):
    """
    Raised when adding an entry to the database fails.
    """
    def __init__(self):
        pass

class RemoveError(Error):
    """
    Raised when removing an entry in the database fails.
    """
    def __init__(self):
        pass

class RecoverError(Error):
    """
    Raised when recovering the database from a backup fails.
    """
    def __init__(self):
        pass

class SearchError(Error):
    """
    Raised when searching the database fails.
    """
    def __init__(self):
        pass
