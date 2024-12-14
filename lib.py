from fastapi import APIRouter

class Router(APIRouter):

    def __init__(self, prefix: str = ""):
        super().__init__(prefix=prefix)

        for method in ["get", "post", "put", "delete"]:
            try:
                self.add_api_route("", getattr(self, method), methods=[method.upper()])
            except:
                pass