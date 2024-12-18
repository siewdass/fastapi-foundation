from importlib import import_module
from os import path, getcwd, walk
from lib import Router, HttpException, httpException
from fastapi import FastAPI

def loadLibrary(cls_type):
	m = []
	base_dir = getcwd()
	ignore_dirs = ['__pycache__', '.vscode', '.venv']
	for root, dirs, files in walk(base_dir):
		dirs[:] = [d for d in dirs if d not in ignore_dirs]
		py_files = [f for f in files if f.endswith('.py') and f != '__init__.py']

		for py_file in py_files:
			module_path = path.relpath(root, base_dir).replace(path.sep, '.')
			module_name = py_file[:-3]
			try:
				imported = import_module(f"{module_path}.{module_name}" if module_path != '.' else module_name)
				for obj in vars(imported).values():
					if isinstance(obj, type) and issubclass(obj, cls_type) and obj is not cls_type:
						if obj not in m:
							m.append(obj)
			except Exception as e:
				print(f"Error importing {module_name}: {e}")
	return m

def loadRouters(app: FastAPI):
	app.add_exception_handler(HttpException, httpException)
	for router in loadLibrary(Router):
		for route in router().__routes__:
			app.router.routes.append(route)
