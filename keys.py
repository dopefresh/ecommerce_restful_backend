from environs import Env

env = Env()
env.read_env()

SECRET_KEY = env.str('SECRET_KEY')
DB_NAME = env.str('DB_NAME')
DB_USER = env.str('DB_USER')
DB_PASSWORD = env.str('DB_PASSWORD')


