# #
import os, platform, ast, inspect, re, time
try: from wopw import *
except ModuleNotFoundError: 
    input('error: internal lib "wopw" was not found. Messenger will abort run. (make sure you have cloned this repo correctly, or didnt aborted cloning in proccess)')
    exit(3)
from typing import Dict, Any
from ast import literal_eval
try: import socket, smessage, paramiko # Sensetive modules
except ModuleNotFoundError: 
    input('error: external modules was not imported. Messenger will abort run. (make sure you have installed all modules listed on GitHub or Project Website)')
    exit(3)
class main:
    # Variables
    SNFail = False
    SupportedPlatforms = ['Darwin', 'Linux', 'Windows']
    RaiseErrorWhenHappen = False
    main_conf = {}
    # Classes
    class version:
        Version = 1.0
        VersionType = 'Beta' # Alpha, Beta, Release
        BuildCount = 7
        Build = f'{str(Version).replace('.', '')}{VersionType[0]}{BuildCount}'
        All = f'Version: {Version}\nVersion Type: {VersionType}\nBuild: {Build}'
        class InternalShell:
            Version = 1.0
            VersionType = 'Beta' # Alpha, Beta, Release
            BuildCount = 1
            Build = f'{str(Version).replace('.', '')}{VersionType[0]}{BuildCount}'
    class log:
        State = True
        RuntimeLogs = ''
        PreRunLogs = ''
        AllLogs = ''
        tickCount = 0
        def clearAll(): 
            l = main.log
            l.AllLogs = ''
            l.PreRunLogs = ''
            l.RuntimeLogs = ''
    class activities:
        def Log(Type: str, text: str, Category: str | None = None):
            'Records logs\n\nCategories:\n- all\n- prerun\n- runtime'
            current_time = f'{time.localtime().tm_year}.{time.localtime().tm_mon}.{time.localtime().tm_mday} {time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}'
            main.log.tickCount += 1
            if Type == 'error': c = f'{color.foreground_st.red}{Type}{color.end}  '
            elif Type == 'warning': c = f'{color.foreground_st.yellow}{Type}{color.end}'
            elif Type == 'debug': c = f'{color.foreground_st.blue}{Type}{color.end}  '
            tick = main.log.tickCount
            cache = f'{tick} {current_time} {c}  {text}'
            if main.log.State == False: return
            if Category == 'prerun':  main.log.PreRunLogs = f'{main.log.PreRunLogs}\n{cache}'
            elif Category == 'runtime': main.log.RuntimeLogs = f'{main.log.RuntimeLogs}\n{cache}'
            main.log.AllLogs = f'{main.log.AllLogs}\n{cache}'
        def CreateLocalChat_TUI(chat_name: str):
            progress('Creating chat...')
            codename = input('Codename of chat ("$CHAT_NAME" to use chat name as codename): ')
            if codename.find('$CHAT_NAME') != -1: 
                print(f'Using {chat_name} as codename for online syncing')
                codename = chat_name.lower()
            chat_passwd = input('Password to encrypt/decrypt chat (blank for no protection, dangerous): ')
            online_sync_passwd = input('Password for online syncing (if using Offline mode, will do nothing): ')
            progress('Making...')
            try: os.mkdir(chat_name) # Has gone with os.mkdir to make more compatable with lot of OS (like Windows support in soon)
            except FileExistsError: 
                if input(f'{err} file or forlder alredy exists here. Delete file/dir "{chat_name}"? [y/n]: ') in ['y', 'Y']: 
                    os.rmdir(chat_name)
                    os.mkdir(chat_name)
            open(f'{chat_name}/chat.smoc', 'w').write(str(smessage.main.activities.Encrypt(f'{color.foreground_st.blue}=+=     Start of chat     =+={color.end}\n', chat_passwd)))
            open(f'{chat_name}/chat-conf.smoc', 'w').write(str({
                'codename': f'{smessage.main.activities.Encrypt(codename, chat_passwd)}',
                'sync-passwd': f'{smessage.main.activities.Encrypt(online_sync_passwd, chat_passwd)}'
            }))
        @staticmethod
        def Dict(source: str) -> Dict[str, Any]: # This function was originally rewrited by DeepSeek AI, because couldn't find out how to make this work
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
            except FileNotFoundError: raise FileNotFoundError(f"File not found: {source}")
            except Exception as e: raise ValueError(f"Unexpected error parsing dictionary: {str(e)}")
        def UnsupportedOS():
            prompt('Sorry, this project only supports macOS, Linux (also Termux for Google Android devices). Due problems with libs (wopw is macOS, and partically Linux only).')
            exit()
        def MakeMainConfigurationFile(username: str | None = None, domain: str | None = None, port: int | None = None, user: str | None = None, passwd: str | None = None, encrypt_passswd: str | None = None, sn: str | None = None):
            progress('Encrypting first layer (by password)...')
            domain = str(smessage.main.activities.Encrypt(domain, encrypt_passswd))
            port = str(smessage.main.activities.Encrypt(port, encrypt_passswd))
            user = str(smessage.main.activities.Encrypt(user, encrypt_passswd))
            passwd = str(smessage.main.activities.Encrypt(passwd, encrypt_passswd))
            progress("Encrypting second layer (by machine's SN, may be not encrypted on this step if using Termux, or Wopw lib didn't given any signs of error)")
            domain = str(smessage.main.activities.Encrypt(domain, sn))
            port = str(smessage.main.activities.Encrypt(port, sn))
            user = str(smessage.main.activities.Encrypt(user, sn))
            passwd = str(smessage.main.activities.Encrypt(passwd, sn))
            return {
                'current_user': username,
                'domain': domain,
                'port': port,
                'user': user,
                'passwd': passwd,
                'build': main.version.Build,
                'log': 'True'
            }
        def parse_encrypted_string(encrypted_str): # Created by DeepSeek AI
            results = []
            dict_strings = re.findall(r'\{.*?\}', encrypted_str)
            for dict_str in dict_strings:
                try: data = literal_eval(dict_str)
                except (SyntaxError, ValueError):
                    try:
                        fixed = re.sub(r'([{,]\s*)([a-zA-Z_][a-zA-Z0-9_]*)(\s*:\s*)([^"\',}][^,}]*)',
                                    r'\1"\2"\3"\4"', 
                                    dict_str)
                        data = literal_eval(fixed)
                    except (SyntaxError, ValueError) as e:
                        print(f"Failed to parse dictionary: {dict_str}\nError: {e}")
                        continue
                results.append(data)
            return results
        def DecrpytReceivedMessage(EncryptedChat, decrypt_passwd):  # Created by DeepSeek AI. 
            'Supports by input: unencrypted messages, encrypted (by smessage, which is Fernet with salt)'
            encrypted_data = act.parse_encrypted_string(EncryptedChat)
            decrypted_lines = []
            for data in encrypted_data:
                try:
                    decrypted = smessage.main.activities.Decrypt(data, decrypt_passwd)
                    decrypted_lines.append(decrypted)
                except Exception as e: print(f"Failed to decrypt: {data}\nError: {e}")
            return '\n'.join(decrypted_lines)
        def InternalSettingsShell():
            if main.version.InternalShell.VersionType == 'Beta': print(f'{warn} running a beta version of shell, proceed with caution. It can corrupt your data')
            while True:
                cache = input('settings-shell:: ')
                if cache.find('help') != -1: print('set - set state for variable in main config\nexit - exits from settings-shell\nwrite-changes - writes all changes (those who is should be saved) to main configuration file\nupdate-config - updates main configuration to current version (after update, if configuration file syntax/data updated)\nreload - reads main conf, also applies it to current runtime\nbuild-info - prints build info of IS')
                elif cache.find('set') != -1: 
                    cache = input('set> variable-to-change> ')
                    cache1 = input('set> state> ')
                    if cache == 'log.State': main.log.State = bool(cache1)
                    elif cache == 'current_user': main.main_conf[cache] = cache1
                elif cache.find('write-changes') != -1:
                    cache = open('Password of config: ')
                    progress('Encrypting data...')
                    open('main.smoc', 'w').write(str(smessage.main.activities.Encrypt(main.main_conf, cache)))
                elif cache.find('exit') != -1: break
                elif cache.find('reload') != -1:
                    main.main_conf = act.Dict(open('main.smoc').read())
                    print('Readed & applied successfully')
                elif cache.find('build-info') != -1: print(f'SMOC Internal Settings Shell {main.version.InternalShell.Version}\nBuild: {main.version.InternalShell.Build}')
                else: print('setings-shell: error: no such command. See "help" to get info about available commands')
        def AdvancedMenu():
            cache = input('Advanced Menu\n\n\n 1: App info\n 2: Internal Settings Shell (Beta)\n 3: Logs\n\nSelect: ')
            cls()
            if cache.find('1') != -1: prompt(main.version.All)
            elif cache.find('2') != -1: act.InternalSettingsShell()
            elif cache.find('3') != -1:
                cache = input('Logs\n\n\n 1: Runtime\n 2: Pre-Run\n 3: All\n\nSelect: ')
                cls()
                if cache.find('1') != -1: prompt(main.log.RuntimeLogs)
                elif cache.find('2') != -1: prompt(main.log.PreRunLogs)
                elif cache.find('3') != -1: prompt(main.log.AllLogs)
                else: input('Wrong option!')
            else: input('Wrong option!')
        def MakeMainConfigurationFile_TUI(sn: str):
            'Returns:\n\n- **-4: aborted by user - didnt agree with SMOC sync method**\n- **-5: aborted by user - didnt agree to user one layer encryption**'
            if input('Please read all following warnings, info:\n\n SMOC Messenger uses SSH (paramiko to connect, previosly sshpass) to connect to machine (should be Linux, recomended Manjaro Sway for server), and runs server.py (read more at GitHub, branch server)\n Do you want to continue? [y/n]: ') not in ['y', 'Y']: return -4
            else:
                if sn == -1: 
                    if input(f"{err} machine's serial number cannot be found. SMOC only uses online SSH syncing, where SN is required for main configuration file (or local chats in future). Do you wan't to continue (will use only one encryption layer)? [y/n]: ") not in ['y', 'Y']: return -5
                domain = input('Domain name of server (or IP address): ')
                port = input('Port: ')
                user = input(f'User of {domain}: ')
                passwd = input(f'Password of {user}: ')
                current_user = input('Username of local user (will be used as chat name): ')
                encryption_passwd = input('Password for main conf file encryption (read more at GitHub page): ')
                out = act.MakeMainConfigurationFile(current_user, domain, port, user, passwd, encryption_passwd, sn)
            progress('Writing .smoc main conf file')
            open('main.smoc', 'w').write(str(out))
