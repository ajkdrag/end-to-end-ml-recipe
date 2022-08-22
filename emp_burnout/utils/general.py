import json
import random
from datetime import datetime
from pathlib import Path
from emp_burnout.utils import constants


def place_holder(input_list, type="insert", delim=", "):
    # Returns the place holder (?, ?, .....) as string
    if type == "insert":
        return delim.join("?" * len(input_list))
    elif type == "set":
        return delim.join([f"{item} = ?" for item in input_list])


def gen_run_id():
    now = datetime.now()
    date = now.date().strftime("%Y%m%d")
    curr_time = now.strftime("%H%M%S")
    rng = random.randint(100000, 999999)
    return f"{date}{curr_time}{rng}"


def dict_replace_multiple(dict_, list_keys, list_new_vals):
    for k, v in zip(list_keys, list_new_vals):
        for _ in find_keys(
                dict_,
                key=k,
                new_val=v,
            ):
                pass


def find_keys(node, key, new_val=None):
    if isinstance(node, list):
        for i in node:
            for x in find_keys(i, key, new_val):
                yield x
    elif isinstance(node, dict):
        if key in node:
            if new_val is not None:
                node[key] = new_val
            yield node[key]
        for j in node.values():
            for x in find_keys(j, key, new_val):
                yield x


def load_schema(schema_name):
    schema_file = Path(constants.SCHEMAS_DIR) / f"{schema_name}.json"
    with schema_file.open() as stream:
        schema = json.load(stream)
        return schema
