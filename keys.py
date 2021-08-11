from environs import Env

env = Env()
env.read_env()

SECRET_KEY = env.str("SECRET_KEY")
DB_NAME = env.str("DB_NAME")
DB_USER = env.str("DB_USER")
DB_PASSWORD = env.str("DB_PASSWORD")
DB_HOST = env.str("DB_HOST")
DB_HOST_DOCKER = env.str("DB_HOST_DOCKER")
