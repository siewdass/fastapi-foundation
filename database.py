from library import MongoDB
from settings import Settings

settings = Settings()

class Database(MongoDB):
	URI: str = settings.MONGO_URI
