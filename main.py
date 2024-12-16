from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import connect
from util import loadLibrary
from beanie import Document
from lib	import Router

uri = 'mongodb://root:toor@192.168.0.100/?authSource=admin'

@asynccontextmanager
async def lifespan(app: FastAPI):
	db = await connect(uri=uri, database='dan', models=loadLibrary(Document))
	for router in loadLibrary(Router):
		router().register(app)
	yield
	db.close()

app = FastAPI(lifespan=lifespan)

from uvicorn import run
#run(app, host='0.0.0.0', port=8000)