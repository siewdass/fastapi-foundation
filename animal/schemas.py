from pydantic import BaseModel

class Request(BaseModel):
  name: str
  sound: str

class Response(BaseModel):
  message: str