from fastapi import HTTPException, Request, FastAPI
from fastapi.routing import APIRoute
from typing import Callable, Type, Optional
from pydantic import BaseModel, ValidationError
import inspect
import logging
from colorlog import ColoredFormatter

logger = logging.getLogger()
handler = logging.StreamHandler()

formatter = ColoredFormatter(
    "%(log_color)s%(levelname)s%(reset)s:     %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    reset=True,
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    }
)

handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class Router:
    methods = [ 'GET', 'POST', 'PUT', 'DELETE' ]
    routes = []

    def __init__(self):
        for name, method in inspect.getmembers(self, predicate=inspect.ismethod):
            for m in self.methods:
                if name.startswith(m.lower()):
                    path = ''
                    model: Optional[Type[BaseModel]] = None
                    endpoint: Callable = method

                    if name.upper() not in self.methods:
                        path = f'/{name[len(m):]}'.lower()

                    signature = inspect.signature(method)

                    for param in signature.parameters.values():
                        if isinstance(param.annotation, type) and issubclass(param.annotation, BaseModel):
                            model = param.annotation
                            break

                    async def logging(request: Request, path=path, m=m.upper(), endpoint=endpoint, model=model):
                        data = None
                        if model:
                            try:
                                body = await request.json()
                                data = model(**body)
                            except ValidationError as e:
                                raise HTTPException(status_code=422, detail=e.errors())
                        
                        logger.info(f'Request received at {self.prefix + path} with method {m}')
                        
                        if data:
                            return await endpoint(data)
                        else:
                            return await endpoint(request)

                    self.routes.append(
                        APIRoute(path=self.prefix + path, endpoint=logging, methods=[m.upper()], name=endpoint.__name__,)
                    )

    def register(self, app: FastAPI):
        for route in self.routes:
            app.router.routes.append(route)
