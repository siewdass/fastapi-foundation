from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from logging import getLogger

logger = getLogger('uvicorn')

class HttpException(HTTPException):
	def __init__(self, status: int, message: str, *args, **kwargs):
		kwargs['status_code'] = status
		kwargs['detail'] = message
		logger.error(f'HTTP Exception: {message}')
		super().__init__(*args, **kwargs)

	Found: int = 302
	BadRequest: int = 400
	Unauthorized: int = 401
	Forbidden: int = 403
	NotFound: int = 404
	NotAcceptable: int = 406
	Conflict: int = 409
	UnprocessableEntity: int = 422
	TooManyRequests: int = 429
	ServerError: int = 500
	NotImplemented: int = 501

def httpException(_: Request, exc: HttpException):
	return JSONResponse(status_code=exc.status_code, content={ 'message': exc.detail })

class HttpResponse(JSONResponse):
	def __init__(self, status: int, message: str, *args, **kwargs):
		kwargs['status_code'] = status
		kwargs['content'] = { 'message': message }
		logger.info(f'HTTP response {message}')
		super().__init__(*args, **kwargs)

	Ok: int = 200
	Created: int = 201
	Accepted: int = 202
	NoContent: int = 204