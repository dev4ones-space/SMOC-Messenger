# #
import os, smessage, platform, ast, subprocess, inspect, re, paramiko
from wopw import *
from typing import Dict, Any
class main:
    # Variables
    SNFail = False
    SupportedPlatforms = ['Darwin', 'Linux', 'Windows']
    # Classes
    class version:
        Version = 1.0
        VersionType = 'Beta' # Alpha, Beta, Release
        BuildCount = 3
        Build = f'{str(Version).replace('.', '')}{VersionType[0]}{BuildCount}'
        All = f'Version: {Version}\nVersion Type: {VersionType}\nBuild: {Build}'
    class activities:
        def MakeChat_TUI(chat_name: str): 
            progress('Creating chat...')
            codename = input('Codename of chat ("$CHAT_NAME" to use chat name as codename): ')
            if codename.find('$CHAT_NAME') != -1: codename = chat_name.lower()
            chat_passwd = input('Password to encrypt/decrypt chat (blank for no protection, dangerous): ')
            online_sync_passwd = input('Password for online syncing (if using Offline mode, will do nothing): ')
            progress('Making...')
            try: os.mkdir(chat_name) # For cross-platform
            except FileExistsError: 
                if input(f'{err} got FileExistsError. Delete file/dir "{chat_name}"? [y/n]: ') in ['y', 'Y']: 
                    os.rmdir(chat_name)
                    os.mkdir(chat_name)
            open(f'{chat_name}/chat.smoc', 'w').write(str(smessage.main.activities.Encrypt(f'{color.foreground_st.blue}=+=     Start of chat     =+={color.end}\n', chat_passwd)))
            open(f'{chat_name}/chat-conf.smoc', 'w').write(str({
                'codename': f'{smessage.main.activities.Encrypt(codename, chat_passwd)}',
                'sync-passwd': f'{smessage.main.activities.Encrypt(online_sync_passwd, chat_passwd)}'
            }))
        @staticmethod
        def Dict(source: str) -> Dict[str, Any]: # This function was fully rewrited by Deepseek AI
            try:
                if os.path.exists(source):
                    with open(source, "r", encoding="utf-8") as f: content = f.read().strip()
                else: content = source.strip()
                if not content: raise ValueError("Empty content provided")
                try: return ast.literal_eval(content)
                except (SyntaxError, ValueError): pass
                fixed_content = re.sub(r'([{,]\s*)([a-zA-Z_][a-zA-Z0-9_]*)(\s*:)', r'\1"\2"\3', content)
                fixed_content = re.sub(r':\s*([a-zA-Z0-9_]+)([,\}])', r': "\1"\2', fixed_content)
                try: return ast.literal_eval(fixed_content)
                except (SyntaxError, ValueError) as e: raise ValueError(f"Failed to parse dictionary (invalid format): {str(e)}")
            except FileNotFoundError:
                raise FileNotFoundError(f"File not found: {source}")
            except Exception as e:
                raise ValueError(f"Unexpected error parsing dictionary: {str(e)}")
        def UnsupportedOS():
            prompt('Sorry, this project only supports macOS. Due problems with libs (wopw is macOS only). On stable release, Windows/Linux/Termux supoort will be brought.')
            exit()
        def MakeMainFile(mode: str, username: str | None = None, domain: str | None = None, port: int | None = None, user: str | None = None, passwd: str | None = None, encrypt_passswd: str | None = None, sn: str | None = None):
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
        def __GetAllActivities__():  # Artazon func
            if main.activities.control.map.get('__GetAllActivities__') != True: 
                main.activities.control.TurnedOff()
                return -90
            funcs = [name for name, func in inspect.getmembers(main.activities, inspect.isfunction)]
            funcs.append('__GetAllActivities__')
            return funcs
        def __RunActivity__(name, *args, **kwargs):  # Artazon func
            if main.activities.control.map.get('__RunActivity__') != True: 
                main.activities.control.TurnedOff()
                return -90
            funcs = dict(inspect.getmembers(main.activities, inspect.isfunction))
            if name not in funcs:
                raise ValueError(f"Activity '{name}' not found.")
            return funcs[name](*args, **kwargs)
        def AdvancedMenu():
            cache = input('Advanced Menu\n\n\n 1: List activities\n 2: Run activity\n 3: App info\n\nSelect: ')
            cls()
            if cache.find('1') != -1: 
                cls()
                prompt('\n'.join(act.__GetAllActivities__()).replace('__GetAllActivities__', ''))
            elif cache.find('2') != -1:
                cls()
                cache = input('Activity: ')
                cache1 = input('Arg (%N to use without args): ')
                if cache1.find('%N') != -1: cache = act.__RunActivity__(cache)
                else: cache = act.__RunActivity__(cache, cache1)
                prompt(f'Activity exit code: {cache}\nDone!')
            elif cache.find('3') != -1: input(f'{main.version.All}\n\nThis advanced menu was taken and set from Artazon\n\npress enter to exit')
            else: input('Wrong option!')
        def MakeMainFile_TUI(sn):
            if input('Use offline? (to transfer chat locally) [y/n]: ') in ['y', 'Y']: out = act.MakeMainFile('Offline')
            else:
                if input('SMOC Online (Sync) mode uses SSH protocol to transfer messages (if using offical builds, messages will be automatically encrypted).\nNotice: To prevent data leaks, proceed with those rules: \n  Only use servers you trust\n  Mass-user server is dangerous(tampering server, making logs, saving data danger)\n\n Do you want to continue? [y/n]: ') not in ['y', 'Y']: out = act.MakeMainFile('Offline')
                else:
                    if sn == -1: 
                        input(f"{err} wopw: serial number of current machine can't be found. SMOC uses double-layer encryption for connection data (main.smoc), and it requires SN to be found.\nWithout SN you cannot use Sync/Online mode by security reasons\n\npress enter to continue, CTRL+C to abort")
                        out = act.MakeMainFile('Offline')
                    else:
                        domain = input('Domain name of server (or IP address): ')
                        port = input('Port: ')
                        user = input(f'User of {domain} (see recomendations on GitHub page or in source info.txt): ')
                        passwd = input(f'Password of {user}: ')
                        current_user = input('Username (will be used for chat): ')
                        encryption_passwd = input('Password for data encryption (read more at info.txt or GitHub page): ')
                        out = act.MakeMainFile('Sync', current_user, domain, port, user, passwd, encryption_passwd, sn)
            progress('Writing .smoc main file')
            open('main.smoc', 'w').write(str(out))
