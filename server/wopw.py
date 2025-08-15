class wopw:
    '# Internal class for checking version, imports (for funcs)\n\nVariables:\n\n- Version: int; a version in int for CheckVersion()\n- VersionType: str; an version type like beta or release\n- BuildCount: int; for counting build (ex. 10A1; where 1 is BuildCount)\n- Build: str; just a build'
    import subprocess, platform, os, sys
    Version = 1.0
    VersionType = 'Beta' # Alpha, Beta, Release
    BuildCount = 2
    Build = f'{str(Version).replace('.', '')}{VersionType[0]}{BuildCount}'
    # Variables
    OS = platform.system()
    OSVersion = platform.release()
    
    # Modules/Classes
    def CheckVersion():
        '''# Requires module "requests" and internet connection
# Checks for lastest version of Wopw

# Returns:

- **1: Version is newest**
- **2: Version is spoofed (current version is bigger that newest)**
- **-1: Version outdated**
- **-2: No module "requests"**
- **-3: Unknown error while requestsing version**'''
        try: import requests
        except ModuleNotFoundError: return -2
        try:
            cache = float(requests.get('https://dev4ones.space/requests/2jLlU9_xXoLveORWrDvRXkqhCvGQIhundvKwmMuuKhKeqwXuP1zq727UtIcnfuXV').content.decode('ascii'))
            if wopw.Version < cache: return -1
            else: 
                if wopw.Version > cache: return 2
                return 1
        except EOFError: return -3
class AppleScript:
    '# For macOS only! Class for funcs with integration with macOS'
    def MakeNotification(Description: str, Title: str | None = None, Subtitle: str | None = None, Sound: str | None = 'Ping', CareAboutTextExceptions: bool | None = True):
        '''# Will make an notification. Requires agreeing a notification access from "Script Editor" on newer macOS

# Variables:

- **Description: str; Text (main) of notification**
- **Title: str | None = None; Title of notification**
- **Subtitle: str | None = None; Subtitle of notification**
- **Sound: str | None = 'Ping'; Sound which will be used when notification is showed**
- **CareAboutTextExceptions: bool | None = True; Used to disable calling -1 return, except just removing prohibited symbols from text**

# Returns (out):

- **-2: If Description, Title, Subtitle is bigger that 240 characters**
- **-1: Wrong value for: Description, Title, Subtitle; Make sure none of them don't contains symbols like: ", $**
- **-3: Non-macOS system running**

**Any other - AppleScript out**''' # originally was made for apple script to python project, but was left unuploaded
        if wopw.OS != 'Darwin': return -3
        try:
            if CareAboutTextExceptions == False: 
                Title = Title.replace('"', '').replace('$', '')
                Description = Description.replace('"', '').replace('$', '')
                Subtitle = Subtitle.replace('"', '').replace('$', '')
            else:
                if Title.find('"') != -1 or Title.find('$') != -1 or Subtitle.find('"') != -1 or Subtitle.find('$') != -1 or Description.find('"') != -1 or Description.find('$') != -1: return -1
        except: pass
        if Title == None: applescript = f'display notification "{Description}"'
        else:
            applescript = f'display notification "{Description}" with title "{Title}"'
            if Subtitle != None: applescript = f'{applescript} subtitle "{Subtitle}"'
            applescript = f'{applescript} sound name "{Sound}"'
        return wopw.subprocess.check_output(f"osascript -e '{applescript}'", shell=True).decode('ascii')
def cls():
    '# Clears terminal screen\n# Supports: Windows, Linux, macOS (Darwin)'
    if wopw.OS == 'Windows': wopw.os.system('cls')
    else: wopw.os.system('clear')
class machine:
    def GetWindowsActivationKey():
        '# Supports: Windows\n# Requires Administrator access!\n\n# Returns:\n\n- **-1: Not found**\n- **-2: Not a Windows OS**'
        if wopw.OS != 'Windows': -2
        try:
            key_result = wopw.subprocess.check_output(
                "powershell (Get-WmiObject -Query 'Select * from SoftwareLicensingService').OA3xOriginalProductKey",
                shell=True, stderr=wopw.subprocess.PIPE, text=True
            )
            product_key = key_result.strip()
        except: -1
    def GetSerialNumber():
        '# Supports: macOS (Darwin), Windows, Linux\n# For Linux: requires sudo access\n\n# Returns:\n\n- **-1: Got error while trying to get SN**'
        OS = wopw.OS
        if OS == 'Darwin':
            try: return wopw.subprocess.run("ioreg -l | grep IOPlatformSerialNumber | awk -F'\"' '{print $4}'", capture_output=True, text=True, shell=True, check=True).stdout.strip()
            except wopw.subprocess.CalledProcessError: return -1
        elif OS == 'Windows':
            try: return wopw.subprocess.check_output("wmic bios get serialnumber", shell=True, stderr=wopw.subprocess.PIPE, text=True).strip().split("\n")[-1].strip()
            except: return -1
        elif OS == 'Linux':
            try:
                commands = ["sudo dmidecode -s system-serial-number", "cat /sys/class/dmi/id/product_serial", "sudo lshw -class system | grep serial | head -1"]
                serial = ''
                for cmd in commands:
                    try:
                        result = wopw.subprocess.check_output(cmd, shell=True, stderr=wopw.subprocess.PIPE, text=True)
                        if result.strip():
                            serial = result.strip()
                            break
                    except: continue
                return serial
            except: return -1
class dev4ones_modules:
    '# Supports: macOS (Darwin), Windows, Linux\n# Compilation of module from projects of dev4ones (author of this module)'
    def DefExitPrompt(text: str | None = 'Done!'): input(f'{text}\n\npress enter to exit')
class color:
    '# Supports: macOS (Darwin)\n# Colors for print\n\nExample usage:\n\nprint(f"{print.foreground_st.blue}Proccessing{print.end}") - will display "Proccessing" in blue color'
    class foreground_st:
        '# Start foreground of colors\nUsed to start color of text'
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        yellow = '\033[33m'
        blue = '\033[34m'
        magenta = '\033[35m'
        cyan = '\033[36m'
        white = '\033[37m'
    class background_st:
        '# Start background of colors\nUsed to start color of background text'
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        yellow = '\033[43m'
        blue = '\033[44m'
        magenta = '\033[45m'
        cyan = '\033[46m'
        white = '\033[47m'
    end = '\033[0m'
class font:
    '# Supports: macOS (Darwin)\n# Example usage: print(f"{font.bold}bold{font.end} default text")\nResult: **bold** default text'
    bold = '\033[1m'
    dim_faint = '\033[2m'
    italic = '\033[3m'
    underline = '\033[4m'
    blink = '\033[5m'
    inverse = '\033[7m'
    hidden = '\033[8m'
    strikethrough = '\033[9m'
    end = '\033[0m'