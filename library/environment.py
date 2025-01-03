from decouple import RepositoryEnv
from inspect import get_annotations

class Environment:
	def __init__(self, DOTENV: str = '.env'):
		repo = RepositoryEnv(DOTENV)
		annotations = get_annotations(self.__class__)

		for key, type in annotations.items():
			if key in repo.data:
				value = repo.data[key]
				try:
					value = type(value)
				except (ValueError, TypeError):
					raise TypeError(f"can't convert '{value}' to '{key}' type '{type.__name__}'.")
				setattr(self, key, value)
