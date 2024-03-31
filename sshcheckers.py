import paramiko

def upload_files(host, user, passwd, local_path, remote_path, port=22):
    transport = paramiko.Transport((host, port))
    transport.connect(None, username=user, password=passwd)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put(local_path, remote_path)
    sftp.close()
    transport.close()

def download_files(host, user, passwd, local_path, remote_path, port=22):
    transport = paramiko.Transport((host, port))
    transport.connect(None, username=user, password=passwd)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.get(remote_path, local_path)
    sftp.close()
    transport.close()

def sshgetout(host, user, passwd, cmd, port=22):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=passwd, port=port)
    stdin, stdout, stderr = client.exec_command(cmd)
    out = (stdout.read() + stderr.read()).decode("utf-8")
    client.close()
    return out

def sshcheckout(host, user, passwd, cmd, text, port=22):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=passwd, port=port)
    stdin, stdout, stderr = client.exec_command(cmd)
    exitcode = stdout.channel.recv_exit_status()
    out = (stdout.read() + stderr.read()).decode("utf-8")
    client.close()
    if text in out and not exitcode:
        return True
    else:
        return False

def sshcheckout(host, user, passwd, cmd, text, port=22):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=passwd, port=port)
    stdin, stdout, stderr = client.exec_command(cmd)
    exitcode = stdout.channel.recv_exit_status()
    out = (stdout.read() + stderr.read()).decode("utf-8")
    print(out)
    client.close()
    if text in out and not exitcode:
        return True
    else:
        return False

def sshnegcheckout(host, user, passwd, cmd, text, port=22):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=passwd, port=port)
    stdin, stdout, stderr = client.exec_command(cmd)
    exitcode = stdout.channel.recv_exit_status()
    out = (stdout.read() + stderr.read()).decode("utf-8")
    client.close()
    if text in out and exitcode:
        return True
    else:
        return False
