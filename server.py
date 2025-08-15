# #
import os, argparse
from wopw import *
class main:
    # Variables
    WORKPATH = '~/SMOC-Server' # Default is ~/SMOC-Server
    # Classes
    class version:
        Version = 1.0
        VersionType = 'Beta' # Alpha, Beta, Release
        BuildCount = 1
        Build = f'{str(Version).replace('.', '')}{VersionType[0]}{BuildCount}'
        All = f'Version: {Version}\nVersion Type: {VersionType}\nBuild: {Build}'
    class activities:
        def DoesFileExists(path): 
            'Returns:\n\n- 0: File exists\n- 1: File is not found'
            try: open(path, 'r').read()
            except FileNotFoundError: return 1
            return 0
        def ConnectedMessage(): print(f'{color.foreground_st.blue}{font.bold}Connected to server! Running {main.version.Build}{color.end}')
        def Send(codename, message, sender_username):
            act.ConnectedMessage()
            progress('Sending message...')
            main_path = f'{main.WORKPATH}/main/{codename}.{sender_username}'
            if act.DoesFileExists(main_path) == 0:
                cache = open(main_path, 'r').read()
                open(main_path, 'w').write(f'{cache}\n{message}')
            else: open(main_path, 'w').write(message)
            progress('Done!')
        def Receive(codename, username_whos_for):
            'Returns:\n\n- -1: No such active session for entered username/codename'
            main_path = f'{main.WORKPATH}/main/{codename}.{username_whos_for}'
            try: cache = open(main_path).read()
            except FileNotFoundError:
                print(-1)
                return -1
            print(cache)
            os.system(f'rm {main_path}')
        def Test(state):
            if state in ['send', '1']: act.Send('starkill', 'Test', 'spencer')
            elif state in ['get', 'receive', '2']: act.Receive('starkill', 'spencer')
act = main.activities
prompt = dev4ones_modules.DefExitPrompt
progress = lambda text: print(f'{color.foreground_st.blue}==>{color.end} {font.bold}{text}{font.end}')
# # Pre-run
if main.WORKPATH in [None, '']: main.WORKPATH = '~/SMOC-Server'
# # Argparse things
parser = argparse.ArgumentParser(description=f'A SMOC Messenger Server')
subparsers = parser.add_subparsers(dest='command', required=True)
send_parser = subparsers.add_parser('send', help='Will send message (if using offical builds of SMOC, it will automatically send encrypted message/s) by codename')
send_parser.add_argument('codename')
send_parser.add_argument('message')
send_parser.add_argument('sender_username')
subparsers.add_parser('version', help='Prints all data about build')
receive_parser = subparsers.add_parser('receive', help='Will print out all messages sent by codename (encrypted if using offical builds)')
receive_parser.add_argument('codename')
receive_parser.add_argument('username_whos_for')
subparsers.add_parser('test', help='Used for testing server is working properly. Tester codename is starkill (also known as AZ-001). States: send, get (also has alias "receive")').add_argument('state')
subparsers.add_parser('get-version', help='Will print server.py version. Used for SMOC client to check if server is compatable')
args = parser.parse_args()
# Main
if args.command == 'send': act.Send(args.codename, args.message, args.sender_username)
elif args.command == 'version': print(main.version.All)
elif args.command == 'receive': act.Receive(args.codename, args.username_whos_for)
elif args.command == 'test': act.Test(args.state)
elif args.command == 'get-version': print(main.version.Version)