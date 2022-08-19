from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from emp_burnout.utils import constants
from emp_burnout.database.db_wrapper import (
    create_connection,
    create_table,
    insert_rows,
    update_cols,
    run_sql,
)
from emp_burnout.utils.general import load_schema


@dataclass
class BaseJob:
    config: dict

    def __post_init__(self):
        self.job_name = self.config["job_name"]
        self.job_type = self.config["job_type"]
        self.run_id = self.config["run_id"]
        self.db_conn = create_connection(constants.DB_NAME)
        self.config["prev_run_id"] = BaseJob._get_prev_run_id(
            self.db_conn, constants.JOB_CTRL_TABLE, self.run_id, self.job_type
        )

    @staticmethod
    def _get_prev_run_id(db_conn, table_name, run_id, job_type):
        sql_ = f"select coalesce(max(run_id), :curr_run_id) from {table_name} where run_id < :curr_run_id and job_type = :job_type"
        par_ = {
            "curr_run_id": run_id,
            "job_type": job_type,
        }
        return run_sql(db_conn, sql_, par_).fetchone()[0]

    def _mark_start(self):
        curr_time = datetime.now().isoformat()

        # create job control table if not there
        job_ctrl_schema = load_schema(constants.JOB_CTRL_TABLE)
        # TODO: remove arg drop_existing during call
        create_table(
            self.db_conn, constants.JOB_CTRL_TABLE, job_ctrl_schema, drop_existing=True
        )

        # update job control table with start time
        cols_to_insert_into = ["job_name", "job_type", "run_id", "start_time", "status"]
        values = [self.job_name, self.job_type, self.run_id, curr_time, "started"]
        insert_rows(self.db_conn, constants.JOB_CTRL_TABLE, cols_to_insert_into, values)

    def _mark_end(self, status):
        curr_time = datetime.now().isoformat()

        # update job control table with end time
        cols_to_update = ["end_time", "status"]
        values = [curr_time, status]
        where_cols = ["run_id"]
        where_values = [self.run_id]
        update_cols(
            self.db_conn,
            constants.JOB_CTRL_TABLE,
            cols_to_update,
            values,
            where_cols,
            where_values,
        )

    @abstractmethod
    def _run(self):
        pass

    def run(self):
        self._mark_start()
        try:
            self._run()
            status = "succeeded"
        except Exception:
            status = "failed"
            raise
        finally:
            self._mark_end(status)
            self.db_conn.close()
