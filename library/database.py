from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie, Document
from .util import loadLibrary

class MongoDB:
	URI: str = None
	client: AsyncIOMotorClient = None

	async def connect(self):
		self.client = AsyncIOMotorClient(self.URI)
		database = self.client.get_default_database()
		await init_beanie(database=database, document_models=loadLibrary(MongoModel))

	async def disconnect(self):
		if self.client is not None:
			self.client.close()

class MongoModel(Document):
	pass
