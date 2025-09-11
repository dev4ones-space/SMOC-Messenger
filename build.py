# #
import platform, subprocess
from wopw import *
progress = lambda text: print(f'{color.foreground_st.blue}==>{color.end} {font.bold}{text}{font.end}')
err = f'{color.foreground_st.red}error:{color.end}'
warn = f'{color.foreground_st.yellow}warning:{color.end}'
shell = subprocess.getoutput
cmd_to_build = 'pyinstaller --noconfirm --onefile --console --add-data "$(pwd)/wopw.py:." --add-data "$(pwd)/smessage.py:."  "$(pwd)/main.py"'
class builder:
    Build = '10R1'
    WorksWith = ['10R2']
    SupportedOS = ['Darwin', 'Linux']
try: import main as smoc
except ModuleNotFoundError:
    print(f'{err} no main.py was found.')
    exit()
except SyntaxError:
    print('error: python version you currently running is unsupported to run SMOC. Recomended using 3.13 and higher')
    exit()
# Main
progress('Checking required info...')
# Checking if build is compatable
if smoc.main.version.Build not in builder.WorksWith:
    print(f'{err} this build is not compatable with builder.')
    exit()
if platform.system() not in builder.SupportedOS: 
    print(f"{err} sorry, this system isn't compatble with builder. Command used to build: {cmd_to_build}")
progress('All requirements are met, building application...')
shell(cmd_to_build)
progress('Build complete, cleaning up...')
build_name = f'smoc-{platform.system().lower()}'
shell('rm -rf build main.spec')
shell(f'mv dist/main ./{build_name}')
shell('rm -rf dist')
print(f'{color.foreground_st.green}{font.bold}Done! Your application was build successfuly, it located by name: {build_name}{color.end}')