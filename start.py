import os
import sys
import ctypes
import subprocess
import zipfile
import shutil

#Relaunch with admin rights if not already elevated
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    print("Requesting admin privileges...")
    script = sys.executable
    params = ' '.join([f'"{arg}"' for arg in sys.argv])
    # Relaunch the script with admin
    ctypes.windll.shell32.ShellExecuteW(None, "runas", script, params, None, 1)
    sys.exit()

#Ensure requests is installed
try:
    import requests
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

# Setup
url = "https://wampserver.aviatechno.net/files/vcpackages/all_vc_redist_x86_x64.zip"
zip_path = "vc_redists.zip"
extract_dir = "vc_redists"
allowed_executables = {
    "vcredist_2010_sp1_x64.exe",
    "vcredist_2010_sp1_x86.exe",
    "vcredist_2012_upd4_x64.exe",
    "vcredist_2012_upd4_x86.exe",
    "vcredist_2013_upd5_x64.exe",
    "vcredist_2013_upd5_x86.exe",
    "vcredist_2022_x64.exe",
    "vcredist_2022_x86.exe",
}

#Download
print("Downloading redistributables ZIP...")
response = requests.get(url)
with open(zip_path, "wb") as f:
    f.write(response.content)
print("Download done.")

#Extract
print("Extracting files...")
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)
print("Extraction complete.")

#Run selected redistributables
print("Installing selected packages...")
for root, dirs, files in os.walk(extract_dir):
    for file in files:
        if file in allowed_executables:
            exe_path = os.path.join(root, file)
            print(f"Running: {exe_path}")
            subprocess.run([exe_path, "/quiet", "/norestart"], check=True)

#Cleanup
print("Cleaning up...")
os.remove(zip_path)
shutil.rmtree(extract_dir)
print("Installation complete and cleanup done.")
