from importlib import import_module
from os import listdir, path, getcwd

from beanie import Document
from lib import Router

modules = [ f for f in listdir(getcwd()) if path.isdir(path.join(getcwd(), f)) and f not in [ '__pycache__', '.vscode', '.git' ] ]

def load_modules():
    m = { 'models': [], 'routers': [] }
    
    for module in modules:
        for submodule in m.keys():
            try:
                imported = import_module(f"{module}.{submodule}")
                for obj in vars(imported).values():
                    if isinstance(obj, type):
                        if issubclass(obj, Document) and obj is not Document:
                            if obj not in m['models']:
                                m['models'].append(obj)
                        elif issubclass(obj, Router) and obj is not Router:
                            if obj not in m['routers']:
                                m['routers'].append(obj)
            except Exception as e:
                print(e)

    return m