from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie, Document
from .util import loadLibrary
import types

class MongoDB:
	URI: str = None
	client: AsyncIOMotorClient = None

	async def connect(self):
		self.client = AsyncIOMotorClient(self.URI)
		database = self.client.get_default_database()
		models = loadLibrary(MongoModel)
		await init_beanie(database=database, document_models=models)
		for model in models:
			bound = types.MethodType(model.onSeeding, model)
			await bound()

	async def disconnect(self):
		if self.client is not None:
			self.client.close()

class MongoModel(Document):

	async def onSeeding(self):
		pass