#!/usr/bin/env python3
"""Convenience script to run all 11 scientific benchmark experiments."""

import subprocess
import sys
import os

if __name__ == "__main__":
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sys.exit(subprocess.call([sys.executable, "main.py", "--run-all-experiments"], cwd=root_dir))
