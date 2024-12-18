from decouple import config

MONGO_URI = config('MONGO_URI', default='', cast=str)
SECRET_KEY = config('SECRET_KEY', default='', cast=str)
