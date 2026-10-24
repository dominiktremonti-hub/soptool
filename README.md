# Airbus Operations v0.4.0 — Browser & iPad Responsive EFB

Simulator-only prototype. All checklist steps are illustrative and are **not** validated aircraft procedures.

## Run

Requires Node.js 20+. Run `npm install` and `npm run dev` in this folder. Open the displayed local URL. For a production build use `npm run build`.

## iPad / responsive design

The interface adapts to both portrait and landscape orientations, including iPad Safari and desktop browsers. On iPad, open the site in Safari and use Share → Add to Home Screen. Installable PWA features require HTTPS or localhost. Browser data (checklist completion, flight session and bridge URL) is stored **locally on each device** and is not synchronized. Offline access requires successful initial loading and service-worker caching.

For testing on the same Wi-Fi network, run Vite on the PC, then open `http://PC-LAN-IP:5173` on the iPad. This HTTP testing URL may not allow full install/offline features on iPad; use trusted HTTPS for deployment.

## SimConnect bridge

The optional Python bridge remains Windows-only and must run on the PC with MSFS 2024. Install bridge requirements and run `py server.py` inside `bridge`. The bridge is **loopback-only by default** and cannot be reached directly from an iPad. The app now offers a configurable bridge URL, but iPad telemetry needs a secure authenticated HTTPS relay or reverse proxy, **not provided**. HTTPS sites may block HTTP bridge calls. Never expose port 8765 publicly.

## Known limitations

SimBrief import may be blocked by CORS. Navigraph charts are linked externally. No alternate rankings, live weather, NOTAM or landing performance. Simulator live connectivity is untested.
