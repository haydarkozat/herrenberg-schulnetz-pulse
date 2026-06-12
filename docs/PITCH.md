# 🎤 Demo Cheat-Sheet — Herrenberg SchulNetz-Pulse

> Spickzettel für das Bewerbungsgespräch (IT-Systemadministrator, Stadt Herrenberg).
> Vor dem Termin einmal durchlesen. Ziel: **Problem → Lösung → mein Mehrwert.**

---

## ⏱️ 0. Vorbereitung (vor dem Gespräch)

```bash
# Image vorab ziehen, damit die Demo auch ohne gutes WLAN läuft:
docker pull ghcr.io/haydarkozat/herrenberg-schulnetz-pulse:latest

# Starten:
docker run -p 8000:8000 ghcr.io/haydarkozat/herrenberg-schulnetz-pulse:latest
# Browser:  http://127.0.0.1:8000
```
Backup: lokales Image bereithalten, Browser-Tab schon offen, README + Actions-Tab als zweiter Tab.

---

## 🗣️ 1. Eröffnung (30 Sek.)

> „14 Schulstandorte einzeln manuell zu überwachen kostet Zeit und ein Ausfall kann übersehen werden.
> Ich habe ein Konzept gebaut: **SchulNetz-Pulse** — ein zentrales Panel, das den Zustand aller
> Schulnetze auf einen Blick zeigt und Routineaufgaben per Klick automatisiert. Voll lauffähig,
> startet mit Docker in Minuten."

→ Botschaft: *Ich verstehe das Problem + ich kann es lösen + ich bringe es zu Ende.*

---

## 🖥️ 2. Live-Demo (der stärkste Teil)

| Schritt | Was zeigen | Was sagen |
|--------|------------|-----------|
| 1 | Dashboard öffnen | „14 Standorte, farbcodiert: grün = online, gelb = Warnung, rot = kritisch." |
| 2 | Auf den **kritischen** Standort zeigen (Längenholz-Grundschule) | „UniFi Controller bekommt keine Heartbeats. Das System hat automatisch einen **Xurrent Ticket-Payload** vorbereitet." |
| 3 | Button **„Automatisierte Nachtwartung starten"** klicken | „Ein Klick → alle Warnungen auf Online, Firmware aktualisiert. Simulation der Nacht-Automation (**NinjaOne / UniFi API Mock**)." |
| 4 | Button **„Xurrent synchronisieren"** + Konsole/Logs | „Kritische Vorfälle werden automatisch ans ITSM (Xurrent) übergeben." |

---

## 🔧 3. Technik (DevOps-Kompetenz zeigen)

- **Production-ready verpackt** → Dockerfile, schlankes `python:3.10-slim`, Layer-Caching
- **CI/CD** → GitHub Actions testet jeden Commit automatisch (Lint + Docker-Build + 3 Endpoint-Smoke-Tests) → grünes Badge zeigen
- **Release-Automation** → bei jedem Git-Tag wird ein **Multi-Arch-Image (amd64 + arm64)** nach `ghcr.io` veröffentlicht
- **Stack:** FastAPI + Python, REST-Endpunkte, container-native

---

## 🎯 4. Bezug zur Stelle (am wichtigsten!)

Die Werkzeugnamen sind **bewusst** gewählt — reale Systeme der Schul-IT:

| Tool | Rolle |
|------|-------|
| **OPNsense** | Firewall |
| **UniFi** | WLAN / Access Points |
| **NinjaOne** | RMM / Endpoint-Management |
| **Xurrent** | ITSM / Ticketing |

> „Das sind Systeme, denen ich im Schulnetz-Betrieb begegne. Die Demo ist ein Mock, aber die
> Architektur ist so gebaut, dass sie an echte APIs andocken kann — also kein Spielzeug, sondern
> das **Gerüst einer echten Integration**."

---

## 🧭 5. Ehrliche Grenze + Vision (zeigt Reife)

> „Aktuell sind die Daten simuliert. Nächste Schritte produktiv: Live-Anbindung an UniFi/NinjaOne-APIs,
> eine Datenbank, Authentifizierung und Alarm-Benachrichtigungen."

---

## ❓ Erwartbare Fragen — Kurzantworten

- **Warum FastAPI?** → schnell, async, automatische API-Doku, leichtgewichtig.
- **Warum Docker?** → beseitigt „läuft nur bei mir", überall identisch reproduzierbar.
- **Sicherheit?** → In der Demo bewusst weggelassen; produktiv: Reverse-Proxy + HTTPS + Auth + Secrets-Management.
- **Skalierung?** → zustandslose Container hinter einem Load-Balancer, horizontal skalierbar.

---

## 🏁 Schlusssatz

> „Kurz gesagt: Ich habe mir noch vor dem ersten Arbeitstag überlegt, wie ich dem Team konkret
> helfen kann — und es lauffähig umgesetzt."

---

🔗 **Repo:** https://github.com/haydarkozat/herrenberg-schulnetz-pulse
🐳 **Image:** `ghcr.io/haydarkozat/herrenberg-schulnetz-pulse:latest`
