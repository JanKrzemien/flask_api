class HTTP_STATUS_CODE:
    OK = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    DATA_NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500

class API_EXCEPTION(Exception):
    def __init__(self, message = None, error = None) -> None:
        super().__init__(message)
        if error:
            self.error = error

class BAD_REQUEST_EXCEPTION(API_EXCEPTION):
    error = "Bad request, something unexpected went wrong but server is not on fire."
    status_code = HTTP_STATUS_CODE.BAD_REQUEST
class UNAUTHORIZED_EXCEPTION(API_EXCEPTION):
    error = "User unauthorized."
    status_code = HTTP_STATUS_CODE.UNAUTHORIZED
class DATA_NOT_FOUND_EXCEPTION(API_EXCEPTION):
    error = "Data not found."
    status_code = HTTP_STATUS_CODE.DATA_NOT_FOUND
class INTERNAL_ERROR_EXCEPTION(API_EXCEPTION):
    error = "Internal error, everything is on fire."
    status_code = HTTP_STATUS_CODE.INTERNAL_SERVER_ERROR