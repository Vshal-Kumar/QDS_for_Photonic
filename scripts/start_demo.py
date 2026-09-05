#!/usr/bin/env python3
"""Convenience script to launch the interactive SIH demonstration web dashboard."""

import subprocess
import sys
import os

if __name__ == "__main__":
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sys.exit(subprocess.call([sys.executable, "main.py", "--demo"], cwd=root_dir))
