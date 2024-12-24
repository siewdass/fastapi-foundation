from database import Database
from library import API

class MyApp(API):

	async def onBoot(self):
		database = Database()
		await database.connect()
		yield
		await database.disconnect()

app = MyApp()

#deactivate
#rm -rf .venv
#python3 -m venv .venv
#source .venv/bin/activatefile:///home/sam/main.js

#pip install -r requirements.txt
#uvicorn main:app --reload --port 8000 --host 0.0.0.0