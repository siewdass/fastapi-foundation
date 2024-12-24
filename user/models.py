from library import MongoModel, Field

class User(MongoModel):
	email: str = Field(unique=True)
	password: str = Field(min_length=60, max_length=60)