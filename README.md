# End-to-End-ML-Recipe (employee burnout prediction)

## Setup conda env
Setup conda virtual environment from the environment.yml file of this repo.
```bash
conda env create -f environment.yml
conda activate emp_burnout
```

## Setup package env
Install the codebase as a package (setup.py)
```bash
pip install .
```

## Usage
- For running the servers (MLFlow server, Minio, NGINX), start docker-compose as:
    ```bash
    docker-compose up 
    ```
    - Make sure to configure the volumes (check host paths) in the docker-compose.yml file as needed.
    - The server is only needed for tracking purposes. If you don't need mlflow tracking, you can opt to ignore this step.

- For the client REST apis, start the app with uvicorn using:
    ```bash
    uvicorn emp_burnout.app:app
    ```
- Head over to `localhost:8000/docs` to view the swagger ui for the exposed REST apis.
- For the job config files, refer to `configs/train.yml` and `configs/predict.yml`.
    - The `train.yml` also contains the hyperparameters for training. One can modify them too.

## TODOS:
- [x] Groundwork
- [x] Environment setup
- [x] Ingestion to DB
- [x] Docker setup
- [x] MLFlow Server setup
- [x] Training Job
- [x] Batch prediction Job
- [x] Single input prediction Job
- [x] Cleanup
- [x] Pydantic config parsing
- [x] REST APIs
- [x] Update README
