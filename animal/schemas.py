from pydantic import BaseModel

class Body(BaseModel):
	name: str
	sound: str
