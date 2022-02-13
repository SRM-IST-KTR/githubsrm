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
    parent_path = Path(__file__).resolve().parent.parent.parent
    log_path = os.path.join(parent_path, "logs")
    size = 0
    max_size = 1000000

    if os.path.exists(log_path):
        for file in os.scandir(log_path):
            size += os.path.getsize(file)

    if size > max_size:
        zip_path = get_folder_name(os.path.join(parent_path, "archives"))
        with ZipFile(zip_path, "w") as f:
            for file in os.scandir(log_path):
                print(f"Zipping {file.name}")
                f.write(file)

        shutil.rmtree(log_path)


if __name__ == "__main__":
    rotate()
