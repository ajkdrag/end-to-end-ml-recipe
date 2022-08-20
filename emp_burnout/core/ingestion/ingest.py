import logging
import pandas as pd
from pathlib import Path
from emp_burnout.core.jobs import train
from emp_burnout.database.db_wrapper import create_table, export_table
from emp_burnout.core.libs.validation import validate
from emp_burnout.utils import constants
from emp_burnout.utils.general import load_schema
from emp_burnout.utils.io import move_files

LOG = logging.getLogger(__name__)


def archive_old_files(data_dir, prev_run_id):
    folders_to_archive = ("rejects", "cleaned", "processed", "results")
    for folder in folders_to_archive:
        LOG.info("Archiving old %s files.", folder)
        folder_path = Path(data_dir) / folder
        dest_path = Path(data_dir) / "archives" / f"{prev_run_id}_{folder}"
        num_archived = move_files(folder_path, dest_path)
        LOG.info("Archived %s files from folder: %s.", num_archived, folder)


def load_file_to_table(file_path, db_conn, table_name, columns):
    df = pd.read_csv(file_path, skiprows=1, header=None, names=columns)
    df.to_sql(table_name, db_conn, if_exists="append", index=False)
    LOG.info("Successfully loaded %s rows into table: %s", len(df), table_name)


def load_data_to_table(config, db_conn, table_name, columns):
    datasets_dir = Path(config["data_dir"]) / "datasets"
    for file_ in datasets_dir.iterdir():
        load_file_to_table(file_, db_conn, table_name, columns)


def ingest_dataset(config, db_conn, training=True):
    data_dir = config["data_dir"]
    datasets_dir = Path(data_dir) / "datasets"
    processed_dir = Path(data_dir) / "processed"
    cleaned_dir = Path(data_dir) / "cleaned"

    # 1. Archive old files
    archive_old_files(data_dir, config["prev_run_id"])

    # 2. Load schema from schema file
    table = constants.TRAIN_TABLE
    if not training:
        table = constants.PREDICT_TABLE
    schema = load_schema(table)

    # 3. Validate current csv file
    validate(config)

    # 4. Load data into resp. table
    # persist training table, but not prediction table
    create_table(
        db_conn, table, schema, drop_existing=(not training)
    )  
    load_data_to_table(config, db_conn, table, schema.keys())

    # 5. Move current csv files to processed dir
    move_files(datasets_dir, processed_dir)

    # 6. Export all data from training table to a file
    export_file = cleaned_dir / f"{table}.csv"
    export_table(db_conn, table, schema.keys(), export_file)
