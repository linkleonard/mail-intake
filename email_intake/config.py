from envparse import Env

env = Env(
    DATABASE_URL=str,
)
env.read_envfile()
