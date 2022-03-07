from pydantic import BaseModel

APP_NAME = "fastjwt"

# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

JWT_EXPIRE_MINUTES_DEFAULT = 30

# "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite-test.db"
DB_ARGS = {"check_same_thread": False}  # SQLITE ONLY

CORS_ORIGINS = [
    "http://localhost",
    "http://localhost:8080",
]


# TODO: need pydantic?


class LogConfig(BaseModel):

    LOGGER_NAME: str = APP_NAME.lower()
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        APP_NAME: {"handlers": ["default"], "level": LOG_LEVEL},
    }
