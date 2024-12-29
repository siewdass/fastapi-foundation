from user.schemas import UserSchema
from user.models import User
from bcrypt import checkpw, hashpw, gensalt 
from jwt import encode
from library import Router, HttpException, HttpResponse
from settings import Settings

settings = Settings()

class UserRouter(Router):
	prefix = '/user' 

	async def postSignUp(self, body: UserSchema):
		user = await User.find_one(User.email==body.email)
		if user is not None:
			raise HttpException(status=HttpException.BadRequest, message='user already exists')
		password = hashpw(body.password.encode('utf-8'), gensalt())
		user = User(email=body.email, password=password)
		await user.insert()
		return HttpResponse(status=HttpResponse.Ok, message='user created!')

	async def postSignIn(self, body: UserSchema):
		user = await User.find_one(User.email==body.email)
		if user is None:
			raise HttpException(status=HttpException.BadRequest, message='user not exists')
		checked = checkpw(body.password.encode('utf-8'), user.password.encode('utf-8'))
		if checked is False: 
			raise HttpException(status=HttpException.BadRequest,message='password invalid')
		token = encode({'email': user.email}, settings.SECRET_KEY, algorithm='HS256')
		return HttpResponse(status=HttpResponse.Ok, message=token)
