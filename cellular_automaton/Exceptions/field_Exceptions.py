class FieldException(Exception):
    """field exception"""

    def __init__(self, message: str):
        Exception.__init__(self, "Field Exception! " + f"with message: {message}")


class SpawnCellException(FieldException):
    """spawn cell exception"""

    def __init__(self, message: str, x: int = None, y: int = None):
        FieldException.__init__(self, message + f" with x: {x} and y: {y}" if x and y else "")


class GetCellException(FieldException):
    """get cell exception"""

    def __init__(self, message: str, x: int = None, y: int = None):
        FieldException.__init__(self, message + f" with x: {x} and y: {y}" if x and y else "")


class GetPatternCellException(FieldException):
    """get pattern cell exception"""

    def __init__(self, message: str, x: int = None, y: int = None):
        FieldException.__init__(self, message + f"with x: {x} and y: {y}" if x and y else "")


class DrawCellException(FieldException):
    """draw cell exception"""

    def __init__(self, message: str, x: int = None, y: int = None):
        FieldException.__init__(self, message + f" with x: {x} and y: {y}" if x and y else "")
