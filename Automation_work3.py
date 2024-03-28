import subprocess
import yaml
from checkers import checkout

with open("config.yaml") as f:
    data = yaml.safe_load(f)

FOLDER_TST = data["FOLDER_TST"]
FOLDER_OUT = data["FOLDER_OUT"]
FOLDER_1 = data["FOLDER_1"]


def test_step1(clear_folders, make_folders, make_files):
    # test1
    res1 = checkout(f"cd {FOLDER_TST}; 7z a {FOLDER_OUT}/arx2.7z", "Everything is Ok")
    res2 = checkout(f"ls {FOLDER_OUT}", "arx2.7z")
    assert res1 and res2, "test1 FAIL"


def test_step2():
    # test2
    res1 = checkout(f"cd {FOLDER_TST}; 7z e {FOLDER_OUT}/arx2.7z -o{FOLDER_1} -y", "Everything is Ok")
    res2 = checkout(f"ls {FOLDER_1}", "text.txt")
    assert res1 and res2, "test2 FAIL"


def test_step3():
    # test3
    assert checkout(f"cd {FOLDER_OUT}; 7z t arx2.7z", "Everything is Ok"), "test3 FAIL"


def test_step4():
    # test4
    assert checkout(f"7z d {FOLDER_OUT}/arx2.7z", "Everything is Ok"), "test4 FAIL"


def test_step5():
    # test5
    assert checkout(f"cd {FOLDER_TST}; 7z u {FOLDER_OUT}/arx2.7z", "Everything is Ok"), "test5 FAIL"


def test_step6():
    # test6 - проверка команды для вывода списка файлов (l)
    res = checkout(f"cd {FOLDER_TST}; 7z l {FOLDER_OUT}/arx2.7z", "text.txt")
    assert res, "test6 FAIL"


def test_step7(clear_folders, make_folders, make_files):
    # test7 - проверка команды для разархивирования с сохранением путей (x)
    res = []
    res.append(checkout(f"cd {FOLDER_TST}; 7z a {FOLDER_OUT}/arx2.7z", "Everything is Ok"))
    res.append(checkout(f"cd {FOLDER_TST}; 7z x {FOLDER_OUT}/arx2.7z -o{FOLDER_1} -y", "Everything is Ok"))
    for item in make_files:
        res.append(checkout(f"ls {FOLDER_1}", item))
    assert all(res), "test7 FAIL"


def test_step8():
    # test8 - проверка команды для расчета хеша (h)
    res = checkout(f"cd {FOLDER_TST}; 7z h {FOLDER_OUT}/arx2.7z", "CRC32")
    assert res, "test8 FAIL"
