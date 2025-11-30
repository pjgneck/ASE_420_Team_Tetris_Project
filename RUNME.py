import os
import platform
import subprocess
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
build_file = os.path.join(script_dir, "build.py")
req_file = os.path.join(script_dir, "requirements.txt")


# Step 1: Install dependencies
print("\n🔹 Installing dependencies...\n")
subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_file])

# Step 2: Run build.py
print("\n🔹 Building the executable...\n")
subprocess.check_call([sys.executable, build_file])

# Step 3: Locate the executable
dist_dir = "dist"
exe_name = "TetrisBOOM"  # match the name in build.py

exe_file = os.path.join(dist_dir, exe_name)
if platform.system() == "Windows":
    exe_file += ".exe"
else:
    if os.path.exists(exe_file):
        os.chmod(exe_file, 0o755)

# Step 4: Run the executable
print(f"\n🔹 Running {exe_file}...\n")
subprocess.check_call([exe_file])
