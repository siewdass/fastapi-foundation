from beanie import Document
from pydantic import Field

class User(Document):
	email: str = Field(unique=True)
	password: str = Field(min_length=60, max_length=60)

