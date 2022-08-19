import os
import logging
import pandas as pd

from pathlib import Path
from . import BaseJob
from ..libs.preprocessing import Preprocessor
from ..ingestion.ingest import ingest_dataset
from ...utils.io import load_obj
from ...utils import constants


LOG = logging.getLogger(__name__)


class PredictJob(BaseJob):
    def _run(self):
        super()._run()
        LOG.info("Running Predict job...")
        preprocessor = Preprocessor(self.config)

        # ingest
        ingest_dataset(self.config, self.db_conn, training=False)
        
        # preprocess
        X, _ = preprocessor.preprocess(os.path.join(self.config["data_dir"], "cleaned", "predict.csv"), training=False)

        # load best model
        model = load_obj(next(Path(constants.MODEL_DIR).iterdir()))[1]

        # predict
        y = model.predict(X)
        result = pd.DataFrame({"prediction": y})
        
        # save predictions
        save_file = Path(self.config["data_dir"]) / "results" /"predictions.csv"
        save_file.parent.mkdir(exist_ok=True, parents=True)
        result.to_csv(save_file, header=True, index=False)

        LOG.info("Finished Prediction job.")