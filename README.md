# OCR Tool (Python)

## Beschreibung
Das war mein erstes Projekt, das ich später bereinigt, strukturiert und auf GitHub hochgeladen habe.

Das Tool dient dazu, Text aus einem frei wählbaren Bildschirmbereich per OCR zu erkennen, Veränderungen zwischen aufeinanderfolgenden OCR-Ergebnissen zu vergleichen und definierte Schlüsselwörter automatisch mitzuzählen.

---

## Funktionen
- Auswahl eines beliebigen Bildschirmbereichs per manueller Kalibrierung
- Screenshot-Erfassung auch bei Multi-Monitor-Setups (inkl. negativer Koordinaten)
- Texterkennung mit Tesseract OCR über `pytesseract`
- Vergleich aufeinanderfolgender OCR-Ergebnisse mit `difflib.SequenceMatcher`
- Erkennung und Zählung definierter Schlüsselwörter
- Speicherung von Debug-Screenshots und OCR-Ausgaben in Dateien

---

## Verwendete Technologien
- Python
- pytesseract
- pyautogui
- Pillow
- mss
- difflib
- re

---

## Projektstruktur
```
ocr-tool/
├── README.md
├── requirements.txt
├── .gitignore
├── main.py
├── config.py
├── config_local.py        # optional, nicht im Repository
├── screenshots/
└── output/
```

---

## Voraussetzungen
Damit das Projekt funktioniert, muss **Tesseract OCR** installiert sein.

Download für Windows:
https://github.com/UB-Mannheim/tesseract/wiki

Falls Tesseract nicht im System-PATH verfügbar ist, kann der Pfad manuell gesetzt werden.

---

## Installation
Repository klonen oder herunterladen und dann:

```
pip install -r requirements.txt
```

---

## Konfiguration

Die Hauptkonfiguration erfolgt in `config.py`:

```
TESSERACT_PATH = None
TARGET_WORDS = {"ok", "okay", "genau"}
DELAY = 0.75
```

### Lokale Konfiguration (`config_local.py`)
Optional kann eine Datei `config_local.py` erstellt werden.

Diese ist eine 1:1 Kopie von `config.py`, in der eigene Pfade oder persönliche Einstellungen angepasst werden.

`config_local.py` wird nicht ins Repository hochgeladen und hat Vorrang vor `config.py`.

Beispiel:

```
TESSERACT_PATH = r"C:\Pfad\zu\tesseract.exe"
```

---

## Verwendung
Programm starten mit:

```
python main.py
```

### Ablauf
1. Bildschirmbereich auswählen
2. Debug-Screenshot überprüfen
3. OCR-Erkennung startet im Loop
4. Änderungen im Text werden erkannt
5. Schlüsselwörter werden gezählt und gespeichert

Beenden mit:
STRG + C

---

## Ausgabedateien

- screenshots/ocr_debug.png  
  Debug-Bild der ausgewählten Region  

- screenshots/ocr.png  
  Aktueller Screenshot während der Laufzeit  

- output/output.txt  
  Fortlaufende Ausgabe erkannter Änderungen  

- output/output_latest.txt  
  Finale Ausgabe beim Beenden des Programms  

---

## Multi-Monitor-Hinweis
Für Screenshots wird `mss` verwendet, da diese Bibliothek stabil mit mehreren Monitoren und negativen Bildschirmkoordinaten arbeitet.

---

## Test-Hinweis
Das Tool wurde unter anderem mit Windows-Untertiteln getestet.

Für bessere OCR-Ergebnisse wird empfohlen:
- klare Schrift
- ausreichend Kontrast
- möglichst undurchsichtiger Hintergrund

Transparente oder halbtransparente Hintergründe können die Erkennung deutlich verschlechtern.

---

## Projektstatus
Ein einfaches Lernprojekt mit Fokus auf:
- praktische Nutzung von OCR
- Textverarbeitung
- grundlegende Automatisierung

---

## Hinweis
Dieses Projekt implementiert keinen eigenen OCR-Algorithmus.
Es nutzt bestehende Bibliotheken und konzentriert sich auf deren Anwendung und Integration.
