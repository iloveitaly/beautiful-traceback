from environs import Env

env = Env()

with env.prefixed("BEAUTIFUL_TRACEBACK_"):
    ENABLED: bool | None = env.bool("ENABLED", default=None)
    LOCAL_STACK_ONLY: bool | None = env.bool("LOCAL_STACK_ONLY", default=None)
    SHOW_ALIASES: bool | None = env.bool("SHOW_ALIASES", default=None)
