from fastapi import FastAPI
from uvicorn import run
from contextlib import asynccontextmanager
from database import connect
from util import load_modules

uri = 'mongodb://root:toor@192.168.0.100/?authSource=admin'

@asynccontextmanager
async def lifespan(app: FastAPI):
    m = load_modules()
    db = await connect(uri=uri, database='dan', models=m['models'])
    for router in m['routes']:
        app.include_router(router)
    yield
    db.close()

app = FastAPI(lifespan=lifespan)
run(app, host='0.0.0.0', port=8000)