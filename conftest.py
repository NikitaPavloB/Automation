import pytest
import yaml
import os
import secrets
from checkers import checkout, getout
from datetime import datetime

with open('config.yaml') as f:
    data = yaml.safe_load(f)

@pytest.fixture()
def make_folders():
    cmd = "mkdir {} {} {} {}".format(data["folder_in"], data["folder_in"], data["folder_ext"], data["folder_ext2"])
    if checkout(cmd, ""):
        return True
    else:
        return False

@pytest.fixture()
def clear_folders():
    cmd = "rm -rf {}/* {}/* {}/* {}/*".format(data["folder_in"], data["folder_in"], data["folder_ext"], data["folder_ext2"])
    if checkout(cmd, ""):
        return True
    else:
        return False

@pytest.fixture()
def make_files():
    list_off_files = []
    for i in range(data["count"]):
        filename = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        cmd = "dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(os.path.join(data["folder_in"], filename), data["bs"])
        if checkout(cmd, ""):
            list_off_files.append(filename)
    return list_off_files

@pytest.fixture()
def make_subfolder():
    subfoldername = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(5))
    testfilename = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(5))
    if not os.path.exists(os.path.join(data["folder_in"], subfoldername)):
        os.mkdir(os.path.join(data["folder_in"], subfoldername))
    cmd = "dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(os.path.join(data["folder_in"], subfoldername, testfilename))
    if checkout(cmd, ""):
        return subfoldername, testfilename
    else:
        return None, None

@pytest.fixture(autouse=True)
def print_time():
    print("Start: {}".format(datetime.now().strftime("%H:%M:%S.%f")))
    yield
    print("Finish: {}".format(datetime.now().strftime("%H:%M:%S.%f")))

@pytest.fixture()
def make_bad_arx():
    cmd = "7z a {}/arxbad -t{}".format(data["folder_out"], data["type"])
    if checkout(cmd, "Everything is Ok"):
        cmd = "truncate -s 1 {}/arxbad.{}".format(data["folder_out"], data["type"])
        if checkout(cmd, "Everything is Ok"):
            yield "arxbad"
            checkout("rm -f {}/arxbad.{}".format(data["folder_out"], data["type"]), "")
        else:
            yield None
    else:
        yield None

@pytest.fixture(autouse=True)
def stat():
    yield
    stat = getout("cat /proc/loadavg")
    cmd = "echo 'time: {} count:{} size: {} load: {}'>> stat.txt".format(datetime.now().strftime("%H:%M:%S.%f"), data["count"], data["bs"], stat)
    checkout(cmd, "")
