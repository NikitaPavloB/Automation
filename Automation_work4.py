from checkers import checkout, getout
import yaml
from sshcheckers import upload_files, sshcheckout, sshgetout

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive:
    def save_log(self, start_time, name):
        with open(name, 'w') as f:
            f.write(getout(f"journalctl --since '{start_time}'"))

    def test_step0(self, start_ttime):
        upload_files(data['host'], data['user'], data['passwd'], 'p7zip-full.deb', '/home/user2/p7zip-full.deb')
        res_1 = (sshcheckout('127.0.0.1', 'user2', '1111', "echo '1111' | sudo -S dpkg -i /home/user2/p7zip-full.deb",
                             'Настраивается пакет'))
        res_2 = (sshcheckout('127.0.0.1', 'user2', '1111', "echo '1111' | sudo -S dpkg -s p7zip-full",
                             'Status: install ok installed'))
        self.save_log(start_ttime, "log_0.txt")
        assert res_1 and res_2, "test-step0 Fail"

    def test_step1(self, make_folders, clear_folders, make_files, print_time, start_ttime):
        # test1
        res1 = sshcheckout(data['host'], data['user'], data['passwd'], "cd {}; 7z a {}/arx -t{}".format(data["folder_in"], data["folder_out"], data["type"]), "Everything is Ok")
        res2 = sshcheckout(data['host'], data['user'], data['passwd'], "ls {}".format(data["folder_out"]), "arx.{}".format(data["type"]))
        self.save_log(start_ttime, "log_1.txt")
        assert res1 and res2, "test1 FAIL"

    def test_step2(self, clear_folders, make_files, start_ttime):
        # test2
        res = []
        res.append(sshcheckout(data['host'], data['user'], data['passwd'], "cd {}; 7z a {}/arx -t{}".format(data["folder_in"], data["folder_out"], data["type"]), "Everything is Ok"))
        res.append(sshcheckout(data['host'], data['user'], data['passwd'], "cd {}; 7z e arx.{} -o{} -y".format(data["folder_out"], data["type"], data["folder_ext"]), "Everything is Ok"))
        for item in make_files:
            res.append(sshcheckout(data['host'], data['user'], data['passwd'], "ls {}".format(data["folder_ext"]), item))
        self.save_log(start_ttime, "log_2.txt")
        assert all(res)

    def test_step3(self, start_ttime):
        # test3
        self.save_log(start_ttime, "log_3.txt")
        assert sshcheckout(data['host'], data['user'], data['passwd'], "cd {}; 7z t arx.{}".format(data["folder_out"], data["type"]), "Everything is Ok"), "test3 FAIL"

    def test_step4(self, start_ttime):
        # test4
        self.save_log(start_ttime, "log_4.txt")
        assert sshcheckout(data['host'], data['user'], data['passwd'], "cd {}; 7z u arx2.{}".format(data["folder_in"], data["type"]), "Everything is Ok"), "test4 FAIL"

    def test_step5(self, clear_folders, make_files, start_ttime):
        # test5
        res = []
        res.append(sshcheckout(data['host'], data['user'], data['passwd'], "cd {}; 7z a {}/arx -t{}".format(data["folder_in"], data["folder_out"], data["type"]), "Everything is Ok"))
        for i in make_files:
            res.append(sshcheckout(data['host'], data['user'], data['passwd'], "cd {}; 7z l arx.{}".format(data["folder_out"], data["type"]), i))
        self.save_log(start_ttime, "log_5.txt")
        assert all(res), "test5 FAIL"

    def test_step6(self, clear_folders, make_files, make_subfolder, start_ttime):
        # test6
        res = []
        res.append(sshcheckout(data['host'], data['user'], data['passwd'], "cd {}; 7z a {}/arx -t{}".format(data["folder_in"], data["folder_out"], data["type"]), "Everything is Ok"))
        res.append(sshcheckout(data['host'], data['user'], data['passwd'], "cd {}; 7z x arx.{} -o{} -y".format(data["folder_out"], data["type"], data["folder_ext2"]), "Everything is Ok"))
        for i in make_files:
            res.append(sshcheckout(data['host'], data['user'], data['passwd'], "ls {}".format(data["folder_ext2"]), i))
        res.append(sshcheckout(data['host'], data['user'], data['passwd'], "ls {}".format(data["folder_ext2"]), make_subfolder[0]))
        res.append(sshcheckout(data['host'], data['user'], data['passwd'], "ls {}/{}".format(data["folder_ext2"], make_subfolder[0]), make_subfolder[1]))
        self.save_log(start_ttime, "log_6.txt")
        assert all(res), "test6 FAIL"

    def test_step7(self, start_ttime):
        # test7
        self.save_log(start_ttime, "log_7.txt")
        assert sshcheckout(data['host'], data['user'], data['passwd'], "cd {}; 7z d arx.{}".format(data["folder_out"], data["type"]), "Everything is Ok"), "test7 FAIL"

    def test_step8(self, clear_folders, make_files, start_ttime):
        # test8
        res = []
        for i in make_files:
            res.append(sshcheckout(data['host'], data['user'], data['passwd'], "cd {}; 7z h {}".format(data["folder_in"], i), "Everything is Ok"))
            hash = sshgetout(data['host'], data['user'], data['passwd'], "cd {}; crc32 {}".format(data["folder_in"], i)).upper()
            res.append(sshcheckout(data['host'], data['user'], data['passwd'], "cd {}; 7z h {}".format(data["folder_in"], i), hash))
        self.save_log(start_ttime, "log_8.txt")
        assert all(res), "test8 FAIL"

    def test_step99(self, start_ttime):
        res_1 = (sshcheckout('127.0.0.1', 'user2', '1111', "echo '1111' | sudo -S dpkg -r p7zip-full",
                             'Удаляется'))
        res_2 = (sshcheckout('127.0.0.1', 'user2', '1111', "echo '1111' | sudo -S dpkg -s p7zip-full",
                             'Status: deinstall ok'))
        self.save_log(start_ttime, "log_99.txt")
        assert res_1 and res_2, "test-step0 Fail"
