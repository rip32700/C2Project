import platform, multiprocessing


class DeviceHooker:

    def __init__(self):
        self._mouse_hook_process = None
        self._keyboard_hook_process = None

    def hook_mouse(self):
        print("[+] Hooking into mouse...")
        if self._mouse_hook_process:
            print("[-] Mouse already hooked")
            return "Mouse already hooked"
        else:
            self._mouse_hook_process = multiprocessing.Process(target=_hook_mouse_worker)
            print("[+] Mouse hooked")
            return "Mouse hooked"

    def unhook_mouse(self):
        print("[+] Unhooking mouse...")
        if self._mouse_hook_process:
            self._mouse_hook_process.terminate()
            print("[+] Mouse unhooked")
            return "Mouse unhooked"
        else:
            print("[-] Mouse is not hooked")
            return "Mouse is not hooked"

    def hook_keyboard(self):
        print("[+] Hooking into keyboard...")
        if self._keyboard_hook_process:
            print("[-] Keyboard already hooked...")
            return "Keyboard already hooked"
        else:
            self._keyboard_hook_process = multiprocessing.Process(target=_hook_keyboard_worker)
            print("[+] Keyboard hooked")
            return "Keyboard hooked"

    def unhook_keyboard(self):
        print("[+] Unhooking keyboard...")
        if self._keyboard_hook_process:
            self._keyboard_hook_process.terminate()
            print("[+] Keyboard unhooked")
            return "Keyboard unhooked"
        else:
            print("[-] Keyboard is not hooked")
            return "Keyboard is not hooked"


def device_enable(event):
        return True


def device_disable(event):
    return False


def _hook_mouse_worker():
    if platform.system() == 'Windows':
        import pyHook, pythoncom

        hooks_manager = pyHook.HookManager()
        hooks_manager.MouseAll = device_enable
        hooks_manager.HookMouse()
        pythoncom.PumpMessages()

    elif platform.system() == 'Linux':
        pass  # TODO
    elif platform.system() == 'Darwin':
        pass  # TODO


def _hook_keyboard_worker():
    if platform.system() == 'Windows':
        import pyHook, pythoncom

        hooks_manager = pyHook.HookManager()
        hooks_manager.KeyAll = device_enable
        hooks_manager.HookKeyboard()
        pythoncom.PumpMessages()

    elif platform.system() == 'Linux':
        pass  # TODO
    elif platform.system() == 'Darwin':
        pass  # TODO

