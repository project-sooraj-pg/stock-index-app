class ApplicationException(Exception):
    def __init__(self, message="Application error", status_code=500):
        super().__init__(message)
        self.status_code = status_code
        self.message = message
