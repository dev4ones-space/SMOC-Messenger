# SMOC-Messenger
SMOC - is messenger with end-to-end (kind of) feature, also using safe method at sending new messages to other people - fernet.

# Requirements to run

- macOS (darwin) or Linux OS
- Python, 3.13 as minimum recomended
- PyPi (pip) "cryptography" library installed
- For Termux, Linux: "sshpass" in $PATH (for termux: `pkg install sshpass`, arch linux: `pacman -Sy sshpass`, ubuntu: `apt install sshpass`)

# Make your own build

1. Edit needed variables in build.py, build_prefernces.*
2. Run `python3 build.py build`

# Warning: DO NOT USE PUBLIC SERVERS, ONES YOU DON'T TRUST 

# App still in beta/alpha developing. Please report all bugs onto GutHub Issues or on mine email: q@dev4ones.space

# Other info:

**When creating chat**

- Codename of chat: used for syncing, and sorting chats
- Password for online syncing: this password will be used to decrypt/encrypt new messages on clients (messenger). This password must be shared to read new messages (if using mode Sync)
- Password for local chat: uses for decrypting local chat. Only for safety about info ({chat name}/chat.smoc file)

**How chat work**

1. Message encrypts (in this format {username}: {message itself}) in Fernet, using internal library "smessage"
2. Then, client connects to the server by entered data, then executes ~/SMOC-Server/server.py (using python) with args "send"
3. On server, it writes encrypted message by this form SMOC-Server/main/{codename of chat}.{username supposed to read}
4. When another client, syncing chat, by it settings connects to server, executes server.py and checks if there's any messages unread by {codename}.{username}
5. If client finds there's a unread one, it will decrypt it, then put into local chat
