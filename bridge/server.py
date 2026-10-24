"""Local MSFS SimConnect telemetry bridge; simulator-only. Run on Windows PC with MSFS."""
import json
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread, Lock

HOST, PORT = '127.0.0.1', 8765
state = {'connected': False, 'error': 'Waiting for MSFS connection', 'updated_at': None}
lock = Lock()

def poll_sim():
    while True:
        try:
            from SimConnect import SimConnect, AircraftRequests
            sm = SimConnect()
            aq = AircraftRequests(sm, _time=1000)
            names = {
                'latitude': ('PLANE_LATITUDE', 1),
                'longitude': ('PLANE_LONGITUDE', 1),
                'altitude_ft': ('PLANE_ALTITUDE', 1),
                'groundspeed_kt': ('GPS_GROUND_SPEED', 1),
                'fuel_gallons': ('FUEL_TOTAL_QUANTITY', 1),
                'fuel_weight_lb_per_gal': ('FUEL_WEIGHT_PER_GALLON', 1),
                'weight_lb': ('TOTAL_WEIGHT', 1),
            }
            while True:
                vals = {k: aq.get(v[0]) for k, v in names.items()}
                if vals['latitude'] is None or vals['longitude'] is None:
                    raise RuntimeError('No aircraft position returned')
                gallons = vals.pop('fuel_gallons')
                density = vals.pop('fuel_weight_lb_per_gal')
                weight = vals.pop('weight_lb')
                vals['fuel_kg'] = gallons * density * 0.45359237 if gallons is not None and density is not None else None
                vals['weight_kg'] = weight * 0.45359237 if weight is not None else None
                with lock:
                    state.update(vals, connected=True, error=None, updated_at=time.time())
                time.sleep(1)
        except Exception as exc:
            with lock:
                state.update(connected=False, error=str(exc)[:180], updated_at=time.time())
            time.sleep(4)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != '/api/telemetry':
            self.send_error(404); return
        with lock:
            result = dict(state)
        if result['updated_at'] and time.time() - result['updated_at'] > 5:
            result['connected'] = False
            result['error'] = 'Telemetry stale'
        payload = json.dumps(result, allow_nan=False).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

if __name__ == '__main__':
    Thread(target=poll_sim, daemon=True).start()
    print(f'SimConnect bridge listening on http://{HOST}:{PORT}/api/telemetry')
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
