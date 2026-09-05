"""Dedicated launcher for the interactive SIH demonstration web dashboard."""

import sys
from visualization.dashboard import start_demo_server

if __name__ == "__main__":
    port_arg = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    start_demo_server(port=port_arg)
