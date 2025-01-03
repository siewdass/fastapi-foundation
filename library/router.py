from fastapi import Request, Depends
from fastapi.routing import APIRoute
from typing import Callable, Type, Optional
from pydantic import BaseModel, ValidationError
from inspect import getmembers, ismethod, signature
from logging import getLogger
from .responses import HttpException

logger = getLogger('uvicorn')

class Router:
	prefix: str = ''
	dependencies: list = []
	__routes__: list = []

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

					def create(endpoint: Callable, method: str, path: str, model: Optional[Type[BaseModel]]):
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

						return APIRoute(
							path=self.prefix + path,
							endpoint=logging,
							methods=[method.upper()],
							name=endpoint.__name__,
							dependencies=[Depends(dep) for dep in self.dependencies] if self.dependencies else []
						)

					self.__routes__.append(create(endpoint, m, path, model))
