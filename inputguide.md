# 📖 Input & Output Guide — Fake News Detection System v4.0.0

> **Project:** Fake News Detection Using NLP  
> **Author:** Ussu  
> **Repo:** https://github.com/issu321/NLP-Python  
> **Version:** 4.0.0 FINAL

---

## 🚀 Quick Start

```bash
# 1. Install dependencies (one time only)
pip install -r requirements.txt

# 2. Run the application
python app.py
```

---

## 📥 How to Give Input — 3 Methods

### Method 1: Interactive Single Article (Menu Option 1)

**Best for:** Testing one article at a time, quick demos, learning the tool.

#### Step-by-Step:
```
[?] Select (0-9): 1
[?] Paste article: <TYPE OR PASTE YOUR TEXT HERE>
```

#### ✅ Good Input Example:
```
[?] Paste article: BREAKING: Secret government documents leaked proving alien contact since 1950s. Anonymous whistleblower reveals shocking truth that NASA has been hiding evidence for decades. Scientists are stunned by this incredible discovery that changes everything we know about human history.
```

#### ✅ Another Good Input Example:
```
[?] Paste article: Federal Reserve announces quarter-point interest rate hike to combat inflation. The decision follows months of economic analysis and was approved by the board of governors. Financial markets responded with modest growth in treasury bonds.
```

#### ❌ Bad Input Example:
```
[?] Paste article: hi
```
**Why it's bad:** Too short (1 word). The app needs at least 10-15 words to extract meaningful linguistic features.

#### ❌ Another Bad Input:
```
[?] Paste article: 12345 $$$ @@@
```
**Why it's bad:** No meaningful words. Numbers and symbols are stripped during preprocessing.

---

### Method 2: Batch CSV Mode (Menu Option 4)

**Best for:** Analyzing hundreds of articles at once, research, dataset evaluation.

#### Step-by-Step:
```
[?] Select (0-9): 4
[?] CSV path (needs 'text' col): /home/user/articles.csv
```

#### ✅ Correct CSV Format:
Create a file named `articles.csv` with this exact structure:

```csv
text,label
"Federal Reserve announces quarter-point interest rate hike to combat inflation",0
"SHOCKING: Doctors hate this one weird trick that cures everything instantly",1
"Local school district receives state grant for STEM education program expansion",0
"BREAKING: Secret documents prove the moon landing was completely staged in Hollywood",1
"University researchers publish findings on climate change patterns in peer-reviewed journal",0
"URGENT: New world order planning to ban all private property starting next month",1
```

| Column | Required? | What to Put |
|--------|-----------|-------------|
| `text` | ✅ **YES** | The full article text or headline |
| `label` | ❌ Optional | `0` = Real news, `1` = Fake news (for comparison only) |

#### ✅ Auto-Detected Column Names:
If your CSV doesn't have `text`, the app automatically checks for:
- `title` → mapped to `text`
- `content` → mapped to `text`
- `article` → mapped to `text`

#### ❌ Incorrect CSV Format:
```csv
headline,category,author
"News today","politics","John"
```
**Why it's bad:** No `text` column. The app will error with: `Needs 'text' column!`

#### ❌ Another Bad CSV:
```csv
text
"This is a short headline"
```
**Why it's bad:** Only 1 row. The app needs at least 10+ rows to train models properly.

---

### Method 3: Command-Line Argument

**Best for:** Automation, scripts, running from other programs.

```bash
# Pass dataset path directly when launching
python app.py /path/to/your_dataset.csv
```

#### Example:
```bash
python app.py /home/ussuroyal/Documents/news_data.csv
```

The app will:
1. Load your CSV automatically
2. Show dataset statistics
3. Run the full NLP pipeline
4. Train all 4 models
5. Show the main menu

---

## 📤 How to Read the Output — Feature by Feature

When you analyze an article, the app prints an **ARTICLE ANALYSIS REPORT**. Here's how to read every section:

---

### 📰 Original Text
```
📰 Original:
   BREAKING: Secret government documents leaked proving alien contact since 1950s...
```
**What it shows:** The first 300 characters of your input (unchanged).

**Example input → output:**
- **Input:** `BREAKING: Secret documents leaked! Scientists stunned!`
- **Output:** `BREAKING: Secret documents leaked! Scientists stunned!`

---

### 🧹 Cleaned Text
```
🧹 Cleaned:
   breaking secret government documents leaked proving alien contact since s
```
**What it shows:** Lowercase, no URLs, no punctuation, no numbers. This is what the ML models actually read.

**Example input → output:**
- **Input:** `NASA confirms: Alien contact since 1950s!!! (SECRET)`
- **Output:** `nasa confirms alien contact since s secret`

