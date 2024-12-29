from library import Middleware, Request, Callable, HttpException
from jwt import decode
from settings import Settings
from user.model import User

settings = Settings()

class UserMiddleware(Middleware):

	async def onRequest(self, request: Request, next: Callable):
		if not request.url.path.startswith('/user'):
			token = request.headers.get('authorization').split(' ')[1]
			if token is None:
				raise HttpException(status=HttpException.Unauthorized, message="Unauthorized")
			email = decode(token, settings.SECRET_KEY)['email']
			user = await User.find_one(User.email==email)
			if user is None:
				raise HttpException(status=HttpException.Unauthorized, message="Unauthorized")
		return await next(request)