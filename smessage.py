# #
import os, platform, base64, subprocess, inspect, random, ast
try: 
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except: 
    print("error: Could't import modules. Please install 'cryptography'")
    exit(-6)
class main:
    # Variables
    DoCheckEncrypt = True
    # Classes
    class version:
        Version = 1.0
        VersionType = 'Beta' # Alpha, Beta, Release
        BuildCount = 1
        Build = f'{str(Version).replace('.', '')}{VersionType[0]}{BuildCount}'
        All = f'Version: {Version}\nVersion Type: {VersionType}\nBuild: {Build}'
    class activities:
        def GenKey(password: str, salt: bytes) -> bytes:
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            return base64.urlsafe_b64encode(kdf.derive(password.encode()))
        def Encrypt(message: str, password: str) -> dict:
            salt = os.urandom(16)
            key = main.activities.GenKey(password, salt)
            f = Fernet(key)
            encrypted_bytes = f.encrypt(message.encode())
            b64_encoded = base64.b64encode(encrypted_bytes)
            b16_encoded = b64_encoded.hex()
            return {
                'encrypted': b16_encoded,
                'salt': salt.hex()
            }
        def GenPasswd():
            print('Generating 18-digits password for en/de|crypt...')
            cache = ''
            for i in range(18): cache += random.choice('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890!@#$%_-')
            return cache
        def Decrypt(encrypted_data: dict, password: str) -> str:
            if isinstance(encrypted_data, str):
                encrypted_data = ast.literal_eval(encrypted_data)
            salt = bytes.fromhex(encrypted_data['salt'])
            b64_encoded = bytes.fromhex(encrypted_data['encrypted'])
            key = main.activities.GenKey(password, salt)
            f = Fernet(key)
            encrypted_bytes = base64.b64decode(b64_encoded)
            return f.decrypt(encrypted_bytes).decode()
        def Else(cache):
            if cache == '' or cache == ' ': pass
            else: input('Wrong option!')
        def __GetAllActivities__():  # First ChatGPT func
            funcs = [name for name, func in inspect.getmembers(main.activities, inspect.isfunction)]
            funcs.append('__GetAllActivities__')
            return funcs
        def __RunActivity__(name, *args, **kwargs):  # Second ChatGPT func
            funcs = dict(inspect.getmembers(main.activities, inspect.isfunction))
            if name not in funcs:
                raise ValueError(f"Activity '{name}' not found.")
            return funcs[name](*args, **kwargs)