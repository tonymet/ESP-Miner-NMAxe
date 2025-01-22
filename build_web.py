import os
import subprocess
from shutil import copytree, rmtree, copy2
from os.path import join, isdir, basename, splitext
from sys import platform
import hashlib


project_dir = os.getenv("PROJECT_DIR", os.getcwd())
if not project_dir:
    raise ValueError("PROJECT_DIR environment variable is not set")


web_src_dir = join(project_dir, "src", "http_server", "axe-os")
dist_dir = join(web_src_dir, "dist", "axe-os")
data_dir = join(project_dir, "data")

# default to linux + darwin npm
npm = "npm"
if platform == "win32":
    npm = "npm.cmd"

if isdir(data_dir):
    rmtree(data_dir)

subprocess.run([npm, "install"], cwd=web_src_dir, check=True)
subprocess.run([npm, "run", "build"], cwd=web_src_dir, check=True)

os.makedirs(data_dir)

for root, _, files in os.walk(dist_dir):
    for file in files:
        src_file = join(root, file)
        dest_file = join(data_dir, file)
        copy2(src_file, dest_file)