progress = lambda text: print(f'{color.foreground_st.blue}==>{color.end} {font.bold}{text}{font.end}')
prompt = dev4ones_modules.DefExitPrompt
err = f'{color.foreground_st.red}error:{color.end}'
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
error = None # To abort error on: except EOFError: ... ; when in normal version: except Exception as error:;
connection_attempts = 0 # Attemps for reconnecting to server (in chat)
act = main.activities # Shortcut
# # Pre-run
if __name__ != '__main__': exit()  # To abort launching TUI, if using in import
if platform.system() not in main.SupportedPlatforms: act.UnsupportedOS()
# # Reading SN
progress('Reading serial number...')
sn = machine.GetSerialNumber()
if sn == -1:
    print(f'{err} reading failed... Offline mode only available.')
    main.SNFail = True
    sn = 0
# # Reading main.smoc
progress('Reading main.smoc...')
try: 
    main_data = act.Dict('main.smoc')
    if main_data == -3: raise FileNotFoundError
except: 
    if input(f'{err} main file (main.smoc) was not found. Create it? [y/n]: ') in ['y', 'Y']: act.MakeMainFile_TUI(sn)
    progress('Reading main.smoc...')
    try: main_data = act.Dict('main.smoc')
    except: raise IndexError('main.smoc was not found after successfully runned activity MakeMainFile_TUI')
