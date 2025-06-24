from cx_Freeze import setup, Executable
import os

# Folder where your assets live relative to setup.py
assets_folder = "assets"
classes_folder = "classes"

build_exe_options = {
    "packages": ["ursina", "ursina.application", "ursina.window", "ursina.color"],
    "include_files": [
        (assets_folder, "assets"),  # copies whole assets folder into build
        (classes_folder, "classes"),
    ],
}

setup(
    name="UrsinaGame",
    version="0.1",
    description="My Ursina game",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py")]
)
