from decouple import RepositoryEnv

class Environment:
	def __init__(self, DOTENV: str = '.env'):
		repo = RepositoryEnv(DOTENV)
		for key, value in repo.data.items():
			setattr(self, key, value)