import yaml


def load_config(config_file):
    with open(config_file) as stream:
        return yaml.safe_load(stream)


def validate_config(config):
    pass

