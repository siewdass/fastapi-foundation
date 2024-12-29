from library import MongoModel, Field
from bcrypt import hashpw, gensalt 

class User(MongoModel):
	email: str = Field(unique=True)
	password: str

	async def onSeeding(self):
		user = await self.find_one(self.email == 'admin@mail.com')
		if not user:
			password = hashpw('123456'.encode('utf-8'), gensalt())
			user = self(email='admin@mail.com', password=password)
			await user.insert()