from fastapi import FastAPI
from typing import AsyncGenerator

class API(FastAPI):
	def __init__(self, **kwargs):
		super().__init__(lifespan=self.lifespan, **kwargs)

	async def onBoot(self):
		yield

	async def lifespan(self, _) -> AsyncGenerator:
		async for _ in self.onBoot():
			yield