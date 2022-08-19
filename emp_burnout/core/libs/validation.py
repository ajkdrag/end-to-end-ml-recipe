import logging
import pandas as pd
from pathlib import Path

LOG = logging.getLogger(__name__)


def validate(config):
    data_dir = Path(config["data_dir"])
    datasets_dir = data_dir / "datasets"

    num_validated = 0
    for file_ in datasets_dir.iterdir():
        # validate file and then overwrite
        df = pd.read_csv(file_)
        df.fillna('NULL', inplace=True)
        df.to_csv(file_, index=None, header=True)
        num_validated += 1

    LOG.info("Successfully validated %s files.", num_validated)
