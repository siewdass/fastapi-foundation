from database import connect, disconnect
from beanie import Document
from settings import Settings

from library import API, Router, loadLibrary

class MyApp(API):
	settings = Settings()

	async def onBoot(self):
		await connect(
			uri=self.settings.MONGO_URI,
			database=self.settings.DATABASE_NAME,
			models=loadLibrary(Document)
		)
		for router in loadLibrary(Router):
			router().register(app)
		yield
		await disconnect()

app = MyApp()
#from uvicorn import run
#run("main.app:app", host="0.0.0.0", port=8000, reload=True)
#deactivate
#rm -rf .venv
#python3 -m venv .venv
#source .venv/bin/activate
#pip install -r requirements.txt
#uvicorn main:app --reload --port 8000 --host 0.0.0.0

#hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
#if bcrypt.checkpw(password.encode('utf-8'), hashed):
#import jwt
#encoded_jwt = jwt.encode({"some": "payload"}, "secret", algorithm="HS256")
#jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
#{'some': 'payload'}