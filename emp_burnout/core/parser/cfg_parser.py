import yaml
from .cfg_model import Config


def load_config(config_file, validate=True):
    with open(config_file) as stream:
        config = yaml.safe_load(stream)
        if validate:
            config = Config.parse_obj(config)
        return config