---

### 📊 Linguistic Features

The app extracts 12 features from every article. Here's what each means with examples:

#### 1. Polarity
```
│ Polarity           │ -0.750 😠                                        │
```
| Value | Meaning | Example Input |
|-------|---------|---------------|
| `+1.0` | Very positive | `"Amazing wonderful fantastic success"` |
| `0.0` | Neutral | `"The report was published today"` |
| `-1.0` | Very negative | `"Terrible awful disaster crisis death"` |

**How it's calculated:** Counts positive words (+1) vs negative words (-1), with negation flipping (`not good` = negative).

---

#### 2. Subjectivity
```
│ Subjectivity       │ 0.850 🔥 Subjective                              │
```
| Value | Meaning | Example Input |
|-------|---------|---------------|
| `0.0` | Purely factual | `"The GDP grew by 2.3% in Q3"` |
| `0.5` | Mixed | `"Experts suggest the policy may help"` |
| `1.0` | Highly opinionated | `"This is the worst scandal ever!"` |

**How it's calculated:** Ratio of sentiment-bearing words to total words. Headlines < 15 words get boosted.

---

#### 3. Word Count
```
│ Word Count         │ 24                                               │
```
| Value | Meaning | Example Input |
|-------|---------|---------------|
| `5` | Very short headline | `"BREAKING NEWS!!!"` |
| `50` | Short article | `"Federal Reserve announced... (50 words)"` |
| `500` | Long article | `"In a comprehensive study published... (500 words)"` |

---

#### 4. Sentence Count
```
│ Sentence Count     │ 3                                                │
```
| Value | Meaning | Example Input |
|-------|---------|---------------|
| `1` | Single sentence | `"Breaking: Major announcement today."` |
| `5` | Multiple sentences | `"The study found X. Researchers said Y. Experts agree Z."` |

**How it's calculated:** Counts `.` + `!` + `?` in the text.

---

#### 5. Avg Word Length
```
│ Avg Word Length    │ 5.42                                             │
```
| Value | Meaning | Example Input |
|-------|---------|---------------|
| `3.5` | Short simple words | `"Big bad news hit town"` |
| `6.5` | Complex vocabulary | `"Comprehensive longitudinal epidemiological study"` |

---

#### 6. Exclamation Count
```
│ Exclamation Count  │ 4                                                │
```
| Value | Meaning | Example Input |
|-------|---------|---------------|
| `0` | Calm, professional tone | `"The Federal Reserve announced..."` |
| `3+` | Sensational, emotional | `"SHOCKING!!! UNBELIEVABLE!!! MUST READ!!!"` |

**Fake news indicator:** High exclamation count (>=2) strongly suggests sensationalism.

---

#### 7. Question Count
```
│ Question Count     │ 1                                                │
```
| Value | Meaning | Example Input |
|-------|---------|---------------|
| `0` | Declarative statements | `"The report confirms..."` |
| `2+` | Clickbait style | `"What happens next? You won't believe this?"` |

---

#### 8. Caps Ratio
```
│ Caps Ratio         │ 0.1523 (15%)                                     │
```
| Value | Meaning | Example Input |
|-------|---------|---------------|
| `0.02` (2%) | Normal writing | `"The federal reserve announced..."` |
| `0.20` (20%) | Excessive caps | `"BREAKING: SHOCKING NEWS!!!"` |

**Fake news indicator:** Caps ratio > 15% is a strong fake news signal.

---

#### 9. Quote Count
```
│ Quote Count        │ 2                                                │
```
| Value | Meaning | Example Input |
|-------|---------|---------------|
| `0` | No quotes | `"The study found that..."` |
| `4` | Heavy quoting | `"Dr. Smith said 'this is unprecedented' and 'we are shocked'"` |

---

#### 10. Number Count
```
│ Number Count       │ 3                                                │
```
| Value | Meaning | Example Input |
|-------|---------|---------------|
| `0` | No specific data | `"Many people are affected"` |
| `5` | Data-rich | `"2.3% growth, 500 jobs, $1.2B budget, 3 years, 15 states"` |

**Real news indicator:** Higher number counts suggest factual reporting.

---

#### 11. Sensational Score
```
│ Sensational Score  │ 3 ⚠️ High                                        │
```
| Value | Meaning | Example Input |
|-------|---------|---------------|
| `0` | No sensational words | `"The committee reviewed the proposal"` |
| `1` | Mild sensationalism | `"Breaking news from Washington"` |
| `2+` | **High sensationalism** | `"SHOCKING EXPOSED!!! Secret conspiracy revealed!!!"` |

