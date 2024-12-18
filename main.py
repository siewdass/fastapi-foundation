from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import connect
from util import loadLibrary, loadRouters
from beanie import Document
from settings import MONGO_URI

@asynccontextmanager
async def lifespan(app: FastAPI):
	models = loadLibrary(Document)
	db = await connect(uri=MONGO_URI, database='dan', models=models)
	yield
	db.close()

app = FastAPI(lifespan=lifespan)
loadRouters(app)

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