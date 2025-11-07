import os
import platform
import PyInstaller.__main__

# detect the correct path separator
sep = ";" if platform.system() == "Windows" else ":"

# construct the add-data arguments
add_data = [
    f"tetris_boom/assets{sep}tetris_boom/assets",
    f"tetris_boom/game{sep}tetris_boom/game",
]

# build arguments
args = [
    "tetris_boom/main.py",
    "--onefile",
    "--noconsole",
    "--name=TetrisBOOM",
]

# add folders
for data in add_data:
    args.append(f"--add-data={data}")

# run PyInstaller
PyInstaller.__main__.run(args)

print("\nBuild complete! Executable is in the 'dist' folder.\n")
