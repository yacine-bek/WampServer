---

# WampServer Auto Setup Helper

This small utility helps you handle the required dependencies to install **WampServer** smoothly.

## 📌 Requirements

Make sure **Python** is installed on your machine before proceeding.  
(You can download it from [python.org](https://www.python.org/downloads/)).

---

## 🚀 Installation Steps

1. **Download WampServer**  
   Get the latest installer from [this link](https://sourceforge.net/projects/wampserver/files/latest/download).

2. **Start the Setup**  
   Begin the WampServer installation. When you encounter the "missing requirements" error, **pause the setup**.

3. **Run the Dependency Installer**  
   Open a terminal with **administrator privileges**, then run:

   ```bash
   python start.py
   ```

   This script will install the required dependencies for WampServer.

4. **Continue Installation**  
   Once the script finishes, go back to the WampServer setup and continue the installation.

✅ **All done!**

---

## 🧹 Uninstalling Dependencies

If you want to remove the dependencies added by `start.py`, you can use the `remove.py` script:

```bash
python remove.py
```

---

## 💡 Notes

- Always run `start.py` and `remove.py` as administrator.
- This script is intended to streamline setup on fresh systems that don’t meet WampServer’s prerequisites.

--
