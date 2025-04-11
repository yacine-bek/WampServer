import os
import sys
import ctypes
import subprocess
import winreg
import requests

# ------------------- ADMIN CHECK -------------------
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    print("Requesting admin rights...")
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join([f'"{arg}"' for arg in sys.argv]), None, 1)
    sys.exit()

# ------------------- 1. UNINSTALL 2010–2013 via Registry -------------------
target_names = [
    "Microsoft Visual C++ 2010  x64 Redistributable - 10.0.40219",
    "Microsoft Visual C++ 2010  x86 Redistributable - 10.0.40219",
    "Microsoft Visual C++ 2012 Redistributable (x64) - 11.0.61030",
    "Microsoft Visual C++ 2012 Redistributable (x86) - 11.0.61030",
    "Microsoft Visual C++ 2013 Redistributable (x64) - 12.0.40664",
    "Microsoft Visual C++ 2013 Redistributable (x86) - 12.0.40664"
]

def uninstall_registry_entries():
    uninstall_keys = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]
    count = 0
    for root in [winreg.HKEY_LOCAL_MACHINE]:
        for path in uninstall_keys:
            try:
                with winreg.OpenKey(root, path) as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            with winreg.OpenKey(key, subkey_name) as subkey:
                                name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                if name in target_names:
                                    uninstall_cmd = winreg.QueryValueEx(subkey, "UninstallString")[0]
                                    print(f"\n→ Uninstalling (Registry): {name}")
                                    if "msiexec" in uninstall_cmd.lower():
                                        uninstall_cmd += " /quiet /norestart"
                                        subprocess.run(uninstall_cmd, shell=True)
                                    else:
                                        subprocess.run(f'start /wait "" {uninstall_cmd} /quiet /norestart', shell=True)
                                    count += 1
                        except Exception:
                            continue
            except FileNotFoundError:
                continue
    return count

# ------------------- 2. UNINSTALL 2015–2022 using Official .exe -------------------
def uninstall_2015_to_2022():
    urls = {
        "vcredist_2022_x64.exe": "https://aka.ms/vs/17/release/vc_redist.x64.exe",
        "vcredist_2022_x86.exe": "https://aka.ms/vs/17/release/vc_redist.x86.exe"
    }

    print("\n📥 Downloading Microsoft 2015–2022 uninstallers...")
    for filename, url in urls.items():
        response = requests.get(url)
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"✅ Downloaded: {filename}")

    print("\n🧨 Uninstalling 2015–2022 Redistributables...")
    for filename in urls:
        subprocess.run([os.path.abspath(filename), "/uninstall", "/quiet", "/norestart"], shell=True)
        print(f"→ Uninstalled: {filename}")

    print("\n🧹 Cleaning up downloaded uninstallers...")
    for filename in urls:
        if os.path.exists(filename):
            os.remove(filename)
            print(f"🗑️ Deleted: {filename}")

# ------------------- EXECUTION -------------------
print("🔧 Starting full Visual C++ cleanup (2010–2022)...")
removed_old = uninstall_registry_entries()
print(f"\n✅ {removed_old} old redistributables uninstalled (2010–2013).")

uninstall_2015_to_2022()
print("\n🎉 Done. All Visual C++ Redistributables removed.")
