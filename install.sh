#!/bin/bash
# ═══════════════════════════════════════════════════════════════
#  🤖 FAKE NEWS DETECTION NLP — LINUX / macOS INSTALLER
#  Author: Ussu
#  https://github.com/issu321/NLP-Python
# ═══════════════════════════════════════════════════════════════

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  🤖 FAKE NEWS DETECTION NLP — LINUX / macOS INSTALLER       ║"
echo "║  Author: Ussu                                                ║"
echo "║  https://github.com/issu321/NLP-Python                       ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "[*] Checking Python version..."
echo "Python is Mandatory for this project. Please ensure you have Python 3.10 or higher installed."

PY_MINOR=$(python3 -c "import sys; print(sys.version_info.minor)")
if [ "$PY_MINOR" -lt 10 ]; then
    echo "[X] Python 3.10+ is required for match-case support!"
    exit 1
fi

echo "[OK] Python version compatible."
echo ""
echo "[*] Installing Python dependencies..."
pip3 install --upgrade pip
pip3 install pandas numpy scikit-learn textblob nltk

echo ""
echo "[*] Downloading NLTK datasets..."
python3 -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True)"

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  [OK] INSTALLATION COMPLETE!                                 ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║  Run the app:  python3 app.py                              ║"
echo "║  With dataset: python3 app.py dataset.csv                    ║"
echo "╚══════════════════════════════════════════════════════════════╝"
