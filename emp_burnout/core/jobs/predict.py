import logging
import pandas as pd

from pathlib import Path
from pandas import DataFrame
from dataclasses import dataclass
from . import BaseJob
from ..libs.preprocessing import Preprocessor
from ..ingestion.ingest import ingest_dataset
from ...utils.io import load_obj
from ...utils import constants


LOG = logging.getLogger(__name__)


@dataclass
class PredictJob(BaseJob):
    df: DataFrame = None

    def __post_init__(self):
        super().__post_init__()
        self.save_results = self.config.save_results

    def _run(self):
        super()._run()
        LOG.info("Running Predict job...")
        preprocessor = Preprocessor()

        # ingest and load df
        if self.df is None:
            ingest_dataset(self.config, self.db_conn, training=False)
            self.df = pd.read_csv(
                Path(self.config.data_dir) / "cleaned" /"predict.csv"
            )
        
        # preprocess
        X, _ = preprocessor.preprocess(self.df, training=False)

        # load best model
        model = load_obj(next(Path(constants.MODEL_DIR).iterdir()))[1]

        # predict
        y = model.predict(X).tolist() if len(X) > 0 else []
        results = {"burn_rate": y}

        # save predictions
        if self.save_results:
            save_file = Path(self.config.data_dir) / "results" / "predictions.csv"
            save_file.parent.mkdir(exist_ok=True, parents=True)
            pd.DataFrame(results).to_csv(save_file, header=True, index=False)
            LOG.info("Saved prediction results to : %s", save_file)

        LOG.info("Finished Prediction job.")
        return results
