from library import Middleware, Request, Callable, HttpException
from jwt import decode
from settings import Settings
from user.model import User

settings = Settings()

class UserMiddleware(Middleware):

	async def onRequest(self, request: Request, next: Callable):
		if not request.url.path.startswith('/user'):
			bearer = request.headers.get('authorization').split(' ')[1]
			token = decode(bearer, settings.SECRET_KEY, algorithms=['HS256'])
			user = await User.find_one(User.email==token['email'])
			if user is None:
				raise HttpException(status=HttpException.Unauthorized, message="Unauthorized")
		return await next(request)