progress = lambda text: print(f'{color.foreground_st.blue}==>{color.end} {font.bold}{text}{font.end}')
prompt = dev4ones_modules.DefExitPrompt
err = f'{color.foreground_st.red}error:{color.end}'
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
warn = f'{color.foreground_st.yellow}warning:{color.end}'
error = None # To abort error on: except EOFError: ... ; when in normal version: except Exception as error:;
act = main.activities # Shortcut for main.activities
log = act.Log
# # Pre-run
if __name__ != '__main__': 
    log('debug', 'Detected running in import/from mode', 'prerun')
    exit()  # To abort launching TUI, if using in import
if platform.system() not in main.SupportedPlatforms: 
    log('debug', f'Using unsupported OS: {platform.system()}', 'prerun')
    act.UnsupportedOS()
# # Reading SN
log('debug', 'Reading SN...', 'prerun')
progress('Reading serial number...')
sn = machine.GetSerialNumber()
if sn == -1:
    log('error', 'Failed to read serial number (wopw.machine.GetSerialNumber return -1, which is exception when it cannot find SN)', 'prerun')
    print(f'{err} reading failed... One layer encryption/decryption available only')
    sn = ''
# # Reading main.smoc
log('debug', 'Reading main configuration file (main.smoc)', 'prerun')
progress('Reading main configuration file...')
try: 
    main.main_conf = act.Dict('main.smoc')
    if main.main_conf == -3: raise FileNotFoundError
