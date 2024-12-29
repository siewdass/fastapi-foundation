from library import Schema, EmailStr, Field 

class UserSchema(Schema):
	email: EmailStr
	password: str = Field(min_length=6, max_length=32)
