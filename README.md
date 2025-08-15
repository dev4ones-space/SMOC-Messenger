# SMOC-Messenger
SMOC - is an end-to-end (half of) messenger with encryption. It supports offline chats, and also online syncing by SSH protocol.

# Requirements

- macOS, Linux (Termux counts) machine with seriel number recognition
- cryptography pip library installed
- python3, not lower that 3.13

# App in beta test! All bugs (report them on GitHub Issues or on mine email: q@dev4ones.space) will be fixed by first stable release.

# How to install on server

1. Download main/server or from branch "server" to your linux machine
2. Place downloaded server folder as ~/SMOC-Server
3. Edit ~/SMOC-Server/server.py, set up main.WORKPATH to your ~/SMOC-Server (full dir, python don't accepts ~ as real dir)
4. Make sure python (not lower that 3.13) is installed
