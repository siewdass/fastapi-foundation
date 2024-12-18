from lib import Router, HttpResponse, HttpException
from .schemas import Body
from .models import Animal

class AnimalRouter(Router):
	prefix: str = '/animal'

	async def post(self, body: Body):
		animal = Animal(name=body.name, sound=body.sound)
		await animal.insert()
		#raise HttpException(status=HttpException.BadRequest, message='error!')
		return HttpResponse(status=HttpResponse.Ok, message='created!')
