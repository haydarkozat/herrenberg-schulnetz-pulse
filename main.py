"""
Herrenberg SchulNetz-Pulse
==========================
Automatisierungs- & Überwachungspanel für 14 Schulstandorte.
Concept Demo für #teamstadtherrenberg.

Entwickelt von: Haydar Kozat

Diese Anwendung ist eine eigenständige Demo. Sämtliche Daten sind simuliert
(Mock von NinjaOne / UniFi Controller / Xurrent / OPNsense), es bestehen keine
Verbindungen zu echten Systemen.
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Herrenberg SchulNetz-Pulse")

# Jinja2 liest die Templates aus dem aktuellen Verzeichnis.
# Die "index.html" wird beim Aufruf der Route zur Laufzeit geschrieben.
templates = Jinja2Templates(directory=".")


# ---------------------------------------------------------------------------
# Simulierte Bestandsdaten der 14 Schulstandorte in Herrenberg
# ---------------------------------------------------------------------------
SCHOOLS_DATA = [
    {"id": 1,  "name": "Schickhardt-Gymnasium",            "status": "Online",   "ap_count": 48, "clients": 612, "fw_version": "OPNsense 24.1"},
    {"id": 2,  "name": "Andreae-Gymnasium",                "status": "Warning",  "ap_count": 41, "clients": 503, "fw_version": "OPNsense 23.7"},
    {"id": 3,  "name": "Theodor-Schüz-Realschule",         "status": "Online",   "ap_count": 33, "clients": 421, "fw_version": "OPNsense 24.1"},
    {"id": 4,  "name": "Vogt-Heß-Gymnasium",               "status": "Online",   "ap_count": 37, "clients": 458, "fw_version": "OPNsense 24.1"},
    {"id": 5,  "name": "Längenholz-Grundschule",           "status": "Critical", "ap_count": 16, "clients": 0,   "fw_version": "OPNsense 23.1"},
    {"id": 6,  "name": "Markweg-Grundschule",              "status": "Online",   "ap_count": 14, "clients": 188, "fw_version": "OPNsense 24.1"},
    {"id": 7,  "name": "Grundschule Mühlstraße",           "status": "Online",   "ap_count": 12, "clients": 161, "fw_version": "OPNsense 24.1"},
    {"id": 8,  "name": "Grundschule Affstätt",             "status": "Online",   "ap_count": 9,  "clients": 102, "fw_version": "OPNsense 24.1"},
    {"id": 9,  "name": "Grundschule Kuppingen",            "status": "Warning",  "ap_count": 11, "clients": 134, "fw_version": "OPNsense 23.7"},
    {"id": 10, "name": "Grundschule Gültstein",            "status": "Online",   "ap_count": 10, "clients": 119, "fw_version": "OPNsense 24.1"},
    {"id": 11, "name": "Grundschule Haslach",              "status": "Online",   "ap_count": 8,  "clients": 91,  "fw_version": "OPNsense 24.1"},
    {"id": 12, "name": "Theodor-Heuss-Schule",            "status": "Online",   "ap_count": 22, "clients": 276, "fw_version": "OPNsense 24.1"},
    {"id": 13, "name": "Friedrich-Fröbel-Schule (SBBZ)",   "status": "Online",   "ap_count": 13, "clients": 147, "fw_version": "OPNsense 24.1"},
    {"id": 14, "name": "Pestalozzischule Herrenberg",      "status": "Online",   "ap_count": 15, "clients": 173, "fw_version": "OPNsense 24.1"},
]


# ---------------------------------------------------------------------------
# HTML-Template (Tailwind CSS via CDN, Dark Mode)
# ---------------------------------------------------------------------------
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Herrenberg SchulNetz-Pulse</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-900 text-gray-100 min-h-screen">
    <div class="max-w-7xl mx-auto px-4 py-8">

        <!-- Header -->
        <header class="border-b border-gray-700 pb-6 mb-8">
            <div class="flex items-center gap-3">
                <span class="inline-flex h-3 w-3 rounded-full bg-green-400 animate-pulse"></span>
                <h1 class="text-3xl md:text-4xl font-bold tracking-tight">Herrenberg SchulNetz-Pulse</h1>
            </div>
            <p class="mt-2 text-gray-400">
                Automatisierungs- &amp; Überwachungspanel für 14 Schulstandorte
                (Concept Demo für <span class="text-sky-400 font-semibold">#teamstadtherrenberg</span>)
            </p>
            <p class="mt-1 text-sm text-gray-500">
                Entwickelt von <span class="font-semibold text-gray-300">Haydar Kozat</span>
            </p>
        </header>

        <!-- Automation Action Buttons -->
        <section class="mb-10">
            <div class="flex items-center justify-between mb-4">
                <h2 class="text-xl font-semibold">Automation Actions</h2>
                <span class="text-xs uppercase tracking-wider bg-gray-800 text-gray-400 px-3 py-1 rounded-full border border-gray-700">
                    NinjaOne &amp; UniFi API Mock
                </span>
            </div>
            <div class="flex flex-col sm:flex-row gap-4">
                <form action="/maintain" method="post" class="flex-1">
                    <button type="submit"
                        class="w-full bg-indigo-600 hover:bg-indigo-500 transition-colors text-white font-semibold py-3 px-6 rounded-lg shadow-lg shadow-indigo-900/40 flex items-center justify-center gap-2">
                        🛠️ Automatisierte Nachtwartung starten
                    </button>
                </form>
                <form action="/sync-xurrent" method="post" class="flex-1">
                    <button type="submit"
                        class="w-full bg-amber-600 hover:bg-amber-500 transition-colors text-white font-semibold py-3 px-6 rounded-lg shadow-lg shadow-amber-900/40 flex items-center justify-center gap-2">
                        🔄 Offene Vorfälle mit Xurrent synchronisieren
                    </button>
                </form>
            </div>
        </section>

        <!-- Status Summary -->
        <section class="grid grid-cols-3 gap-4 mb-10">
            <div class="bg-gray-800 border border-gray-700 rounded-lg p-4 text-center">
                <p class="text-2xl font-bold text-green-400">{{ schools | selectattr('status', 'equalto', 'Online') | list | length }}</p>
                <p class="text-xs uppercase tracking-wider text-gray-500 mt-1">Online</p>
            </div>
            <div class="bg-gray-800 border border-gray-700 rounded-lg p-4 text-center">
                <p class="text-2xl font-bold text-yellow-400">{{ schools | selectattr('status', 'equalto', 'Warning') | list | length }}</p>
                <p class="text-xs uppercase tracking-wider text-gray-500 mt-1">Warning</p>
            </div>
            <div class="bg-gray-800 border border-gray-700 rounded-lg p-4 text-center">
                <p class="text-2xl font-bold text-red-400">{{ schools | selectattr('status', 'equalto', 'Critical') | list | length }}</p>
                <p class="text-xs uppercase tracking-wider text-gray-500 mt-1">Critical</p>
            </div>
        </section>

        <!-- School Grid -->
        <section>
            <h2 class="text-xl font-semibold mb-4">Schulstandorte</h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
                {% for school in schools %}
                {% if school.status == 'Online' %}
                    {% set border = 'border-green-500/60' %}
                    {% set badge = 'bg-green-500/20 text-green-300 border border-green-500/40' %}
                    {% set dot = 'bg-green-400' %}
                {% elif school.status == 'Warning' %}
                    {% set border = 'border-yellow-500/60' %}
                    {% set badge = 'bg-yellow-500/20 text-yellow-300 border border-yellow-500/40' %}
                    {% set dot = 'bg-yellow-400' %}
                {% else %}
                    {% set border = 'border-red-500/70' %}
                    {% set badge = 'bg-red-500/20 text-red-300 border border-red-500/40' %}
                    {% set dot = 'bg-red-400' %}
                {% endif %}
                <div class="bg-gray-800 rounded-xl p-5 border-l-4 {{ border }} shadow-md hover:shadow-xl transition-shadow">
                    <div class="flex items-start justify-between gap-2">
                        <h3 class="font-semibold text-gray-100 leading-snug">{{ school.name }}</h3>
                        <span class="shrink-0 inline-flex items-center gap-1.5 text-xs font-semibold px-2.5 py-1 rounded-full {{ badge }}">
                            <span class="h-2 w-2 rounded-full {{ dot }}"></span>{{ school.status }}
                        </span>
                    </div>

                    <div class="grid grid-cols-3 gap-2 mt-4 text-center">
                        <div class="bg-gray-900/60 rounded-lg py-2">
                            <p class="text-lg font-bold text-gray-100">{{ school.ap_count }}</p>
                            <p class="text-[10px] uppercase tracking-wider text-gray-500">Access Points</p>
                        </div>
                        <div class="bg-gray-900/60 rounded-lg py-2">
                            <p class="text-lg font-bold text-gray-100">{{ school.clients }}</p>
                            <p class="text-[10px] uppercase tracking-wider text-gray-500">Clients</p>
                        </div>
                        <div class="bg-gray-900/60 rounded-lg py-2">
                            <p class="text-[11px] font-bold text-gray-100 leading-tight mt-1">{{ school.fw_version }}</p>
                            <p class="text-[10px] uppercase tracking-wider text-gray-500">Firewall</p>
                        </div>
                    </div>

                    {% if school.status == 'Critical' %}
                    <div class="mt-4 bg-red-950/60 border border-red-500/40 rounded-lg p-3">
                        <p class="text-sm font-semibold text-red-300 flex items-center gap-2">⚠️ Standort nicht erreichbar</p>
                        <p class="text-xs text-red-200/80 mt-1">
                            <span class="font-semibold">UniFi Controller</span> meldet keine Heartbeats mehr.
                            Automatisch generierter <span class="font-semibold">Xurrent Ticket-Payload</span>
                            steht zur Synchronisierung bereit.
                        </p>
                    </div>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
        </section>

        <!-- Footer -->
        <footer class="mt-12 pt-6 border-t border-gray-700 text-center text-xs text-gray-600">
            Concept Demo &middot; Alle Daten simuliert (NinjaOne / UniFi / Xurrent / OPNsense Mock) &middot;
            &copy; 2026 Haydar Kozat &middot; #teamstadtherrenberg
        </footer>
    </div>
</body>
</html>"""


