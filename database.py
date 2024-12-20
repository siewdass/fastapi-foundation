from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

client: AsyncIOMotorClient = None

async def connect(uri, database, models):
	client = AsyncIOMotorClient(uri)
	await init_beanie(database=client[database], document_models=models)

async def disconnect():
	if client is not None:
		client.close()