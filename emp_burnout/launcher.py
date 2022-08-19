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


def init_logging(config):
    log_config = constants.LOG_CONFIG
    logger = log_utils.Logger(log_config, config)
    logger.setup()


def init_controller(config):
    job_controller = JobController(config)
    job_controller.run()


def main(config):
    init_config(config)
    init_logging(config)
    LOG.info(config)
    init_controller(config)


if __name__ == "__main__":
    config_file = "configs/predict.yml"
    hyps_file = "configs/hyps.yml"
    config = load_config(config_file)
    hyps = load_config(hyps_file)
    config["hyps"] = hyps

    main(config)
