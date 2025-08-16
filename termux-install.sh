echo "Installing cryptography"
apt install python-cryptography
echo "Installing paramiko" # Commands to install paramiko was taken from Reddit, user: BufuWinner (3 years ago, in 2022) in r/termux
pkg install clang python libffi openssl libsodium
SODIUM_INSTALL=system pip install pyacl
pip install paramiko
