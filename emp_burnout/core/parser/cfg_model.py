from typing import List, Literal, Optional
from pydantic import root_validator, validator
from pydantic import BaseModel, Field
from emp_burnout.utils.general import gen_run_id


class Config(BaseModel):
    job_name: str
    job_type: Literal["TrainJob", "PredictJob"]
    data_dir: str
    save_results: Optional[bool] = None
    track: Optional[bool] = None
    hyps: Optional[dict] = None
    log_format: Literal["standard", "json"] = "standard"
    log_output: List[Literal["console", "logfile"]] = ["console"]
    run_id: str = Field(default_factory=gen_run_id)
    prev_run_id: str = ""

    @root_validator(pre=True)
    def check_illegal_attributes(cls, values):
        illegal_attrs_map = {
            "TrainJob": ["save_results"],
            "PredictJob": ["track", "hyps"]
        }
        for job, illegal_attrs in illegal_attrs_map.items(): 
            if values["job_type"] == job:
                for attr in illegal_attrs:
                    assert attr not in values, f"Illegal attribute {attr} provided for {job.value}"
        return values 

    @validator("track", always=True)
    def default_value_for_tracking(cls, v):
        return v if v is not None else False
        
    @validator("hyps", always=True)
    def default_value_for_hyps(cls, v):
        return v if v is not None else {} 
    
    @validator("save_results", always=True)
    def default_value_for_save_results(cls, v):
        return v if v is not None else True 
