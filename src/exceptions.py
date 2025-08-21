

class ConnectionError(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidFile(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)