def _write_template() -> None:
    """Schreibt das HTML-Template auf die Platte, damit Jinja2 es lesen kann."""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(HTML_TEMPLATE)


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Rendert das Dashboard mit den aktuellen Standortdaten."""
    _write_template()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "schools": SCHOOLS_DATA},
    )


@app.post("/maintain", response_class=HTMLResponse)
async def maintain(request: Request):
    """
    Simuliert eine automatisierte Nachtwartung (NinjaOne / UniFi Mock):
    Alle Standorte im Status 'Warning' werden auf 'Online' gesetzt und
    die Firmware als aktualisiert markiert.
    """
    for school in SCHOOLS_DATA:
        if school["status"] == "Warning":
            school["status"] = "Online"
            school["fw_version"] = "OPNsense 24.1 (Updated)"
    _write_template()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "schools": SCHOOLS_DATA},
    )


@app.post("/sync-xurrent", response_class=HTMLResponse)
async def sync_xurrent(request: Request):
    """
    Simuliert die Synchronisierung offener Vorfälle mit Xurrent (ITSM):
    Für jeden kritischen Standort wird ein Ticket-Payload-Log ausgegeben.
    """
    for school in SCHOOLS_DATA:
        if school["status"] == "Critical":
            print(
                f"[XURRENT-SYNC] Ticket-Payload erstellt für '{school['name']}' "
                f"(ID {school['id']}) -> Quelle: UniFi Controller | "
                f"Priorität: HIGH | Status: open"
            )
    _write_template()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "schools": SCHOOLS_DATA},
    )
