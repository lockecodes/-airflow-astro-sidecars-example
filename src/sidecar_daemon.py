"""
# Run a loop handling files until either the file mutex is gone, files are gone, or timeouts are met
########################################################################################################################
"""
import datetime
import os
import sys
from time import sleep
from pathlib import Path
from typing import List

OUTPUT_DIR = Path("/data")
MUTEX_FILE = Path(OUTPUT_DIR, "running-mutex")
UPLOAD_SIDE_CAR_TIME_OUT = 60


def upload_csvs(project: str, dataset: str):
    """
    Dummy upload function
    """
    now = datetime.datetime.now()
    paths = get_r_files_by_ts(ts=now)
    for path in paths:
        print(f"Would upload {path} to {project}.{dataset}")
        print(f"Deleting {path}")
        os.remove(path)


def get_r_files_by_ts(ts: datetime.datetime = None) -> List[Path]:
    """
    Get a list of file paths from the R output directory that are no newer than the timestamp passed.
    This skips locked files.

    :param ts: timestamp check for files equal to or older than this
    :return: List of files to upload
    """
    files = []
    for f in OUTPUT_DIR.iterdir():
        file_mtime = f.stat().st_mtime
        file_ts = datetime.datetime.fromtimestamp(file_mtime)
        if (
            f.name.endswith(".csv")
            and (not ts or file_ts <= ts)
            and not Path(OUTPUT_DIR, f"{f.name}.lock").exists()
        ):
            files.append(f)
    return files


def _flush_std():
    sys.stdout.flush()
    sys.stderr.flush()


def _should_stop_file_based(start: datetime.datetime) -> bool:
    now = datetime.datetime.utcnow()
    files = get_r_files_by_ts()
    if files:
        return False
    if MUTEX_FILE.exists():
        return False
    if now - start < datetime.timedelta(seconds=(UPLOAD_SIDE_CAR_TIME_OUT * 2)):
        return False
    return True


if __name__ == "__main__":
    global_start = datetime.datetime.utcnow()
    while True:
        start = datetime.datetime.utcnow()
        if _should_stop_file_based(global_start):
            print("Break out of the upload loop")
            break
        print("Running Upload CSVs")
        _flush_std()
        upload_csvs(project="dummy-project", dataset="dummy-dataset")
        _flush_std()
        sleep(UPLOAD_SIDE_CAR_TIME_OUT)
