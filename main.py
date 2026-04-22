import pyautogui
import pytesseract
import time
import difflib
import mss
from PIL import Image
import re
import sys
# Lokale Konfiguration hat Vorrang (nicht im Repo)
try:
    from config_local import TESSERACT_PATH, DEBUG_IMAGE_PATH, SCREENSHOT_PATH, OUTPUT_PATH, END_OUTPUT_PATH, TARGET_WORDS, DELAY
except ImportError:
    from config import TESSERACT_PATH, DEBUG_IMAGE_PATH, SCREENSHOT_PATH, OUTPUT_PATH, END_OUTPUT_PATH, TARGET_WORDS, DELAY


# # Falls Tesseract nicht im PATH ist, kann der Pfad in config.py gesetzt werden
# https://github.com/UB-Mannheim/tesseract/wiki
try:
    if TESSERACT_PATH:
        pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

    # Tesseract Test
    pytesseract.get_tesseract_version()

except Exception:
    print("Tesseract nicht gefunden. Bitte PATH prüfen oder TESSERACT_PATH in config.py setzen.")
    sys.exit(1)

# Work-around für Mehrere Bildschirmen und Minus Koordinaten :D
def take_screenshot(region):
    with mss.mss() as sct:
        monitor = {
            "left": region[0],
            "top": region[1],
            "width": region[2],
            "height": region[3],
        }
        img = sct.grab(monitor)
        return Image.frombytes("RGB", img.size, img.rgb)

def set_region():
    while True:
        print("\n--- OCR Region Aufnahme! ---")
        print("1. Zeiger auf die obere linke Ecke der Aufnahme setzen!")
        input("- Aufnahme mit [Enter] bestätigen...")
        time.sleep(0.3)
        x1, y1 = pyautogui.position()
        print(f"(X1, Y1): ({x1}, {y1})")
        print("2. Zeiger auf die untere rechte Ecke der Aufnahme setzen!")
        input("- Aufnahme mit [Enter] bestätigen...")
        time.sleep(0.3)
        x2, y2 = pyautogui.position()
        print(f"(X2, Y2): ({x2}, {y2})")
        left = min(x1, x2)      # Check if it was truly left -> right, if not then adapt
        top = min(y1, y2)       # Check if it was truly top -> bottom, if not then adapt
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        region = (left, top, width, height)
        # region = (x1, y1, x2 - x1, y2 - y1)   # exactly same, but without changing of directions :)
        screenshot = take_screenshot(region)    # Debug screenshot erstellt
        screenshot.save(DEBUG_IMAGE_PATH)    # Debug screenshot gespeichert
        print(f"Region: {region}\n- Debug screenshot gespeichert unter: {DEBUG_IMAGE_PATH} Bitte überprüfen!-")
        # --- Bestätigung ---
        confirm = input("Ist die Region korrekt? (y/n): ").strip().lower()
        if confirm in ("y", "yes", "j", "ja", "jup"):
            return region
        else:
            print("Region wird erneut aufgenommen...\n")


# DIFFLIB SequenceMatcher - ChatGPT halb-geklauter Code :)
def compare_ocr_texts(text1, text2, counters):
    words1 = text1.split()
    words2 = text2.split()
    new_words = []
    if text1 == text2: return " ".join(new_words), counters
    sm = difflib.SequenceMatcher(None, words1, words2)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ('replace', 'insert'):
            for w in words2[j1:j2]:
                new_words.append(w)
                word_clean = re.sub(r"[^\w]", "", w.lower())
                if word_clean in TARGET_WORDS:
                    counters[word_clean] += 1
                    print(f"Got Keyword! : {w}, derzeit: {counters[word_clean]}")
    return " ".join(new_words), counters


if __name__ == '__main__':
    counters = {w: 0 for w in TARGET_WORDS}   # Auto-Init für jeden Key im Dictionary
    oldtext = ""
    wholetext = ""  
    region = set_region()    # Region :)
    # Endless Loop :) STRG+C to kill in VSCode
    try:
        print("------- START -------")
        while True:
            screenshot = take_screenshot(region)                              # region = (x, y, width, height) :)
            screenshot.save(SCREENSHOT_PATH)                                                # OCR.png ist aktuellste SS, muss nicht gespeichert werden, aber sieht cool aus
            text = pytesseract.image_to_string(screenshot, lang="deu", config='--psm 6')    #psm 6 für Textblock, psm 7 Singleline-Text
            difference, counters = compare_ocr_texts(oldtext, text, counters) 
            if oldtext != text: 
                wholetext += "\n" + difference
                oldtext = text
                with open(OUTPUT_PATH, "a", encoding = "utf-8") as ausgabe:
                    ausgabe.write("\n" + difference)        ## Mehr von DEBUG als richtiger Nutzung!
            # Effizient ist es nicht! ...aber falls fehlgeschlagen in der Mitte - das gesamte Text speichert sich in OCRoutput.txt! :)
            # ACHTUNG! DAS .TXT WIRD NUR GRÖßER!
            # TODO Verlauf und umsetzen von alten Dateien / Erstellen von neue Dateien mit Start-Uhrzeit 
            print("--- STRG+C um es zu beenden! ---")   # Ich weiß, dass es vielleicht bessere Möglichkeiten gibt's, aber dieser Lösung fördert kein UI und lässt in Ruhe Arbeiten an andere Sachen in der Zeit als es läuft.
            time.sleep(DELAY)

    except KeyboardInterrupt:
        print(f"Anzahl von Schlüsselwörter:\n {counters}")
        with open(END_OUTPUT_PATH, "w", encoding = "utf-8") as ausgabe:
            ausgabe.write(wholetext)        ## auf der Ende TEXT AUSGABE IN EINEM .TXT :)
