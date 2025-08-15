# #
import os, smessage, platform, ast, subprocess, json, re
from wopw import *
from typing import Dict, Any
class main:
    # Variables
    SNFail = False
    SupportedPlatforms = ['Darwin']
    # Classes
    class version:
        Version = 1.0
        VersionType = 'Beta' # Alpha, Beta, Release
        BuildCount = 1
        Build = f'{str(Version).replace('.', '')}{VersionType[0]}{BuildCount}'
        All = f'Version: {Version}\nVersion Type: {VersionType}\nBuild: {Build}'
    class activities:
        def CreateLocalChat(): 
            progress('Creating...')
            cache = input('Name of chat (local): ')
            cache1 = input('Codename of chat (read more about at "help" command): ')
            cache2 = input('Password for local chat: ')
            cache3 = input('Password for online syncing (blank or any if using in offline mode): ')
            progress('Creaing...')
            os.system(f'mkdir {cache}')
            open(f'{cache}/chat.smoc', 'w').write(str(smessage.main.activities.Encrypt(f'{color.foreground_st.blue}=+= Start of chat =+={color.end}', cache2)))
            open(f'{cache}/chat-conf.smoc', 'w').write(str({
                'chat-codename': f'{smessage.main.activities.Encrypt(cache1, cache2)}',
                'sync-passwd': f'{smessage.main.activities.Encrypt(cache3, cache2)}'
            }))
            prompt('Done!')
        @staticmethod
        def Dict(source: str) -> Dict[str, Any]: # deepseek fixed full function (rewrited it)
            """
            Converts a string (or file content) into a Python dict, even if keys are unquoted.
            
            Handles:
            - Standard JSON (`{"key": "value"}`)
            - Python-style (`{'key': 'value'}`)
            - Unquoted keys (`{key: value}`)
            - Files containing such strings
            
            Args:
                source: File path or string containing dictionary data.
                
            Returns:
                Parsed dictionary.
                
            Raises:
                ValueError: If parsing fails.
                FileNotFoundError: If source is a file path and doesn't exist.
            """
            try:
                # Read content if source is a file
                if os.path.exists(source):
                    with open(source, "r", encoding="utf-8") as f:
                        content = f.read().strip()
                else:
                    content = source.strip()

                if not content:
                    raise ValueError("Empty content provided")

                # Case 1: Already valid Python/JSON dict (quoted keys)
                try:
                    return ast.literal_eval(content)
                except (SyntaxError, ValueError):
                    pass  # Fall through to unquoted key handling

                # Case 2: Fix unquoted keys (e.g., `{encrypted: value}`)
                # Step 1: Wrap unquoted keys in quotes
                fixed_content = re.sub(
                    r'([{,]\s*)([a-zA-Z_][a-zA-Z0-9_]*)(\s*:)',
                    r'\1"\2"\3',
                    content
                )
                
                # Step 2: Ensure string values are quoted (if they aren't already)
                fixed_content = re.sub(
                    r':\s*([a-zA-Z0-9_]+)([,\}])',
                    r': "\1"\2',
                    fixed_content
                )

                # Try parsing again
                try:
                    return ast.literal_eval(fixed_content)
                except (SyntaxError, ValueError) as e:
                    raise ValueError(f"Failed to parse dictionary (invalid format): {str(e)}")

            except FileNotFoundError:
                raise FileNotFoundError(f"File not found: {source}")
            except Exception as e:
                raise ValueError(f"Unexpected error parsing dictionary: {str(e)}")
        ReadInDict = Dict
        def UnsupportedOS():
            prompt('Sorry, this project only supports macOS. Due problems with libs (wopw is macOS only). On stable release, Windows/Linux/Termux supoort will be brought.')
            exit()
        def ReadRemoteFileSSH(done_data_dict: dict, file: str):
            'Reads file on remote machine trough SSH, then trough "cat". File is not transfered, only reads (no security leaks)'
            data = done_data_dict
            return str(subprocess.check_output(f'./sshpass -p "{data['passwd']}" ssh {data['user']}@{data['domain']} -p {data['port']} "cat {file}"', shell=True).decode())
        def CreateMainFile(mode: str, username: str | None = None, domain: str | None = None, port: int | None = None, user: str | None = None, passwd: str | None = None, encrypt_passswd: str | None = None, sn: str | None = None):
            if mode == 'Offline':
                return {
                    'mode': 'Offline', 
                    'current_user': 'anon'
                }
            elif mode == 'Sync': 
                progress('Encrypting first layer (by password)...')
                domain = str(smessage.main.activities.Encrypt(domain, encrypt_passswd))
                port = str(smessage.main.activities.Encrypt(port, encrypt_passswd))
                user = str(smessage.main.activities.Encrypt(user, encrypt_passswd))
                passwd = str(smessage.main.activities.Encrypt(passwd, encrypt_passswd))
                progress("Encrypting second layer (by machine's SN)")
                domain = str(smessage.main.activities.Encrypt(domain, sn))
                port = str(smessage.main.activities.Encrypt(port, sn))
                user = str(smessage.main.activities.Encrypt(user, sn))
                passwd = str(smessage.main.activities.Encrypt(passwd, sn))
                return {
                    'mode': 'Sync',
                    'current_user': username,
                    'domain': domain,
                    'port': port,
                    'user': user,
                    'passwd': passwd
                }
        def CreateServerMain():
            if input('Do offline? (to transfer chat locally) [y/n]: ') in ['y', 'Y']:
                out = main.activities.CreateMainFile('Offline')
            else:
                if input('SMOC remote chats uses SSH protocol to transfer data (encrypted), auth will be made only with password (entered data will be double encrypted, and will be exclusive to current machine).\nWarning: DO NOT USE SERVERS YOU DONT TRUST, OR PUBLIC ONES\n Do you want to continue? [y/n]: ') not in ['y', 'Y']:
                    out = main.activities.CreateMainFile('Offline')
                else:
                    progress('Finding current machine serial number...')
                    sn = machine.GetSerialNumber()
                    if sn == -1: 
                        input(f'{err} Machine serial number was not found. Press enter to continue with offline mode, to abort - ctrl+c')
                        out = main.activities.CreateMainFile('Offline')
                    else:
                        cache = input('Domain name of server (or IP): ')
                        cache1 = input('Port (make sure it works with SSH): ')
                        cache2 = input(f'User of {cache}(recomended using user with rbash, if it, "cat" is required): ')
                        cache3 = input(f'Password of {cache2}: ')
                        cache4 = input('Username (will be shown in chats): ')
                        cache5 = input('Password for second-layer encryption (any, recomended 8 digits or more): ')
                        out = main.activities.CreateMainFile('Sync', cache4, cache, cache1, cache2, cache3, cache5, sn)
            progress('Writing .smoc main file')
            open('main.smoc', 'w').write(str(out))
