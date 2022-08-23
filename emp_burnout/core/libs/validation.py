import logging
import pandas as pd
from pathlib import Path
from emp_burnout.core.parser.cfg_model import Config

LOG = logging.getLogger(__name__)


def validate(datasets_dir: Path):
    num_validated = 0
    for file_ in datasets_dir.iterdir():
        # validate file and then overwrite
        df = pd.read_csv(file_)
        df.fillna("NULL", inplace=True)
        df.to_csv(file_, index=None, header=True)
        num_validated += 1

    LOG.info("Successfully validated %s files.", num_validated)