except Exception as e: 
    log('error', f'Excepted error: {e}', 'prerun')
    if input(f'{err} main conf file (main.smoc) was not found. Create it? [y/n]: ') in ['y', 'Y']: act.MakeMainConfigurationFile_TUI(sn)
    progress('Reading main.smoc...')
    try: main.main_conf = act.Dict('main.smoc')
    except: exit()
# Main
log('debug', 'Starting runtime...')
while True:
    try: 
        while True: 
            cls()
            chat_name = input('Chat name to open: ')
            cls()
            if chat_name == 'i': act.AdvancedMenu()
            else: 
                log('debug', f'Reading chat: {chat_name}', 'runtime')
                progress('Reading chat...')
                try: chat = open(f'{chat_name}/chat.smoc')
                except FileNotFoundError: 
                    log('warning', 'Got FileNotFoundError. Looking like there is no chat', 'runtime')
                    if input(f'{err} chat was not found. Create new chat? [y/n]: ') in ['y', 'Y']: act.CreateLocalChat_TUI(chat_name)
                    else: break
                chat_passwd = input('Password to decrypt chat: ')
                progress('Decrypting chat...')
                try: chat = smessage.main.activities.Decrypt(main.activities.Dict(f'{chat_name}/chat.smoc'), chat_passwd)
                except Exception as e: 
                    log('error', f'Excepted: {e}. Looking like password for chat is wrong', 'runtime')
                    prompt(f'{err} password for decrypt is wrong.')
                    break
                cls()
                log('debug', 'Decrypting main configuration file connection data...', 'runtime')
                progress('Decrypting data...')
                cache = input('Password to decrypt data for syncing: ')
                progress('Decrypting first layer...')
                log('debug', 'Decrypting first layer', 'runtime')
                try: done_data = {
                    'domain': smessage.main.activities.Decrypt(main.main_conf['domain'], sn), 
                    'port': smessage.main.activities.Decrypt(main.main_conf['port'], sn),
                    'user': smessage.main.activities.Decrypt(main.main_conf['user'], sn),
                    'passwd': smessage.main.activities.Decrypt(main.main_conf['passwd'], sn)
                }
                except Exception as e: 
                    log('error', f'Excepted: {e}. Looking like machine SN is not same', 'runtime')
                    prompt(f'{err} failed to decrypt. Possible reasons: main.smoc created on different machine, corrupted data')
                    break
                progress('Decrypting second layer...')
                log('debug', 'Decrypting second layer...', 'runtime')
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
                log('debug', 'Decrypting chat conf...', 'runtime')
                chat_conf = act.Dict(f'{chat_name}/chat-conf.smoc')
                chat_conf = {
                    'codename': smessage.main.activities.Decrypt(chat_conf['codename'], chat_passwd),
                    'sync-passwd': smessage.main.activities.Decrypt(chat_conf['sync-passwd'], chat_passwd)
                }
                log('debug', 'All data prepared, starting chat', 'runtime')
                while True:
                    try:
                        cls()
                        cache = input(f'{chat}\n\n  {color.foreground_st.green}Message:{color.end} ')
                        if cache in ['', ' ']: 
                            cls()
                            log('debug', 'Syncing chat...', 'runtime')
                            progress('Syncing chat...')
                            try: 
                                ssh.connect(done_data['domain'], done_data['port'], done_data['user'], done_data['passwd'])
                                stdin, stdout, stderr = ssh.exec_command(f'python3 /home/{done_data['user']}/SMOC-Server/server.py receive {chat_conf['codename']} {main.main_conf['current_user']}')
                                got = ''
                                for line in stdout: got += line.strip()
                            except paramiko.SSHException as e: 
                                log('error', f'Got {e}. Connection to server failed', 'runtime')
                                prompt(f'Connection failed...\n\nParamiko error: {e}')
                                raise EOFError
                            if got.replace('\n', '') == '-1': 
                                log('debug', 'No messages was found. Raising EOFError to get to main page', 'runtime')
                                raise EOFError # No messages was found
                            else: 
                                log('debug', 'Received new message from server', 'runtime')
                                progress('Got new message! Decrypting...')
                                cache = act.DecrpytReceivedMessage(got, chat_conf['sync-passwd'])
                                if cache == '': 
                                    log('warning', 'Looking like got a unecrypted message (probably was sent by hand from server)', 'runtime')
                                    if input('Looking like received message is unencrypted. Do you want to read it? [y/n]: ') in ['y', 'Y']: cache = f'({color.foreground_st.red}unencrypted{color.end}) {got}'
                                    else: raise EOFError
                                chat = f'{chat}\n{cache}'
                                progress('Writing changes to local chat...')
                                log('debug', 'Writing changes to chat after syncing', 'runtime')
                                cache = smessage.main.activities.Encrypt(chat, chat_passwd)
                                open(f'{chat_name}/chat.smoc', 'w').write(str(cache))
                        else: 
                            if cache == '$quote%':
                                log('debug', 'Entered quote mode', 'runtime')
                                print('Entered quote, CTRL+C to exit from.')
                                try:
                                    cache1 = input('quote>')
                                    while True: cache1 = f'{cache1}\n {input('quote>')}'
                                except KeyboardInterrupt: pass
                                cache = cache1
                            cache1 = input('Send to: ')
                            progress('Sending message to server...')
                            log('debug', 'Sending message to server...', 'runtime')
                            cache2 = f'{color.foreground_st.blue}{main.main_conf['current_user']}{color.end}: {cache}'
                            message = smessage.main.activities.Encrypt(cache2, chat_conf['sync-passwd'])
                            try: 
                                ssh.connect(done_data['domain'], done_data['port'], done_data['user'], done_data['passwd'])
                                stdin, stdout, stderr = ssh.exec_command(f"python3 /home/{done_data['user']}/SMOC-Server/server.py send {chat_conf['codename']} '''{message}''' {cache1}")
                                for line in stdout: cache += line.strip()
                            except socket.gaierror:
                                log('error', 'Got error: socket.gaierror. Looking like there is no internet', 'runtime')
                                prompt('Cannot connect to server, looking like there is not internet connection or host is not searchable')
                                raise EOFError
                            except paramiko.SSHException as e: 
                                prompt(f'Connection failed...\n\nParamiko error: {e}')
                                raise EOFError
                            ssh.close()
                            chat = f'{chat}\n{cache2}'
                            progress('Writing changes to local chat...')
                            cache = smessage.main.activities.Encrypt(chat, chat_passwd)
                            open(f'{chat_name}/chat.smoc', 'w').write(str(cache))
                    except EOFError: log('warning', 'Got EOFerror')
    except EOFError: pass 
    except KeyboardInterrupt: 
        log('debug', 'Received KeyboardInterrupt.')
        try: 
            if input('\nExit? [y/n]: ') in ['y', 'Y']: 
                cls()
                exit()
        except EOFError: exit()
        except: pass # To except spaming exception hot keys (like KeyboardInterrupt)
    except Exception as error:
        if main.version.VersionType == 'Beta' or main.RaiseErrorWhenHappen == True: raise # To handle errors if using Beta version (for debugging exceptions)
        try:
            log('error', f'Excepted: {error}', 'runtime')
            cls()
            prompt(f'Unexcepted error occured: {error}')
        except: pass
