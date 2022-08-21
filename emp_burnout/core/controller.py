from dataclasses import dataclass
from typing import Optional
from .jobs.train import TrainJob
from .jobs.predict import PredictJob


@dataclass
class JobController:
    config: dict
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
        job_type = self.config["job_type"]
        job = self._get_job_from_job_type(job_type)
        return job.run()