# Main
while True:
    try: 
        while True: 
            cls()
            chat_name = input('Chat name to open ("i" for advanced menu): ')
            cls()
            if chat_name == 'i': act.AdvancedMenu()
            else: 
                progress('Reading chat...')
                try: chat = open(f'{chat_name}/chat.smoc')
                except FileNotFoundError: 
                    if input(f'{err} chat was not found. Create new chat? [y/n]: ') in ['y', 'Y']: act.MakeChat_TUI(chat_name)
                    else: break
                chat_passwd = input('Password to decrypt chat: ')
                progress('Decrypting chat...')
                try: chat = smessage.main.activities.Decrypt(main.activities.Dict(f'{chat_name}/chat.smoc'), chat_passwd)
                except: 
                    prompt(f'{err} password for decrypt is wrong.')
                    break
                cls()
                if main_data['mode'] == 'Sync':
                    progress('Decrypting data...')
                    cache = input('Password to decrypt data for syncing: ')
                    progress('Decrypting first layer...')
                    try: done_data = {
                        'domain': smessage.main.activities.Decrypt(main_data['domain'], sn), 
                        'port': smessage.main.activities.Decrypt(main_data['port'], sn),
                        'user': smessage.main.activities.Decrypt(main_data['user'], sn),
                        'passwd': smessage.main.activities.Decrypt(main_data['passwd'], sn)
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
                progress('Decrypting chat conf...')
                chat_conf = act.Dict(f'{chat_name}/chat-conf.smoc')
                chat_conf = {
                    'codename': smessage.main.activities.Decrypt(chat_conf['codename'], chat_passwd),
                    'sync-passwd': smessage.main.activities.Decrypt(chat_conf['sync-passwd'], chat_passwd)
                }
                while True:
                    try:
                        cls()
                        cache = input(f'{chat}\n\n  {color.foreground_st.green}Message:{color.end} ')
                        cls()
                        if cache in ['', ' ']: 
                            progress('Syncing chat...')
                            if main_data['mode'] == 'Offline': 
                                chat = act.Dict(f'{chat_name}/chat.smoc')
                                chat = smessage.main.activities.Decrypt(chat, chat_passwd)
                            else:
                                try: 
                                    ssh.connect(done_data['domain'], done_data['port'], done_data['user'], done_data['passwd'])
                                    stdin, stdout, stderr = ssh.exec_command(f'python3 /home/{done_data['user']}/SMOC-Server/server.py receive {chat_conf['codename']} {main_data['current_user']}')
                                    for line in stdout: cache += line.strip()
                                except paramiko.SSHException as e: 
                                    prompt(f'Connection failed...\n\nParamiko error: {e}')
                                    raise EOFError
                                if cache.replace('\n', '') == '-1': raise EOFError # No messages was found
                                else: 
                                    progress('Got new message! Decrypting...')
                                    try: 
                                        cache1 = act.Dict(cache)
                                        cache = smessage.main.activities.Decrypt(cache1, chat_conf['sync-passwd'])
                                    except ValueError:
                                        if input('Looking like message received is unencrypted. Do you want to read it? [y/n]: ') in ['y', 'Y']: cache = f'({color.foreground_st.red}unencrypted{color.end}) {cache}'
                                        else: raise EOFError
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
                            cache2 = f'{color.foreground_st.blue}{main_data['current_user']}{color.end}: {cache}'
                            message = smessage.main.activities.Encrypt(cache2, chat_conf['sync-passwd'])
                            try: 
                                ssh.connect(done_data['domain'], done_data['port'], done_data['user'], done_data['passwd'])
                                stdin, stdout, stderr = ssh.exec_command(f"python3 /home/{done_data['user']}/SMOC-Server/server.py send {chat_conf['codename']} '{message}' {cache1}")
                                for line in stdout: cache += line.strip()
                            except paramiko.SSHException as e: 
                                prompt(f'Connection failed...\n\nParamiko error: {e}')
                                raise EOFError
                            #os.system(f'''./sshpass -p "{done_data['passwd']}" ssh {done_data['user']}@{done_data['domain']} -p {done_data['port']} "python3 /home/{done_data['user']}/SMOC-Server/server.py send {chat_conf['codename']} '{message}' {cache1}"''')
                            chat = f'{chat}\n{cache2}'
                            progress('Writing changes to local chat...')
                            cache = smessage.main.activities.Encrypt(chat, chat_passwd)
                            open(f'{chat_name}/chat.smoc', 'w').write(str(cache))
                    except EOFError: pass
    except EOFError: pass 
    except KeyboardInterrupt: 
        try: 
            if input('\nExit? [y/n]: ') in ['y', 'Y']: 
                cls()
                raise RuntimeError
        except RuntimeError: exit()
        except: pass
    except EOFError:  # EOFError  #Exception as error
        try:
            cls()
            prompt(f'Unexcepted error occured: {error}')
        except: pass