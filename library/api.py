from fastapi import FastAPI
from typing import AsyncGenerator
from .router import Router
from .responses import HttpException, httpException
from fastapi.middleware.cors import CORSMiddleware
from .util import loadLibrary
from logging import getLogger
from .middleware import Middleware

logger = getLogger('uvicorn')

class API(FastAPI):
	origins = [ '*' ]
	headers = [ '*' ]
	methods = [ '*' ]

	def __init__(self, **kwargs):
		super().__init__(lifespan=self.__lifespan__, **kwargs)
		self.add_exception_handler(HttpException, httpException)
		self.add_middleware(CORSMiddleware, allow_origins=self.origins, allow_methods=self.methods, allow_headers=self.headers)
		for middleware in loadLibrary(Middleware):
			self.add_middleware(middleware)

	async def onBoot(self):
		yield

	async def __lifespan__(self, _) -> AsyncGenerator:
		try:
			for router in loadLibrary(Router):
				for route in router().__routes__:
					self.router.routes.append(route)
			async for _ in self.onBoot():
				yield
		except Exception as e:
			logger.error(f'Exception: {e}')
			yield