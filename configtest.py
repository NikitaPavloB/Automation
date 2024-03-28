import pytest
import yaml
from checkers import checkout

with open("config.yaml") as f:
    data = yaml.safe_load(f)
@pytest.fixture()
def clear_folders():
    return checkout(f"rm -rf {data['FOLDER_TST']} {data['FOLDER_OUT']} {data['FOLDER_1']}", "")

@pytest.fixture()
def make_folders():
    return checkout(f"mkdir {data['FOLDER_TST']} {data['FOLDER_OUT']} {data['FOLDER_1']}", "")

@pytest.fixture()
def make_files():
    file_names = []
    for i in range (data["COUNT"]):
        checkout(f"cd {data['FOLDER_TST']} dd if=/dev/urandom of=file{i} bs=1M count=1 iflag=fullblock", "")
        file_names.append(f"file{i}")
    return file_names
