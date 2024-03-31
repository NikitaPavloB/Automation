from checkers import checkout, getout
import yaml
from sshcheckers import upload_files, sshcheckout

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
        self.save_log(start_ttime, "log_1.txt")
        assert res_1 and res_2, "test-step0 Fail"

    def test_step1(self, make_folders, clear_folders, make_files, print_time):
        # test1
        res1 = checkout("cd {}; 7z a {}/arx -t{}".format(data["folder_in"], data["folder_out"], data["type"]), "Everything is Ok")
        res2 = checkout("ls {}".format(data["folder_out"]), "arx.{}".format(data["type"]))
        assert res1 and res2, "test1 FAIL"

    def test_step2(self, clear_folders, make_files):
        # test2
        res = []
        res.append(checkout("cd {}; 7z a {}/arx -t{}".format(data["folder_in"], data["folder_out"], data["type"]), "Everything is Ok"))
        res.append(checkout("cd {}; 7z e arx.{} -o{} -y".format(data["folder_out"], data["type"], data["folder_ext"]), "Everything is Ok"))
        for item in make_files:
            res.append(checkout("ls {}".format(data["folder_ext"]), item))
        assert all(res)

    def test_step3(self):
        # test3
        assert checkout("cd {}; 7z t arx.{}".format(data["folder_out"], data["type"]), "Everything is Ok"), "test3 FAIL"

    def test_step4(self):
        # test4
        assert checkout("cd {}; 7z u arx2.{}".format(data["folder_in"], data["type"]), "Everything is Ok"), "test4 FAIL"

    def test_step5(self, clear_folders, make_files):
        # test5
        res = []
        res.append(checkout("cd {}; 7z a {}/arx -t{}".format(data["folder_in"], data["folder_out"], data["type"]), "Everything is Ok"))
        for i in make_files:
            res.append(checkout("cd {}; 7z l arx.{}".format(data["folder_out"], data["type"]), i))
        assert all(res), "test5 FAIL"

    def test_step6(self, clear_folders, make_files, make_subfolder):
        # test6
        res = []
        res.append(checkout("cd {}; 7z a {}/arx -t{}".format(data["folder_in"], data["folder_out"], data["type"]), "Everything is Ok"))
        res.append(checkout("cd {}; 7z x arx.{} -o{} -y".format(data["folder_out"], data["type"], data["folder_ext2"]), "Everything is Ok"))
        for i in make_files:
            res.append(checkout("ls {}".format(data["folder_ext2"]), i))
        res.append(checkout("ls {}".format(data["folder_ext2"]), make_subfolder[0]))
        res.append(checkout("ls {}/{}".format(data["folder_ext2"], make_subfolder[0]), make_subfolder[1]))
        assert all(res), "test6 FAIL"

    def test_step7(self):
        # test7
        assert checkout("cd {}; 7z d arx.{}".format(data["folder_out"], data["type"]), "Everything is Ok"), "test7 FAIL"

    def test_step8(self, clear_folders, make_files):
        # test8
        res = []
        for i in make_files:
            res.append(checkout("cd {}; 7z h {}".format(data["folder_in"], i), "Everything is Ok"))
            hash = getout("cd {}; crc32 {}".format(data["folder_in"], i)).upper()
            res.append(checkout("cd {}; 7z h {}".format(data["folder_in"], i), hash))
        assert all(res), "test8 FAIL"

    def test_step99(self):
        res_1 = (sshcheckout('127.0.0.1', 'user2', '1111', "echo '1111' | sudo -S dpkg -r p7zip-full",
                          'Удаляется'))
        res_2 = (sshcheckout('127.0.0.1', 'user2', '1111', "echo '1111' | sudo -S dpkg -s p7zip-full",
                          'Status: deinstall ok'))
        assert res_1 and res_2, "test-step0 Fail"