from dataclasses import dataclass
from .jobs.train import TrainJob
from .jobs.predict import PredictJob


@dataclass
class JobController:
    config: dict

    def _get_job_from_job_type(self, job_type):
        if job_type == "TrainJob":
            job = TrainJob(self.config)
        elif job_type == "PredictJob":
            job = PredictJob(self.config)

        return job

    def run(self):
        job_type = self.config["job_type"]
        job = self._get_job_from_job_type(job_type)
        job.run()