**Critical fake news indicator:** Score >= 2 means multiple sensational trigger words detected. This is one of the strongest predictors.

**Trigger words detected:** `breaking`, `shocking`, `exposed`, `secret`, `conspiracy`, `miracle`, `cure`, `doctors hate`, `won't believe`, `mind blowing`, `must read`, `share before`, `they don't want`, `what happens next`, `you won't believe`

---

#### 12. Avg Sentence Length
```
│ Avg Sentence Length│ 8.00                                             │
```
| Value | Meaning | Example Input |
|-------|---------|---------------|
| `5` | Short punchy sentences | `"News today. Big changes. Stay tuned."` |
| `20` | Complex academic style | `"The comprehensive longitudinal study examining the correlation between..."` |

---

## 🤖 How to Read Model Predictions

After features, you see:

```
🤖 Predictions:

┌──────────────────────────┬──────────────────────────┬────────────────┐
│          Model           │         Verdict          │   Confidence   │
├──────────────────────────┼──────────────────────────┼────────────────┤
│ Logistic Regression      │ FAKE NEWS ⚠️            │     78.5%      │
│ Random Forest            │ FAKE NEWS ⚠️            │     91.2%      │
│ Support Vector Machine   │ FAKE NEWS ⚠️            │     85.3%      │
│ Gradient Boosting        │ FAKE NEWS ⚠️            │     94.7%      │
└──────────────────────────┴──────────────────────────┴────────────────┘

📊 Ensemble Consensus: FAKE (4 Fake vs 0 Real votes)
```

### Reading the Verdict:

| Verdict | Color | Meaning |
|---------|-------|---------|
| `FAKE NEWS ⚠️` | 🔴 Red | Model predicts this is disinformation |
| `GENUINE NEWS ✅` | 🟢 Green | Model predicts this is authentic |

### Reading Confidence:

| Confidence | Interpretation |
|------------|----------------|
| `> 90%` | Very high confidence — strong prediction |
| `70-90%` | High confidence — reliable prediction |
| `50-70%` | Uncertain — model is guessing |
| `< 50%` | Low confidence — treat with skepticism |

### Reading Ensemble Consensus:

| Result | Meaning | Action |
|--------|---------|--------|
| `FAKE (4 vs 0)` | All 4 models agree fake | **High confidence it's fake** |
| `FAKE (3 vs 1)` | Most say fake | **Likely fake, review details** |
| `GENUINE (1 vs 3)` | Most say real | **Likely genuine** |
| `GENUINE (0 vs 4)` | All 4 models agree real | **High confidence it's real** |

---

## 🎛️ Full Menu Walkthrough with Examples

### Option 1 — Interactive Analysis
```
[?] Select (0-9): 1
[?] Paste article: BREAKING: Secret documents prove the moon landing was filmed in Hollywood!

📰 Original:
   BREAKING: Secret documents prove the moon landing was filmed in Hollywood!
🧹 Cleaned:
   breaking secret documents prove the moon landing was filmed in hollywood
📊 Linguistic Features:
   ...
🤖 Predictions:
   Logistic Regression → FAKE NEWS ⚠️ (82.3%)
   Random Forest       → FAKE NEWS ⚠️ (91.5%)
   SVM                 → FAKE NEWS ⚠️ (78.9%)
   Gradient Boosting   → FAKE NEWS ⚠️ (95.1%)
📊 Ensemble Consensus: FAKE (4 Fake vs 0 Real votes)
```

### Option 2 — Model Comparison
```
[?] Select (0-9): 2

┌──────────────────────┬──────────┬────────┬─────────┬───────────┬────────┬──────┐
│        Model         │ Test Acc │ CV Acc │ ROC-AUC │ Precision │ Recall │  F1  │
├──────────────────────┼──────────┼────────┼─────────┼───────────┼────────┼──────┤
│ Logistic Regression  │  85.0%   │ 82.3%  │  0.912  │   0.889   │ 0.842  │0.864 │
│ Random Forest        │  90.0%   │ 87.1%  │  0.945  │   0.923   │ 0.889  │0.905 │
│ Support Vector Mach..│  80.0%   │ 78.5%  │  0.891  │   0.857   │ 0.800  │0.827 │
│ Gradient Boosting    │  92.5%   │ 89.4%  │  0.967  │   0.941   │ 0.913  │0.927 │
└──────────────────────┴──────────┴────────┴─────────┴───────────┴────────┴──────┘
🏆 BEST: Gradient Boosting (Test=92.5%, CV=89.4%)
```

