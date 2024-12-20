from decouple import RepositoryEnv
from inspect import get_annotations

class Environment:
	def __init__(self, DOTENV: str = '.env'):
		repo = RepositoryEnv(DOTENV)
		data = repo.data
		annotations = get_annotations(self.__class__)

		data = repo.data
		for key, type in annotations.items():
			if key in data:
				value = data[key]
				try:
					value = type(value)
				except (ValueError, TypeError):
					raise TypeError(f"La variable '{key}' no cumple con el tipo esperado '{type.__name__}'.")
				setattr(self, key, value)
