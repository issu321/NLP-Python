# 🔍 Fake News Detection Using Natural Language Processing

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Author](https://img.shields.io/badge/Author-Ussu-orange.svg)](https://github.com/issu321)
[![Repo](https://img.shields.io/badge/Repo-NLP--Python-purple.svg)](https://github.com/issu321/NLP-Python)

> An **advanced** NLP-based system that classifies news articles as **Fake** or **Genuine** using multiple machine learning techniques. Built with Python 3.10+, featuring TF-IDF vectorization, deep sentiment analysis, ensemble voting, and a professional terminal UI.

---

## 🌟 Key Features

| Feature | Description |
|---------|-------------|
| ✅ **Advanced Text Preprocessing** | URL removal, punctuation stripping, lowercasing, whitespace normalization |
| ✅ **TF-IDF Vectorization** | N-gram range (1-3), 8000 max features, sublinear TF scaling |
| ✅ **Sentiment Analysis** | Polarity, subjectivity, word count, sentence count via TextBlob |
| ✅ **4 ML Models** | Logistic Regression, Random Forest, SVM (RBF), Multinomial Naive Bayes |
| ✅ **Ensemble Consensus** | Majority voting across all models for robust predictions |
| ✅ **Rich Metrics** | Accuracy, Precision, Recall, F1-Score, ROC-AUC, Confusion Matrix |
| ✅ **Model Persistence** | Save & load trained model bundles with Pickle |
| ✅ **Batch Processing** | Analyze entire CSV datasets in one run |
| ✅ **Attractive Terminal UI** | Box-drawing tables, color-coded output, progress bars, typing effects |
| ✅ **Python 3.10+ Match-Case** | Clean switch-case menu navigation |

---

## 🚀 Quick Start

### Windows
```batch
install.bat
python app.py
```

### Linux / macOS
```bash
chmod +x install.sh
./install.sh
python3 app.py
```

### Manual Installation
```bash
pip install pandas numpy scikit-learn textblob nltk
python app.py
```

---

## 📊 Usage

### Interactive Mode (Option 1)
Paste any news article into the terminal. The system will:
1. Preprocess & clean the text
2. Run sentiment analysis
3. Apply TF-IDF vectorization
4. Predict using 4 ML models + ensemble consensus

### Batch Mode (Option 4)
Load a CSV file with a `text` column. The system classifies every row automatically.

### Custom Dataset (CLI)
```bash
python app.py dataset.csv
```

**Expected CSV Format:**
| text | label |
|------|-------|
| Article content here... | 0 (Real) or 1 (Fake) |

> If no dataset is provided, a high-quality synthetic demo dataset is auto-generated for immediate testing.

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.10+ (match-case syntax) |
| ML Models | scikit-learn (LR, RF, SVM, NB) |
| Vectorization | scikit-learn TfidfVectorizer (1-3 grams) |
| Sentiment | TextBlob + NLTK |
| Data | pandas, numpy |
| Persistence | pickle |
| UI | ANSI escape codes, box-drawing chars |

---

## 📁 Project Structure

```
.
├── app.py          # Single-file application (all logic + UI)
├── install.bat     # Windows dependency installer
├── install.sh      # Linux/macOS dependency installer
├── inputguide.md   # Detailed input/output format guide
└── README.md       # Project documentation
```

---

## 👤 Author

**Ussu**
- 🌐 GitHub Profile: [@issu321](https://github.com/issu321)
- 📁 Repository: [NLP-Python](https://github.com/issu321/NLP-Python)

---

## 📄 License

MIT License — free to use, modify, and distribute.
