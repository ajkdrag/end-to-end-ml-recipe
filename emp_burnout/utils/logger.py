import time
import json
import logging
import logging.config
from typing import Dict
from dataclasses import dataclass
from emp_burnout.utils import constants
from emp_burnout.utils.general import dict_replace_multiple


LOG = logging.getLogger(__name__)


class Singleton(type):
    _instances: Dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class BaseFormatter(logging.Formatter):
    def __init__(self, **kwargs):
        if "extraArgs" in kwargs:
            self.extraArgs = kwargs.get("extraArgs")
            del kwargs["extraArgs"]
        super().__init__(**kwargs)

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if not datefmt:
            datefmt = "%Y-%m-%d %H:%M:%S"
        return time.strftime(datefmt, ct)

    def formatException(self, exc_info):
        result = super().formatException(exc_info)
        if result:
            result = result.replace("\n", " ")
        return result


class StandardFormatter(BaseFormatter):
    def format(self, record):
        formatted_record = []
        record.message = record.getMessage()
        record.asctime = self.formatTime(record, self.datefmt)
        formatted_record.append(record.asctime)
        if self.extraArgs is not None:
            for val in self.extraArgs.values():
                formatted_record.append(val)
        for key in ["module", "funcName", "levelname"]:
            formatted_record.append(getattr(record, key))
        formatted_record.append(record.message)
        if record.exc_info:
            formatted_record.append(self.formatException(record.exc_info))
        return " | ".join(map(str, formatted_record))


class JsonFormatter(BaseFormatter):
    def format(self, record):
        formatted_record = dict()
        record.message = record.getMessage()
        record.asctime = self.formatTime(record, self.datefmt)
        formatted_record["created"] = record.asctime
        if self.extraArgs is not None:
            for key, val in self.extraArgs.items():
                formatted_record[key] = val
        for key in ["module", "funcName", "levelname"]:
            formatted_record[key] = getattr(record, key)
        formatted_record["message"] = record.message
        if record.exc_info:
            formatted_record["traceback"] = self.formatException(record.exc_info)
        return json.dumps(formatted_record, indent=4)


@dataclass
class Logger(metaclass=Singleton):
    log_config: dict
    job_config: dict

    def setup(self):
        keys = ["formatter", "filename"]
        vals = [self.job_config.get("log_format", "standard"), f"logs/{self.job_config['run_id']}.log"]
        dict_replace_multiple(self.log_config, keys, vals) 

        extra_args = {
            "job_name": self.job_config["job_name"],
        }
        handlers = self.job_config.get("log_output", ["console"])
        self.update_handlers(handlers)
        self.update_extra_args(extra_args)
        LOG.info("Logging setup completed.")

    def update_extra_args(self, extra_args):
        constants.LOG_EXTRA_ARGS.update(extra_args)
        logging.config.dictConfig(self.log_config)
        LOG.info("Updated logs with extra args: %s", extra_args)

    def update_handlers(self, handlers: list):
        constants.LOG_HANDLERS.clear()
        constants.LOG_HANDLERS += handlers
        logging.config.dictConfig(self.log_config)
        LOG.info("Updated default handlers with: %s", handlers)
