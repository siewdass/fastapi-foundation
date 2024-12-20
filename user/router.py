from .schemas import UserSchema
from .models import User
from bcrypt import checkpw, hashpw, gensalt 

from library import Router, HttpException, HttpResponse

class UserRouter(Router):
	prefix = '/user' 

	async def postSignUp(self, body: UserSchema):
		try:
			user = await User.find_one(User.email==body.email)
			if user is not None:
				raise HttpException(status=HttpException.BadRequest, message='user already exists')
			password = hashpw(body.password.encode('utf-8'), gensalt())
			user = User(email=body.email, password=password)
			await user.insert()
			return HttpResponse(status=HttpResponse.Ok, message='user created!')
		except HttpException as error:
			return error
		except Exception as error:
			return HttpException(status=HttpException.ServerError, message='unknown error')

#hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
#if bcrypt.checkpw(password.encode('utf-8'), hashed):
#import jwt
#encoded_jwt = jwt.encode({"some": "payload"}, "secret", algorithm="HS256")
#jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
#{'some': 'payload'}