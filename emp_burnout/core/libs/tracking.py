import os
import mlflow
from dataclasses import dataclass


@dataclass
class ModelTracker:
    config: dict
    exp: str
    run_id = None

    def __post_init__(self) -> None:
        mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URI"])
        self.exp_id = mlflow.set_experiment(experiment_name=self.exp).experiment_id
    
    def track_model_metrics(self, metrics, name=None):
        with mlflow.start_run(run_id=self.run_id, experiment_id=self.exp_id, run_name=name) as run:
            mlflow.log_metrics(metrics)
            self.run_id = run.info.run_id
    
    def track_model_artifacts(self, artifacts, name=None):
        with mlflow.start_run(run_id=self.run_id, experiment_id=self.exp_id, run_name=name) as run:
            mlflow.log_artifacts(artifacts)
            self.run_id = run.info.run_id
    
    def track_model_params(self, params, name=None):
        with mlflow.start_run(run_id=self.run_id, experiment_id=self.exp_id, run_name=name) as run:
            mlflow.log_params(params)
            self.run_id = run.info.run_id


            

    
        

