from typing import Optional
from dataclasses import dataclass

from .jobs.train import TrainJob
from .jobs.predict import PredictJob
from emp_burnout.core.parser.cfg_model import Config


@dataclass
class JobController:
    config: Config
    kwargs: Optional[dict] = None

    def _get_job_from_job_type(self, job_type):
        if self.kwargs is None:
            self.kwargs = {}

        if job_type == "TrainJob":
            job = TrainJob(self.config, **self.kwargs)
        elif job_type == "PredictJob":
            job = PredictJob(self.config, **self.kwargs)

        return job

    def run(self):
        job = self._get_job_from_job_type(self.config.job_type)
        return job.run()
