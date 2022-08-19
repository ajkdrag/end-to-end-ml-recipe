# model configs
MODEL_DIR = "emp_burnout/artifacts/models"
EXTRAS_DIR = "emp_burnout/artifacts/extras"

# db configs
DB_NAME = "emp_burnout"
DB_FILES_DIR = "emp_burnout/artifacts/dbs"
SCHEMAS_DIR = "emp_burnout/artifacts/schemas"
JOB_CTRL_TABLE = "job_ctrl"
TRAIN_TABLE = "train"
PREDICT_TABLE = "predict"

# logging configs
LOG_FILENAME = "runs.log"
LOG_EXTRA_ARGS = {}
LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s:%(name)s:%(process)d:%(lineno)d:%(levelname)s | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "standard": {
            "()": "emp_burnout.utils.logger.StandardFormatter",
            "extraArgs": LOG_EXTRA_ARGS,
        },
        "json": {
            "()": "emp_burnout.utils.logger.JsonFormatter",
            "extraArgs": LOG_EXTRA_ARGS,
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",  # can change to default/json
            "stream": "ext://sys.stdout",
        },
        "logfile": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_FILENAME,
            "formatter": "standard",  # can change to default/json
            "backupCount": 2,
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],  # can change to logfile
    },
}