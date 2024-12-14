from importlib import import_module
from beanie import Document
from lib import Router
from os import listdir, path, getcwd

excluded = { '__pycache__', '.vscode' }
current = getcwd()
modules = [ f for f in listdir(current) if path.isdir(path.join(current, f)) and f not in excluded ]

def load_modules():
    m = { 'models': [], 'routes': [] }
    
    for module in modules:
        for submodule in m.keys():
            try:
                imported = import_module(f"{module}.{submodule}")
                for obj in vars(imported).values():
                    if isinstance(obj, type):
                        if issubclass(obj, Document) and obj is not Document:
                            if obj not in m["models"]:
                                m["models"].append(obj)
                        elif issubclass(obj, Router) and obj is not Router:
                            instance = obj(f'/{module}')
                            if instance not in m["routes"]:
                                m["routes"].append(instance)
            except:
                pass 

    return m