from fastapi import HTTPException, Request, FastAPI
from fastapi.routing import APIRoute
from typing import Callable, Type, Optional
from pydantic import BaseModel, ValidationError
from inspect import getmembers, ismethod, signature
from logging import getLogger, StreamHandler, INFO
from colorlog import ColoredFormatter

logger = getLogger()
handler = StreamHandler()

formatter = ColoredFormatter(
    '%(log_color)s%(levelname)s%(reset)s:     %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    reset=True,
    log_colors={ 'DEBUG': 'cyan', 'INFO': 'green', 'WARNING': 'yellow', 'ERROR': 'red', 'CRITICAL': 'bold_red' }
)

handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(INFO)

class Router:
    __routes__ = []

    def __init__(self):
        methods = [ 'GET', 'POST', 'PUT', 'DELETE' ]
        for name, method in getmembers(self, predicate=ismethod):
            for m in methods:
                if name.startswith(m.lower()):
                    path = ''
                    model: Optional[Type[BaseModel]] = None
                    endpoint: Callable = method

                    if name.upper() not in methods:
                        path = f'/{name[len(m):]}'.lower()

                    parameters = signature(method).parameters

                    for param in parameters.values():
                        if isinstance(param.annotation, type) and issubclass(param.annotation, BaseModel):
                            model = param.annotation
                            break

                    async def logging(request: Request):
                        data = None
                        if model:
                            try:
                                body = await request.json()
                                data = model(**body)
                            except ValidationError as e:
                                raise HTTPException(status_code=422, detail=e.errors())
                        
                        logger.info(f'Request received with parameters {data}')
                        return await endpoint(data if data else request)

                    self.__routes__.append(
                        APIRoute(path=self.prefix + path, endpoint=logging, methods=[m.upper()], name=endpoint.__name__)
                    )

    def register(self, app: FastAPI):
        for route in self.__routes__:
            app.router.routes.append(route)
