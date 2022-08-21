import logging
import emp_burnout.utils.logger as log_utils
from emp_burnout.core.controller import JobController
from emp_burnout.utils import constants
from emp_burnout.utils.general import gen_run_id
from emp_burnout.core.parser.cfg_parser import load_config

LOG = logging.getLogger(__name__)


def init_config(config):
    run_id = gen_run_id()
    config["run_id"] = run_id
    LOG.info(config)


def init_logging(config):
    log_config = constants.LOG_CONFIG
    logger = log_utils.Logger(log_config, config)
    logger.setup()
    return logger


def init_controller(config, **kwargs):
    job_controller = JobController(config, kwargs)
    return job_controller


def main(config, **kwargs):
    init_config(config)
    init_logging(config)
    job_controller = init_controller(config, **kwargs)
    return job_controller.run()


if __name__ == "__main__":
    config_file = "configs/train.yml"
    hyps_file = "configs/hyps.yml"
    config = load_config(config_file)
    hyps = load_config(hyps_file)
    config["hyps"] = hyps

    results = main(config)
    LOG.info("Results: %s", results)
