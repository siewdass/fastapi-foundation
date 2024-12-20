from library import Environment

class Settings(Environment):
	MONGO_URI: str 
	SECRET_KEY: str
	DATABASE_NAME: str