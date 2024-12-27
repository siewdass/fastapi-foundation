from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from typing import AsyncGenerator
from .router import Router
from .responses import HttpException, httpException
from .util import loadLibrary
from logging import getLogger

logger = getLogger('uvicorn')

class Middleware(BaseHTTPMiddleware):
	async def dispatch(self, request: Request, next):
		try:
			return await next(request)
		except Exception as e:
			logger.error(f'Exception: {e.args}')
			return JSONResponse(status_code=500, content={ 'message': e.args })

class API(FastAPI):

	def __init__(self, **kwargs):
		super().__init__(lifespan=self.__lifespan__, **kwargs)
		self.add_exception_handler(HttpException, httpException)
		self.add_middleware(Middleware)

	async def onBoot(self):
		yield

	async def __lifespan__(self, _) -> AsyncGenerator:
		for router in loadLibrary(Router):
			for route in router().__routes__:
				self.router.routes.append(route)
		async for _ in self.onBoot():
			yield