import os
import platform
import requests
import zipfile
import shutil
from pathlib import Path

def download_ffmpeg(download_url, output_dir):
    response = requests.get(download_url, stream=True)
    zip_path = Path(output_dir) / "ffmpeg.zip"
    with open(zip_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)

    os.remove(zip_path)

def setup_ffmpeg():
    # Determine the platform and set the download URL
    system_platform = platform.system().lower()
    if system_platform == "windows":
        download_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"  # Example URL
    elif system_platform == "linux":
        download_url = "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-i686-static.tar.xz"  # Example URL
    elif system_platform == "darwin":
        download_url = "https://evermeet.cx/ffmpeg/ffmpeg-4.4.1-macos64-static.zip"  # Example URL
    else:
        raise Exception("Unsupported OS")

    # Create a directory for ffmpeg
    output_dir = Path("ffmpeg")
    output_dir.mkdir(exist_ok=True)

    # Download and extract ffmpeg
    if not any(Path(output_dir).glob("ffmpeg*")):
        print("Downloading ffmpeg...")
        download_ffmpeg(download_url, output_dir)
    
    # Add ffmpeg to PATH
    if system_platform == "windows":
        ffmpeg_bin = output_dir / "ffmpeg/bin"
        os.environ["PATH"] += os.pathsep + str(ffmpeg_bin)
    else:
        ffmpeg_bin = output_dir / "ffmpeg"
        shutil.copytree(ffmpeg_bin, "/usr/local/bin/ffmpeg", dirs_exist_ok=True)

    print("ffmpeg setup complete.")

if __name__ == "__main__":
    setup_ffmpeg()
