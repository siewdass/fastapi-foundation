from lib import Router
from .schemas import Request, Response
from .models import Animal

class AnimalRouter(Router):
	prefix: str = '/animal'

	async def post(self, request: Request):
		animal = Animal(name=request.name, sound=request.sound)
		await animal.insert()
		return Response(message = 'tu animal se creo!')