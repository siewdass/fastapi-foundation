from settings import Settings
from library import API, MongoDB

settings = Settings()

class MyApp(API):

	async def onBoot(self):
		db = MongoDB(settings.MONGO_URI)
		await db.connect()
		yield
		await db.disconnect()

app = MyApp()

#deactivate
#rm -rf .venv
#python3 -m venv .venv
#source .venv/bin/activate
#pip install -r requirements.txt
#uvicorn main:app --reload --port 8000 --host 0.0.0.0
