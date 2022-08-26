from typing import Union
from datetime import datetime, date
from pydantic import BaseModel


class PredictModel(BaseModel):
    emp_id: str
    date_of_joining: Union[date, datetime]
    gender: str
    company_type: str
    wfh_setup_available: str
    designation: float
    resource_allocation: float
    mental_fatigue_score: float
