"""
# Run a loop writing some csv files
########################################################################################################################
"""
import os
import sys
from time import sleep
from pathlib import Path

OUTPUT_DIR = Path("/data")
MUTEX_FILE = Path(OUTPUT_DIR, "running-mutex")
FILE_CREATE_TIMEOUT = 20


def _flush_std():
    sys.stdout.flush()
    sys.stderr.flush()


if __name__ == "__main__":
    try:
        for i in range(10):
            csv_file = Path(OUTPUT_DIR, f"{i}_names.csv")
            try:
                print(f"Creating file {csv_file}")
                _flush_std()
                csv_file.touch(mode=0o777)
            except IOError:
                print("I/O error")
                _flush_std()
            sleep(FILE_CREATE_TIMEOUT)
    finally:
        os.remove(MUTEX_FILE)
