from fastapi import HTTPException


class BadRequestException(HTTPException):
    def __init__(self, message=None, status_code=400):
        super().__init__(status_code=status_code, detail=message)
