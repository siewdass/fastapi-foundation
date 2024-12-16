from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

async def connect(uri, database, models):
	client = AsyncIOMotorClient(uri)
	await init_beanie(database=client[database], document_models=models)
	return client