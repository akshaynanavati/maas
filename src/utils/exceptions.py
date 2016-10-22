class HTTPException(Exception):
    status_code = None

    def __init__(self, message):
        if not self.status_code:
            raise NotImplementedError('Child class must implement status_code.')
        self.message = message

    def to_json(self):
        return {'error_message': self.message}


class NotFoundException(HTTPException):
    status_code = 404


class BadRequest(HTTPException):
    status_code = 400


class InsufficientStorage(HTTPException):
    status_code = 507

class InternalServerError(HTTPException):
    status_code = 500
