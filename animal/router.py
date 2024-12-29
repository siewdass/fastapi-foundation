from library import Router, HttpException, HttpResponse
from .schema import Body
from .model import Animal

class AnimalRouter(Router):
	prefix: str = '/animal'

	async def post(self, body: Body):
		animal = Animal(name=body.name, sound=body.sound)
		await animal.insert()
		#raise HttpException(status=HttpException.BadRequest, message='error!')
		return HttpResponse(status=HttpResponse.Ok, message='created!')
