from lib import Router
from .schemas import Request, Response
from .models import Animal

class Rourter(Router):
	
	async def post(self, request: Request):
		print('animal', request)
		animal = Animal(name=request.name, sound=request.sound)
		await animal.insert()
		return Response(message = 'tu animal se creo!')