from fastapi import Request, FastAPI, Depends, HTTPException
from fastapi.routing import APIRoute
from fastapi.responses import JSONResponse
from typing import Callable, Type, Optional
from pydantic import BaseModel, ValidationError
from inspect import getmembers, ismethod, signature
from logging import getLogger

logger = getLogger('uvicorn')

class HttpException(HTTPException):
	def __init__(self, status: int, message: str, *args, **kwargs):
		kwargs['status_code'] = status
		kwargs['detail'] = message
		logger.warning(f'HTTP Exception: {message}')     
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

async def httpException(_, e: HttpException):
	return JSONResponse(status_code=e.status_code, content={ 'status_code': e.status_code, 'message': e.detail })

class HttpResponse(JSONResponse):
	def __init__(self, status: int, message: str, *args, **kwargs):
		kwargs['status_code'] = status
		kwargs['content'] = { 'status_code': status, 'message': message }
		logger.info(f'HTTP response {message}')
		super().__init__(*args, **kwargs)

	Ok: int = 200
	Created: int = 201
	Accepted: int = 202
	NoContent: int = 204

class Router:
	prefix: str = ''
	__routes__: list = []
	dependencies: list = []

	def __init__(self):
		methods = [ 'GET', 'POST', 'PUT', 'DELETE' ]
		for name, method in getmembers(self, predicate=ismethod):
			for m in methods:
				if name.startswith(m.lower()):
					path = ''
					model: Optional[Type[BaseModel]] = None
					endpoint: Callable = method

					if name.upper() not in methods:
						path = f'/{name[len(m):]}'.lower()

					parameters = signature(method).parameters

					for param in parameters.values():
						if isinstance(param.annotation, type) and issubclass(param.annotation, BaseModel):
							model = param.annotation
							break

					async def logging(request: Request):
						data = None
						if model:
							try:
								body = await request.json()
								data = model(**body)
							except ValidationError as e:
								error_messages = [f"Missing field: {err['loc'][0]}, Error: {err['msg']}" for err in e.errors()]
								error_message = " | ".join(error_messages)
								raise HttpException(status=HttpException.UnprocessableEntity, message=error_message)
					
						logger.info(f'HTTP Request {data}')
						return await endpoint(data if data else request)

					self.__routes__.append(
						APIRoute(
							path=self.prefix + path,
							endpoint=logging,
							methods=[m.upper()],
							name=endpoint.__name__,
							dependencies=[Depends(dep) for dep in self.dependencies] if self.dependencies else []
						)
					)