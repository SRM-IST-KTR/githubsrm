"""
File to rotate generated logs.
"""

import os
from pathlib import Path
from zipfile import ZipFile

import shutil


def get_folder_name(parent_folder):
    from datetime import datetime

    current_time = datetime.today()
    return (
        f"{parent_folder}_{current_time.strftime('%y-%m-%d')}_{current_time.hour}.zip"
    )


def rotate():
    """Using custom rollover function since `logging.handlers.RotatingFileHandler
    doesn't allow the flexibility of compression and has the constraint of backupCount
    slowing anti-automating the process in someways."""

    parent_path = Path(__file__).resolve().parent.parent.parent
    log_path = os.path.join(parent_path, "logs")
    size = 0
    max_size = 1000000
    log_files = []

    if os.path.exists(log_path):
        for file in os.scandir(log_path):
            log_files.append(file)
            size += os.path.getsize(file)

    if size > max_size:
        zip_path = get_folder_name(os.path.join(parent_path, "archives"))
        with ZipFile(zip_path, "w") as f:
            for file in log_files:
                print(f"Zipping {file.name}")
                f.write(file)

        shutil.rmtree(log_path)
        os.mkdir(log_path)
        for file in log_files:
            os.mknod(os.path.join(log_path, file))


if __name__ == "__main__":
    rotate()
