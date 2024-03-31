from sshcheckers import sshcheckout

class TestPositive:
    # ... код предыдущих шагов ...

    def test_step1(self, make_folders, clear_folders, make_files, print_time):
        # test1
        res1 = sshcheckout(data['host'], data['user'], data['passwd'], "cd {}; 7z a {}/arx -t{}".format(data["folder_in"], data["folder_out"], data["type"]), "Everything is Ok")
        res2 = sshcheckout(data['host'], data['user'], data['passwd'], "ls {}".format(data["folder_out"]), "arx.{}".format(data["type"]))
        assert res1 and res2, "test1 FAIL"

    def test_step2(self, clear_folders, make_files):
        # test2
        res = []
        res.append(sshcheckout(data['host'], data['user'], data['passwd'], "cd {}; 7z a {}/arx -t{}".format(data["folder_in"], data["folder_out"], data["type"]), "Everything is Ok"))
        res.append(sshcheckout(data['host'], data['user'], data['passwd'], "cd {}; 7z e arx.{} -o{} -y".format(data["folder_out"], data["type"], data["folder_ext"]), "Everything is Ok"))
        for item in make_files:
            res.append(sshcheckout(data['host'], data['user'], data['passwd'], "ls {}".format(data["folder_ext"]), item))
        assert all(res)

    def test_step3(self):
        # test3
        assert sshcheckout(data['host'], data['user'], data['passwd'], "cd {}; 7z t arx.{}".format(data["folder_out"], data["type"]), "Everything is Ok"), "test3 FAIL"

    def test_step4(self):
        # test4
        assert sshcheckout(data['host'], data['user'], data['passwd'], "cd {}; 7z u arx2.{}".format(data["folder_in"], data["type"]), "Everything is Ok"), "test4 FAIL"

    def test_step5(self, clear_folders, make_files):
        # test5
        res = []
        res.append(sshcheckout(data['host'], data['user'], data['passwd'], "cd {}; 7z a {}/arx -t{}".format(data["folder_in"], data["folder_out"], data["type"]), "Everything is Ok"))
        for i in make_files:
            res.append(sshcheckout(data['host'], data['user'], data['passwd'], "cd {}; 7z l arx.{}".format(data["folder_out"], data["type"]), i))
        assert all(res), "test5 FAIL"

    def test_step6(self, clear_folders, make_files, make_subfolder):
        # test6
        res = []
        res.append(sshcheckout(data['host'], data['user'], data['passwd'], "cd {}; 7z a {}/arx -t{}".format(data["folder_in"], data["folder_out"], data["type"]), "Everything is Ok"))
        res.append(sshcheckout(data['host'], data['user'], data['passwd'], "cd {}; 7z x arx.{} -o{} -y".format(data["folder_out"], data["type"], data["folder_ext2"]), "Everything is Ok"))
        for i in make_files:
            res.append(sshcheckout(data['host'], data['user'], data['passwd'], "ls {}".format(data["folder_ext2"]), i))
        res.append(sshcheckout(data['host'], data['user'], data['passwd'], "ls {}".format(data["folder_ext2"]), make_subfolder[0]))
        res.append(sshcheckout(data['host'], data['user'], data['passwd'], "ls {}/{}".format(data["folder_ext2"], make_subfolder[0]), make_subfolder[1]))
        assert all(res), "test6 FAIL"

    def test_step7(self):
        # test7
        assert sshcheckout(data['host'], data['user'], data['passwd'], "cd {}; 7z d arx.{}".format(data["folder_out"], data["type"]), "Everything is Ok"), "test7 FAIL"

    def test_step8(self, clear_folders, make_files):
        # test8
        res = []
        for i in make_files:
            res.append(sshcheckout(data['host'], data['user'], data['passwd'], "cd {}; 7z h {}".format(data["folder_in"], i), "Everything is Ok"))
            hash = sshgetout(data['host'], data['user'], data['passwd'], "cd {}; crc32 {}".format(data["folder_in"], i)).upper()
            res.append(sshcheckout(data['host'], data['user'], data['passwd'], "cd {}; 7z h {}".format(data["folder_in"], i), hash))
        assert all(res), "test8 FAIL"

    def test_step99(self):
        res_1 = sshcheckout(data['host'], data['user'], data['passwd'], "echo '1111' | sudo -S dpkg -r p7zip-full", "Удаляется")
        res_2 = sshcheckout(data['host'], data['user'], data['passwd'], "echo '1111' | sudo -S dpkg -s p7zip-full", "Status: deinstall ok")
        assert res_1 and res_2, "test-step0 Fail"
