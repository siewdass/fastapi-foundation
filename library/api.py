from fastapi import FastAPI
from typing import AsyncGenerator
from .router import Router
from .responses import HttpException, httpException
from .loadLibrary import loadLibrary

class API(FastAPI):

	def __init__(self, **kwargs):
		super().__init__(lifespan=self.lifespan, **kwargs)
		self.add_exception_handler(HttpException, httpException)

	async def onBoot(self):
		yield

	async def lifespan(self, _) -> AsyncGenerator:
		for router in loadLibrary(Router):
			for route in router().__routes__:
				self.router.routes.append(route)
		async for _ in self.onBoot():
			yield