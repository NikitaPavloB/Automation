import yaml
from checkers import checkout, getout
import os
import secrets

with open('config.yaml') as f:
    data = yaml.safe_load(f)

class TestPositive:
    def test_step1(self, make_folders, clear_folders, make_files, print_time):
        cmd = "7z a {}/arx -t{}".format(data["folder_out"], data["type"])
        res1 = checkout(cmd, "Everything is Ok")
        cmd = "ls {}".format(data["folder_out"])
        res2 = checkout(cmd, "arx.{}".format(data["type"]))
        assert res1 and res2, "test1 FAIL"

    def test_step2(self, clear_folders, make_files):
        res = []
        cmd = "7z a {}/arx -t{}".format(data["folder_out"], data["type"])
        res.append(checkout(cmd, "Everything is Ok"))
        cmd = "7z e arx.{} -o{} -y".format(data["type"], data["folder_ext"])
        res.append(checkout(cmd, "Everything is Ok"))
        for item in make_files:
            cmd = "ls {}".format(data["folder_ext"])
            res.append(checkout(cmd, item))
        assert all(res)

    def test_step3(self):
        cmd = "7z t arx.{}".format(data["type"])
        assert checkout(cmd, "Everything is Ok"), "test3 FAIL"

    def test_step4(self):
        cmd = "7z u arx2.{}".format(data["type"])
        assert checkout(cmd, "Everything is Ok"), "test4 FAIL"

    def test_step5(self, clear_folders, make_files):
        res = []
        cmd = "7z a {}/arx -t{}".format(data["folder_out"], data["type"])
        res.append(checkout(cmd, "Everything is Ok"))
        for i in make_files:
            cmd = "7z l arx.{}".format(data["type"])
            res.append(checkout(cmd, i))
        assert all(res), "test5 FAIL"

    def test_step6(self, clear_folders, make_files, make_subfolder):
        res = []
        cmd = "7z a {}/arx -t{}".format(data["folder_out"], data["type"])
        res.append(checkout(cmd, "Everything is Ok"))
        cmd = "7z x arx.{} -o{} -y".format(data["type"], data["folder_ext2"])
        res.append(checkout(cmd, "Everything is Ok"))
        for i in make_files:
            cmd = "ls {}".format(data["folder_ext2"])
            res.append(checkout(cmd, i))
        cmd = "ls {}".format(data["folder_ext2"])
        res.append(checkout(cmd, make_subfolder[0]))
        cmd = "ls {}/{}".format(data["folder_ext2"], make_subfolder[0])
        res.append(checkout(cmd, make_subfolder[1]))
        assert all(res), "test6 FAIL"

    def test_step7(self):
        cmd = "7z d arx.{}".format(data["type"])
       
