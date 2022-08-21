import pandas as pd
from fastapi import FastAPI
from emp_burnout.core.parser.cfg_parser import load_config
from emp_burnout.launcher import main


app = FastAPI()


@app.post("/train/{config_path:path}")
async def train(config_path: str):
    hyps_file = "configs/hyps.yml"
    config = load_config(config_path)
    hyps = load_config(hyps_file)
    config["hyps"] = hyps
    main(config)
    return {"run_id": config["run_id"]}


@app.post("/predict/")
async def predict_single(rqst: dict):
    config = {
        "job_name": "single_predict",
        "job_type": "PredictJob",
        "save_results": False
    }
    df = pd.DataFrame([rqst])
    results = main(config, df=df)
    return {"run_id": config["run_id"], **results}


@app.post("/predict/{config_path:path}")
async def predict(config_path: str):
    config = load_config(config_path)
    main(config)
    return {"run_id": config["run_id"]}