### Option 4 — Batch CSV
```
[?] Select (0-9): 4
[?] CSV path (needs 'text' col): /home/user/news_1000.csv
[*] Processing 1,000 articles...

─── 1/1000 ───
[full analysis for article 1]
─── 2/1000 ───
[full analysis for article 2]
...
```

### Option 6 — Retrain with Custom Data
```
[?] Select (0-9): 6
[?] Dataset path (Enter=demo): /home/user/large_dataset.csv
[✓] Loaded 10,000 records
[📊 stats table]
[*] Running NLP Feature Pipeline...
[*] Text Cleaning          ████████████████████████████████████████ 100.0%
[✓] Pipeline done: 8,000 train │ 2,000 test
[🧠 training phase]
[✓] Logistic Regression    Acc: 94.2% CV: 92.1% ████████████████████ (2.34s)
[✓] Random Forest          Acc: 96.8% CV: 95.3% ████████████████████ (8.91s)
[✓] Support Vector Machine Acc: 93.5% CV: 91.8% ███████████████████░ (4.12s)
[✓] Gradient Boosting      Acc: 97.1% CV: 96.0% ████████████████████ (12.45s)
[?] Save models? (y/n): y
[✓] Saved to saved_models/models_20260521_062430.pkl
[✓] Retrain complete!
```

### Option 7 — Save Models
```
[?] Select (0-9): 7
[✓] Saved to saved_models/models_20260521_062430.pkl
```

### Option 8 — Load Models
```
[?] Select (0-9): 8
[*] Saved models:
   1. models_20260521_062430.pkl
   2. models_20260521_061930.pkl
[?] Select (1-2): 1
[✓] Loaded models_20260521_062430.pkl
```

---

## 💡 Real-World Usage Examples

### Example 1: Checking a WhatsApp Forward
```
[?] Paste article: URGENT ALERT!!! New WhatsApp policy allows them to read all your messages and share with government!!! Share this with 10 friends before midnight!!!

📊 Linguistic Features:
   Exclamation Count: 4
   Caps Ratio: 0.18 (18%)
   Sensational Score: 3 ⚠️ High
   Subjectivity: 0.92 🔥 Subjective

🤖 Predictions:
   All 4 models → FAKE NEWS ⚠️
📊 Ensemble Consensus: FAKE (4 vs 0)
```
**Verdict:** Clearly fake — high sensationalism, excessive caps, multiple exclamations.

### Example 2: Checking a News Article
```
[?] Paste article: The Federal Reserve raised interest rates by 0.25 percentage points on Wednesday, the tenth consecutive increase as policymakers continue their campaign to cool inflation. The decision brings the federal funds rate to a range of 5% to 5.25%.

📊 Linguistic Features:
   Polarity: 0.05 😐
   Subjectivity: 0.12 📘 Objective
   Caps Ratio: 0.02 (2%)
   Sensational Score: 0 ✓ Low
   Number Count: 5

🤖 Predictions:
   All 4 models → GENUINE NEWS ✅
📊 Ensemble Consensus: GENUINE (0 vs 4)
```
**Verdict:** Clearly genuine — objective tone, data-rich, no sensational words, low caps.

---

## 🛠️ Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `[!] Empty input.` | You pressed Enter without typing | Type actual article text |
| `Needs 'text' column!` | CSV missing the text column | Rename column to `text` or use `title`/`content`/`article` |
| `File not found!` | Wrong file path | Check path with `ls /your/path/` |
| Low accuracy on demo | Only 48 synthetic samples | Use Option 6 with a real dataset (5,000+ rows) |
| Garbled boxes / no colors | Terminal doesn't support Unicode | Use Windows Terminal, iTerm2, or GNOME Terminal |
| `Python version error` | Using Python < 3.10 | Upgrade to Python 3.10+ for match-case support |

---

## 📦 Tech Stack

| Component | Library | Purpose |
|-----------|---------|---------|
| Language | Python 3.10+ | match-case menu navigation |
| ML Models | scikit-learn | LogisticRegression, RandomForest, SVC, GradientBoosting |
| Vectorization | scikit-learn TfidfVectorizer | Convert text to numbers (1-2 grams, 5000 features) |
| Scaling | scikit-learn MinMaxScaler | Normalize all features to [0,1] range |
| Sentiment | Built-in lexicon | 100+ words, negation + intensifier handling |
| Data | pandas, numpy | CSV loading, array operations |
| Persistence | pickle | Save/load model bundles |
| UI | ANSI + Unicode | Colors, box-drawing tables, progress bars |

---

**Author:** Ussu  
**Profile:** https://github.com/issu321  
**Repository:** https://github.com/issu321/NLP-Python
