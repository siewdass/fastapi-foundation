from library import Model, Field

class User(Model):
	email: str = Field(unique=True)
	password: str = Field(min_length=60, max_length=60)