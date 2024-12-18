from lib import Router
from .schemas import UserSchema
from .models import User
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from bcrypt import checkpw, hashpw, gensalt 

class UserRouter(Router):
	prefix = '/user' 

	async def postSignUp(self, body: UserSchema):
		try:
			user = await User.find_one(User.email==body.email)
			if user is not None:
				raise HTTPException(status_code=400, detail={'message': 'user already exists'})
			password = hashpw(body.password.encode('utf-8'), gensalt())
			user = User(email=body.email, password=password)
			await user.insert()
			return JSONResponse(status_code=200, content={'message': 'user created!'})
		except HTTPException as error:
			return error
		except Exception as error:
			return HTTPException(status_code=500, detail={'message': 'unknown error'})



#hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
#if bcrypt.checkpw(password.encode('utf-8'), hashed):
#import jwt
#encoded_jwt = jwt.encode({"some": "payload"}, "secret", algorithm="HS256")
#jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
#{'some': 'payload'}