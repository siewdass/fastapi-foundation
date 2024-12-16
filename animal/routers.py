from lib import Router
from .schemas import Request, Response
from .models import Animal

def validate(item: Request):
	return item

class AnimalRouter(Router):
	prefix: str = '/animal'
	dependencies: list = [ validate ]

	async def post(self, request: Request):
		animal = Animal(name=request.name, sound=request.sound)
		await animal.insert()
		return Response(message = 'created!')