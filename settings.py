from decouple import config

MONGO_URI = config('MONGO_URI', default='', cast=str)
