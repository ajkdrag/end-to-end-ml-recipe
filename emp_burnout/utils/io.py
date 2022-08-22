import os
import time
import shutil
import pickle
from pathlib import Path


def move_file(file_:Path, dest_dir: Path):
    file_name = file_.name
    dest_dir.mkdir(parents=True, exist_ok=True)
    file_.replace(dest_dir / file_name)


def move_files(src_dir: Path, tgt_dir: Path):
    moved = 0
    if src_dir.exists():
        for file_ in src_dir.iterdir():
            move_file(file_, tgt_dir)
            moved += 1
    return moved


def save_obj(obj, tgt_file: Path, empty_dir=False):
    tgt_dir = tgt_file.parent
    if empty_dir and tgt_dir.exists():
        shutil.rmtree(tgt_dir)

    tgt_dir.mkdir(exist_ok=True, parents=True)
    with tgt_file.open("wb") as stream:
        pickle.dump(obj, stream)


def load_obj(src_file: Path):
    with src_file.open("rb") as stream:
        return pickle.load(stream)


def remove_old_subdirs(src_dir: Path, num_days=86400*7):
    now = time.time()
    removed = 0
    for el in src_dir.iterdir():
        if el.is_dir():
            timestamp = os.path.getmtime(el)
            if now - num_days > timestamp:
                try:
                    shutil.rmtree(el)  #uncomment to use
                    removed += 1
                except Exception as exc:
                    pass
    return removed