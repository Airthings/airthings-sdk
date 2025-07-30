"""Module providing an Airthings API SDK errors."""


class UnexpectedStatusError(Exception):
    """Unexpected status error."""

    message = "Unexpected status code received from Airthings API."

    def __init__(self, status_code: int, content: bytes):
        self.status_code = status_code
        self.content = content.decode("utf-8")
        super().__init__(f"{self.message} Status code: {status_code}, content: {self.content}")


class UnexpectedPayloadError(Exception):
    """Unexpected payload error."""

    message = "Unexpected payload received from Airthings API."

    def __init__(self, payload: bytes):
        self.payload = payload.decode("utf-8")
        super().__init__(f"{self.message} Payload: {self.payload}")


class ApiError(Exception):
    """Airthings API error."""

    message = "Received an error response from Airthings API."

    def __init__(self, error: str):
        self.error = error
        super().__init__(f"{self.message} Error: {error}")
