import os
import subprocess
import platform
import sys
from setuptools import setup, find_packages
from distutils.command.install import install

def is_admin():
    try:
        if platform.system() == 'Windows':
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        else:
            return os.geteuid() == 0
    except AttributeError:
        return False

def run_as_admin():
    if platform.system() == 'Windows':
        import ctypes
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
    else:
        os.execvp('sudo', ['sudo', sys.executable] + sys.argv)

if not is_admin():
    print("This script requires administrative privileges. Attempting to restart with elevated permissions...")
    run_as_admin()
    sys.exit(0)

def request_firewall_exception():
    if platform.system() == "Darwin":
        print("Please manually add this application to your macOS firewall exceptions.")
    else:
        print("Firewall exception setup is not automated for this operating system.")

def add_firewall_exception():
    if platform.system() == "Linux":
        print("Requesting firewall exception for the application...")
        subprocess.run(["bash", "src/add_firewall_exception_linux.sh"], check=True)
    elif platform.system() == "Windows":
        print("Requesting firewall exception for the application...")
        subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "src/add_firewall_exception_windows.ps1"], check=True)
    else:
        print("Firewall exception setup is not automated for this operating system.")

def install_ffmpeg():
    subprocess.run([sys.executable, "src/setup_ffmpeg.py"], check=True)

class PostInstallCommand(install):
    def run(self):
        install.run(self)
        self.create_shortcut()

    def create_shortcut(self):
        if platform.system() == 'Windows':
            self.create_windows_shortcut()
        elif platform.system() == 'Darwin':
            self.create_mac_shortcut()
        elif platform.system().startswith('linux'):
            self.create_linux_shortcut()
        else:
            print("Unsupported platform. Shortcut creation is not supported.")

    def create_windows_shortcut(self):
        try:
            import winshell
            from win32com.client import Dispatch
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "winshell", "pywin32"])
            import winshell
            from win32com.client import Dispatch

        desktop = winshell.desktop()
        path = os.path.join(desktop, "ScreenAudioRecorder.lnk")
        target = os.path.join(sys.prefix, 'src', 'main.py')
        wDir = os.path.join(sys.prefix, 'src')
        icon = target

        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = wDir
        shortcut.IconLocation = icon
        shortcut.save()
        print(f"Shortcut created at {path}")

    def create_mac_shortcut(self):
        script = '''
        tell application "Finder"
            make new alias file to POSIX file "{target}" at POSIX file "{desktop}"
            set name of result to "ScreenAudioRecorder"
        end tell
        '''.format(target=os.path.join(sys.prefix, 'src', 'main.py'), desktop=os.path.join(os.path.expanduser("~"), "Desktop"))
        
        os.system("osascript -e '{}'".format(script))
        print("Shortcut created on macOS Desktop")

    def create_linux_shortcut(self):
        desktop_file_content = '''
        [Desktop Entry]
        Name=ScreenAudioRecorder
        Exec=python3 {target}
        Icon={icon}
        Terminal=false
        Type=Application
        '''.format(target=os.path.join(sys.prefix, 'src', 'main.py'), icon=os.path.join(sys.prefix, 'src', 'main.py'))
        
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "ScreenAudioRecorder.desktop")
        
        with open(desktop_path, 'w') as desktop_file:
            desktop_file.write(desktop_file_content)
        
        os.chmod(desktop_path, 0o755)
        print("Shortcut created on Linux Desktop")

def create_virtualenv():
    if not os.path.exists('.venv'):
        subprocess.check_call([sys.executable, '-m', 'venv', '.venv'])
    
    venv_python = os.path.join('.venv', 'Scripts', 'python.exe') if platform.system() == 'Windows' else os.path.join('.venv', 'bin', 'python')
    subprocess.check_call([venv_python, '-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([venv_python, '-m', 'pip', 'install', '-r', 'requirements.txt'])

create_virtualenv()
install_ffmpeg()
request_firewall_exception()
add_firewall_exception()

setup(
    name='screen_audio_recorder',
    version='0.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'pyqt5',
        'pyaudio',
        'pydub',
        'opencv-python',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'screen_audio_recorder = main:main'
        ]
    },
    include_package_data=True,
    cmdclass={
        'install': PostInstallCommand,
    },
)