progress = lambda text: print(f'{color.foreground_st.blue}==>{color.end} {font.bold}{text}{font.end}')
prompt = dev4ones_modules.DefExitPrompt
err = f'{color.foreground_st.red}error:{color.end}'
error = None
att = 0
act = main.activities
# # Pre-run
if __name__ != '__main__': exit()  # To abort launching TUI, if using in import
if platform.system() not in main.SupportedPlatforms: main.activities.UnsupportedOS()
# # Binding server
progress('Finding main.smoc...')
try: 
    server_main = act.Dict('main.smoc')
    if server_main == -3: raise FileNotFoundError
except FileNotFoundError: 
    if input(f'{err} server connection info was not found. Create now? [y/n]: ') in ['y', 'Y']: act.CreateServerMain()
    progress('Finding main.smoc...')
    try: server_main = act.Dict('main.smoc')
    except: raise IndexError('No server-main.smoc was found after creating activity was runned.')
# # Reading SN
progress('Reading serial number for "Sync" mode...')
sn = machine.GetSerialNumber()
if sn == -1:
    print(f'{err} reading failed... Offline mode only available.')
    main.SNFail = True
# Main
while True:
    try: 
        while True: 
            cls()
            chat_name = input('Local chat name to open ("help" to get info): ')
            cls()
            if chat_name == 'help': prompt('Help menu\n\nCodename of chat is used to tie up sessions to receive new messages. It will be located on server as (example of): remote-server/home/remote-user/SMOCServerClient/codenames-tie/starkill.tie\nPassword for local chats used to encrypt them, nad make hard to read without password (keep password in secret)\nPassword for online chats used to encrypt message between person to read chat (password must be shared to read chat)\n\nIn chat:\n\nPress enter to try receiving an message from server')
            else:
                cache = chat_name
                progress('Finding local chat...')
                try: chat = open(f'{cache}/chat.smoc')
                except FileNotFoundError: 
                    if input(f'{err} chat was not found. Create new chat? [y/n]: ') in ['y', 'Y']: main.activities.CreateLocalChat()
                    else: break
                chat_passwd = input('Password for decrypt: ')
                progress('Decrypting chat...')
                try: chat = smessage.main.activities.Decrypt(main.activities.ReadInDict(f'{cache}/chat.smoc'), chat_passwd)
                except: 
                    prompt(f'{err} password is wrong.')
                    break
                cls()
                if server_main['mode'] == 'Sync':
                    progress('Decrypting data for syncing...')
                    cache = input('Password for decrypting syncing data: ')
                    progress('Decrypting first layer...')
                    try: done_data = {
                        'domain': smessage.main.activities.Decrypt(server_main['domain'], sn), 
                        'port': smessage.main.activities.Decrypt(server_main['port'], sn),
                        'user': smessage.main.activities.Decrypt(server_main['user'], sn),
                        'passwd': smessage.main.activities.Decrypt(server_main['passwd'], sn)
                    }
                    except: 
                        prompt(f'{err} failed to decrypt. Possible reasons: main.smoc created on different machine, corrupted data')
                        break
                    progress('Decrypting second layer...')
                    try: done_data = {
                        'domain': smessage.main.activities.Decrypt(done_data['domain'], cache), 
                        'port': smessage.main.activities.Decrypt(done_data['port'], cache),
                        'user': smessage.main.activities.Decrypt(done_data['user'], cache),
                        'passwd': smessage.main.activities.Decrypt(done_data['passwd'], cache)
                    }
                    except: 
                        prompt(f'{err} failed to decrypt. Possible reasons: wrong password, corrupted data')
                        break
                chat_conf = act.ReadInDict(f'{chat_name}/chat-conf.smoc')
                chat_conf = {
                    'chat-codename': smessage.main.activities.Decrypt(chat_conf['chat-codename'], chat_passwd),
                    'sync-passwd': smessage.main.activities.Decrypt(chat_conf['sync-passwd'], chat_passwd)
                }
                while True:
                    try:
                        cls()
                        cache = input(f'{chat}\n\n | Message: ')
                        cls()
                        if cache in ['', ' ']: 
                            progress('Syncing chat...')
                            if server_main['mode'] == 'Offline': 
                                chat = act.ReadInDict(f'{chat_name}/chat.smoc')
                                chat = smessage.main.activities.Decrypt(chat, chat_passwd)
                            else:
                                while True: 
                                    try: 
                                        cache = subprocess.check_output(f'./sshpass -p "{done_data['passwd']}" ssh {done_data['user']}@{done_data['domain']} -p {done_data['port']} "python3 /home/{done_data['user']}/SMOC-Server/server.py receive {chat_conf['chat-codename']} {server_main['current_user']}"', shell=True).decode()
                                        break
                                    except subprocess.CalledProcessError: 
                                        if att >= 5: raise TabError
                                        att += 1
                                        progress(f'Failed to connect to server trying again... (att={att})')
                                if cache.replace('\n', '') == '-1': raise EOFError
                                else: 
                                    cache = act.Dict(cache)
                                    progress('Got new message! Decrypting...')
                                    try: cache = smessage.main.activities.Decrypt(cache, chat_conf['sync-passwd'])
                                    except: 
                                        prompt(f'{err} looking like password for online syncing is wrong.')
                                        raise EOFError
                                    chat = f'{chat}\n{cache}'
                                    progress('Writing changes to local chat...')
                                    cache = smessage.main.activities.Encrypt(chat, chat_passwd)
                                    open(f'{chat_name}/chat.smoc', 'w').write(str(cache))
                        else: 
                            cache1 = input('Send to: ')
                            progress('Sending message to server...')
                            cache2 = f'{color.foreground_st.blue}{server_main['current_user']}{color.end}: {cache}'
                            message = smessage.main.activities.Encrypt(cache2, chat_conf['sync-passwd'])
                            os.system(f'''./sshpass -p "{done_data['passwd']}" ssh {done_data['user']}@{done_data['domain']} -p {done_data['port']} "python3 /home/{done_data['user']}/SMOC-Server/server.py send {chat_conf['chat-codename']} '{message}' {cache1}"''')
                            prompt()
                            chat = f'{chat}\n{cache2}'
                            progress('Writing changes to local chat...')
                            cache = smessage.main.activities.Encrypt(chat, chat_passwd)
                            open(f'{chat_name}/chat.smoc', 'w').write(str(cache))
                    except EOFError: pass
    except EOFError: pass 
    except KeyboardInterrupt: 
        if input('\nExit? [y/n]: ') in ['y', 'Y']: 
            cls()
            exit()
    except TabError: 
        prompt('Cannot connect to server, exiting.')
    except Exception as error:  # EOFError:
        cls()
        prompt(f'Unexcepted error occured: {error}')