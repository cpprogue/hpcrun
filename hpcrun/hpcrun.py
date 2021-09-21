#!/usr/bin/env python3
import argparse
from getpass import getpass
from pathlib import Path
from shutil import make_archive
from tempfile import TemporaryDirectory
import paramiko

def main():
    dir_path, username, password = setup_env()

    with TemporaryDirectory() as temp_dir:
        client = paramiko.SSHClient()
        client.load_system_host_keys()

        print('Authenticating...')
        client.connect('login.cpp.edu',
            username=username,
            password=password
        )

        print('Zipping data...')
        zip_path = Path(temp_dir).joinpath(dir_path.name)
        zip_path = Path(make_archive(zip_path, 'zip',
            root_dir=dir_path.parent.absolute(),
            base_dir=dir_path.name
        ))

        sftp = client.open_sftp()
        remote_zip_path = f'/user/{username}/{zip_path.name}'
        print('Uploading to ZFS...')
        sftp.put(str(zip_path), remote_zip_path)

    print('Uploading to HPC...')
    run_cmd(client, f'scp ~/{zip_path.name} hpc:~/;rm ~/{zip_path.name}')

    print('Running on HPC... (this may take a while)')
    run_cmd(client,
        "ssh hpc \""
            f"unzip -o ~/{zip_path.name};"
            f"rm ~/{zip_path.name};"
            f"cd ~/{dir_path.name};"
            f"sbatch --wait *.sh;"
            "cd ..;"
            f"zip ~/{zip_path.name} {dir_path.name}/*;"
            f"rm -r ~/{dir_path.name}"
        "\""
    )

    print('Uploading results back...')
    run_cmd(client, f'scp hpc:~/{zip_path.name} ~/')
    sftp.get(remote_zip_path, dir_path.parent.joinpath(zip_path.name))
    sftp.remove(remote_zip_path)

def run_cmd(client, cmd):
    stdin, stdout, stderr = client.exec_command(cmd)
    channel = stdout.channel

    while not channel.exit_status_ready():
        buf = stdout.read()
        if len(buf) > 0:
            output = buf.decode().split('\n')
            for line in output:
                print(f'Remote: {line}')

    exit_code = stdout.channel.recv_exit_status()
    if exit_code != 0:
        print(f'Error: exit code == {exit_code}')
        print(stderr.read().decode())
        exit(2)

def setup_env():
    parser = argparse.ArgumentParser(description='Run a MPI program on the CPP HPC')
    parser.add_argument('directory',
        help='directory to copy to the HPC and run')
    parser.add_argument('username',
        help='CPP account username')

    args = parser.parse_args()

    dir_path = Path(args.directory).resolve()
    if not dir_path.is_dir():
        print('Directory not found')
        exit(1)

    password = getpass()

    return (dir_path, args.username, password)

if __name__ == '__main__':
    main()
