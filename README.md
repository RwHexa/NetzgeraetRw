# NetzgeraetRw — 12‑V‑Sperrwandler verstehen, prüfen & simulieren

![Projektkarte](projektkarte.png)

Dokumentation eines isolierten **Sperrwandler‑Netzteils** (12 V, ~10–15 W) mit dem PWM‑Controller **OB2263**, Optokoppler **PC817** und **TL431** — aufbereitet als Lehr‑/Werkstattbericht in drei Schritten: **Verstehen → Prüfen → Simulieren**.

## 📚 Inhalt

| Teil | Datei | Inhalt |
|---|---|---|
| 🗂️ Start | [NetzgeraetUebersichtKi.md](NetzgeraetUebersichtKi.md) | Gesamtübersicht mit Inhaltsverzeichnis & Lernpfad |
| 📘 Verstehen | [NetzgeraetKi.md](NetzgeraetKi.md) | Funktionsanalyse (Regelung, Trafo, Bauteile) |
| 🔧 Prüfen | [NetzgeraetMessKi.md](NetzgeraetMessKi.md) | Störungs‑ & Fehleranalyse (sichere Messungen) |
| 🖥️ Simulieren | [NetzgeraetFalstadKi.md](NetzgeraetFalstadKi.md) | Aufbau im Falstad‑Browser |
| 🎛️ Interaktiv | [NetzgeraetSimulation.html](NetzgeraetSimulation.html) | Offline‑Simulation des Regelverhaltens |
| 📄 Heft | `NetzgeraetHeft.pdf` | Alles gebündelt als gestaltetes PDF‑Heft |

## 🎛️ Interaktive Simulation

`NetzgeraetSimulation.html` einfach im Browser öffnen (läuft offline, keine Installation). Schieberegler für **Netzspannung** und **Laststrom**, Knöpfe für **Lastsprung** und **Regelung öffnen** — zeigt live, wie der Regelkreis die 12 V hält und was bei offener Rückkopplung passiert.

## 🖼️ Diagramme

Alle selbst erstellten Diagramme liegen als `.svg` (Quelle) **und** `.png` (2×) vor:
`regelschleife` · `trafo_zwei_phasen` · `messablauf` · `vergleich_schaltplaene` · `projektkarte`.

## ⚖️ Rechte & Quellen

- **Eigene Inhalte** (Texte, selbst erstellte Diagramme, HTML‑Simulation, Heft, Logo): © Reinhard Wermeling (RwTec), erarbeitet mit Claude Code.
- ⚠️ **Fremde Bilder** (nur zu Lern‑/Referenzzwecken): einige Bitmap‑Schaltbilder und Fotos stammen aus dem Web und unterliegen fremdem Urheberrecht — u. a. `Schaltplan_vollstaendig.jpg` (Wasserzeichen ornatepixels.com), `Schaltplan.jpg` / `SchaltplanKl.JPG`, `PlatineKl.JPG`. **Nicht für Weiterverbreitung.** Vor einer etwaigen Veröffentlichung entfernen oder durch eigene Nachzeichnungen ersetzen.

---

*Werkstattbericht · RwTec · 2026 · erstellt mit Claude Code*
