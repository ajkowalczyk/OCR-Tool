import os

# --- OCR configuration ---
# TESSERACT_PATH = r"C:\Pfad\zu\tesseract.exe"
TESSERACT_PATH = None
# --- Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
# --- Files ---
DEBUG_IMAGE_PATH = os.path.join(SCREENSHOTS_DIR, "ocr_debug.png")
SCREENSHOT_PATH = os.path.join(SCREENSHOTS_DIR, "ocr.png")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "output.txt")
END_OUTPUT_PATH = os.path.join(OUTPUT_DIR, "output_latest.txt")
# --- FOLDER CHECK-UP ---
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
# --- Detection settings ---
TARGET_WORDS = {"ok", "okay", "genau"}  # Schlüsselwörter
DELAY = 0.75  # Zeitverzögerung zwischen den Durchläufen (Sekunden)