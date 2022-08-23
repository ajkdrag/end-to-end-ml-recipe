import pandas as pd
from fastapi import FastAPI
from emp_burnout.core.parser.cfg_model import Config
from emp_burnout.core.parser.cfg_parser import load_config
from emp_burnout.launcher import main


app = FastAPI()


@app.post("/job/{config_path:path}")
async def run_job(config_path: str):
    config = load_config(config_path)
    main(config)
    return {"run_id": config.run_id}


@app.post("/predict/")
async def predict_single(rqst: dict):
    config = Config(
        job_name="single_predict",
        job_type="PredictJob",
        data_dir="",
        save_results=False,
    )
    df = pd.DataFrame([rqst])
    results = main(config, df=df)
    return {"run_id": config.run_id, **results}
