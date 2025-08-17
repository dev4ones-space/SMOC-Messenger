pyinstaller --noconfirm --onefile --console --add-data "$(pwd)/wopw.py:." --add-data "$(pwd)/smessage.py:."  "$(pwd)/main.py"
