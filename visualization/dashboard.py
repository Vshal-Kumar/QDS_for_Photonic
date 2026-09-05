"""Lightweight Built-in HTTP and API Server for the Interactive SIH Demonstration."""

import http.server
import json
import os
import socketserver
import sys
from typing import Optional

from core.simulator import QDSThreatSimulator


class DashboardHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP Request Handler serving static web files and JSON simulation API."""
    
    simulator: QDSThreatSimulator = None
    
    def __init__(self, *args, **kwargs):
        static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "web", "static"))
        super().__init__(*args, directory=static_dir, **kwargs)
        
    def do_POST(self):
        """Handle POST /api/simulate requests."""
        if self.path == "/api/simulate":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            
            try:
                params = json.loads(body) if body else {}
                
                msg = params.get("message", "Transfer 1000 Quantum Credits to Bob")
                distance_km = float(params.get("distance_km", 50.0))
                shots = int(params.get("shots", 1000))
                atk_type = params.get("attack_type", "none")
                atk_strength = float(params.get("attack_strength", 0.0))
                
                # Protocol role overrides for impersonation / unauthorized verifier
                signer_id = "Alice"
                verifier_id = "Bob"
                is_replay = False
                
                if atk_type.lower() == "impersonation":
                    signer_id = "Eve_Pretending_Alice"
                elif atk_type.lower() == "unauthorized_verification":
                    verifier_id = "Eve_Rogue_Verifier"
                elif atk_type.lower() == "replay":
                    is_replay = True
                    
                if DashboardHTTPRequestHandler.simulator is None:
                    DashboardHTTPRequestHandler.simulator = QDSThreatSimulator()
                    
                sim_res = DashboardHTTPRequestHandler.simulator.run_simulation(
                    message_text=msg,
                    distance_km=distance_km,
                    attack_type=atk_type,
                    attack_strength=atk_strength,
                    shots=shots,
                    signer_id=signer_id,
                    verifier_id=verifier_id,
                    is_replay=is_replay
                )
                
                res_dict = sim_res.to_dict()
                response_bytes = json.dumps(res_dict).encode("utf-8")
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(response_bytes)))
                self.end_headers()
                self.wfile.write(response_bytes)
                
            except Exception as e:
                err_dict = {"error": str(e)}
                err_bytes = json.dumps(err_dict).encode("utf-8")
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(err_bytes)))
                self.end_headers()
                self.wfile.write(err_bytes)
        else:
            self.send_error(404, "Endpoint not found")
            
    def log_message(self, format, *args):
        # Suppress noisy standard request logging in console
        pass


def start_demo_server(port: int = 8000, host: str = "0.0.0.0") -> None:
    """Launch the interactive web demo server."""
    DashboardHTTPRequestHandler.simulator = QDSThreatSimulator()
    
    # Allow address reuse to prevent port binding conflicts
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((host, port), DashboardHTTPRequestHandler) as httpd:
        print("=" * 70)
        print(f"🚀 Interactive SIH QDS Threat Detection Server running at http://localhost:{port}")
        print("   Press Ctrl+C to stop the demonstration server.")
        print("=" * 70)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
            httpd.shutdown()


if __name__ == "__main__":
    port_arg = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    start_demo_server(port=port_arg)
