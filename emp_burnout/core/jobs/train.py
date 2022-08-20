import os
import pandas as pd
import logging

from pathlib import Path
from sklearn.model_selection import train_test_split


from . import BaseJob
from ..libs.tracking import ModelTracker
from ..libs.preprocessing import Preprocessor
from ..ingestion.ingest import ingest_dataset
from ..libs.model_selection import ModelSelector
from ...utils.io import save_obj
from ...utils import constants


LOG = logging.getLogger(__name__)


class TrainJob(BaseJob):
    def __post_init__(self):
        super().__post_init__()
        self.track = self.config.get("track", False)

    def _run(self):
        super()._run()
        LOG.info("Running Train job...")
        preprocessor = Preprocessor(self.config)
        model_selector = ModelSelector(self.config)

        # ingest and load df
        ingest_dataset(self.config, self.db_conn)
        df = pd.read_csv(os.path.join(self.config["data_dir"], "cleaned", "train.csv"))

        # preprocess
        X, y = preprocessor.preprocess(df)

        # train-test split
        x_train, x_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=0
        )

        # getting the best model
        best_model = model_selector.get_best_model(x_train, y_train, x_test, y_test)
        params = {
            "best_model": best_model[0],
        }
        params.update(best_model[-2])

        # save model
        save_obj(
            best_model,
            Path(constants.MODEL_DIR) / f"{best_model[0]}.pkl",
            empty_dir=True,
        )

        # track run
        if self.track:
            LOG.info("Tracking params, metrics and artifacts for run: %s", self.run_id)
            model_tracker = ModelTracker(self.config, "emp_burnout")
            model_tracker.track_model_params(params, name=self.run_id)
            model_tracker.track_model_metrics(best_model[-1], name=self.run_id)
            model_tracker.track_model_artifacts(constants.MODEL_DIR, name=self.run_id)

        LOG.info("Finished Train job.")
        return best_model
