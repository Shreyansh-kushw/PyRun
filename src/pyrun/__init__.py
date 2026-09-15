import subprocess
import sys

def main():
    subprocess.run([sys.executable, "src/pyrun/run.py", "src/pyrun/test.py"])