from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from typing import Callable

class Middleware(BaseHTTPMiddleware):

	async def onRequest(self, request: Request, next: Callable):
		print('ssss')
		return await next(request)

	async def dispatch(self, request: Request, next: Callable):
		return await self.onRequest(request, next)
