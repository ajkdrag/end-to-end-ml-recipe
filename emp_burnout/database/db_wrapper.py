import csv
import os
from pathlib import Path
import sqlite3
import logging
from emp_burnout.utils import constants
from ..utils.general import place_holder


LOG = logging.getLogger(__name__)


def run_sql(conn, sql_, *args):
    LOG.info("Running sql: %s", sql_)
    with conn:
        return conn.execute(sql_, *args)


def create_connection(database):
    try:
        db_path = os.path.join(constants.DB_FILES_DIR, f"{database}.db")
        LOG.info("Connecting to databse: %s", db_path)
        conn = sqlite3.connect(db_path)
        LOG.info("Opened %s database successfully.", database)
        return conn
    except ConnectionError as exc:
        LOG.info("Failed to connect to database:%s.\nError: %s", database, exc)
        raise


def create_table(db_conn, table_name, column_names, drop_existing=False):
    try:
        if drop_existing:
            sql_ = f"DROP TABLE IF EXISTS {table_name};"
            run_sql(db_conn, sql_)

        sql_ = (
            "SELECT count(name) FROM sqlite_master WHERE type = :type AND name = :tbl"
        )
        par_ = {"type": "table", "tbl": table_name}
        result = run_sql(db_conn, sql_, par_).fetchone()[0]

        if result == 1:
            LOG.info("Table %s already exists.", table_name)
            desc = run_sql(db_conn, f"PRAGMA table_info({table_name})").fetchall()

            existing_cols = {fields[1] for fields in desc}
            curr_schema_cols = set(column_names.keys())
            missing_cols = curr_schema_cols - existing_cols
            for col in missing_cols:
                col_type = column_names[col]
                sql_ = f"ALTER TABLE {table_name} ADD COLUMN {col} {col_type}"
                run_sql(db_conn, sql_)
                LOG.info("Added missing col: %s to table %s.", col, table_name)
        else:
            LOG.info("Table %s doesn't exist. Creating...", table_name)
            cols = ",".join(
                [f"{col} {col_type.lower()}" for col, col_type in column_names.items()]
            )
            sql_ = f"CREATE TABLE {table_name} ( {cols} )"
            run_sql(db_conn, sql_)
            LOG.info("Successfully created table %s.", table_name)

    except Exception as exc:
        LOG.error("Failure during table %s creation.\nError: %s", table_name, exc)
        raise


def insert_rows(db_conn, table_name, columns, values):
    cols = ",".join(columns)
    ph = place_holder(columns)

    sql_ = f"INSERT INTO {table_name} ( {cols} ) VALUES ( {ph} )"
    run_sql(db_conn, sql_, values)


def update_cols(db_conn, table_name, columns, values, where_columns, where_values):
    set_clause = place_holder(columns, type="set")
    where_clause = place_holder(where_columns, type="set", delim="AND")

    sql_ = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
    run_sql(db_conn, sql_, values + where_values)


def export_table(db_conn, table_name, columns, out_file):
    sql_ = f"SELECT * FROM {table_name}"
    Path(out_file).parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, mode="w") as stream:
        writer = csv.writer(stream)
        writer.writerow(columns)
        writer.writerows(run_sql(db_conn, sql_))