from .schemas import UserSchema
from .models import User
from bcrypt import checkpw, hashpw, gensalt 
from jwt import encode, decode
from library import Router, HttpException, HttpResponse
from settings import Settings

settings = Settings()

class UserRouter(Router):
	prefix = '/user' 

	async def postSignUp(self, body: UserSchema):
		#try:
			user = await User.find_one(User.email==body.email)
			if user is not None:
				raise HttpException(status=HttpException.BadRequest, message='user already exists', aa=1)
			password = hashpw(body.password.encode('utf-8'), gensalt())
			user = User(email=body.email, password=password)
			await user.insert()
			return HttpResponse(status=HttpResponse.Ok, message='user created!')
		#except HttpException as error:
		#	raise error
		#except Exception as error:
		#	return HttpException(status=HttpException.ServerError, message='unknown error')

	async def postSignIn(self, body: UserSchema):
		try:
			user = await User.find_one(User.email==body.email)
			if user is None:
				raise HttpException(status=HttpException.BadRequest, message='user not exists')
			checked = checkpw(body.password.encode('utf-8'), user.password)
			if checked is False: 
				raise HttpException(status=HttpException.BadRequest,message='password invalid')
			token = encode(user, settings.SECRET_KEY, algorithms=['HS256'])
			return HttpResponse(status=HttpResponse.Ok, message=token)
		except HttpException as error:
			raise error
		except Exception as error:
			return HttpException(status=HttpException.ServerError, message='unknow error')	




#import jwt
#encoded_jwt = jwt.encode({"some": "payload"}, "secret", algorithm="HS256")
#jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
