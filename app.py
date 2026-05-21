#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║   🤖  FAKE NEWS DETECTION USING NATURAL LANGUAGE PROCESSING                     ║
║   🔒  ADVANCED NLP CYBER-SECURITY TOOLKIT — REAL-WORLD READY                     ║
║                                                                                  ║
║   👤  Author  : Ussu                                                             ║
║   🌐  GitHub  : https://github.com/issu321                                       ║
║   📁  Repo    : https://github.com/issu321/NLP-Python                            ║
║   📅  Version : 5.0.0 VISUAL ENHANCED                                            ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
"""

import sys
import os
import re
import string
import time
import warnings
import pickle
from typing import Optional, Dict, List, Tuple
from datetime import datetime
from collections import Counter

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix, roc_auc_score,
    precision_score, recall_score, f1_score, roc_curve
)

# ═══════════════════════════════════════════════════════════════════════════════
#   OPTIONAL VISUALIZATION ENGINE
# ═══════════════════════════════════════════════════════════════════════════════
try:
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend for compatibility
    import matplotlib.pyplot as plt
    import seaborn as sns
    VISUALS_AVAILABLE = True
except ImportError:
    VISUALS_AVAILABLE = False
    plt = None
    sns = None

# ═══════════════════════════════════════════════════════════════════════════════
#   BUILT-IN SENTIMENT & LINGUISTIC FEATURE EXTRACTOR (Zero external deps)
# ═══════════════════════════════════════════════════════════════════════════════
class LinguisticAnalyzer:
    """
    Extracts sentiment, style, and structural features from text.
    Completely self-contained — no downloads, no internet.
    """
    POSITIVE_WORDS = {
        'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'best',
        'love', 'happy', 'positive', 'success', 'win', 'victory', 'boost', 'growth',
        'improve', 'benefit', 'effective', 'strong', 'secure', 'safe', 'trust',
        'honest', 'true', 'real', 'genuine', 'verified', 'confirmed', 'approved',
        'support', 'help', 'care', 'progress', 'advance', 'achieve', 'celebrate',
        'proud', 'honor', 'respect', 'peace', 'stable', 'prosper', 'thrive',
        'recommend', 'praise', 'commend', 'outstanding', 'remarkable', 'superb',
        'breakthrough', 'innovation', 'solution', 'recovery', 'optimistic'
    }
    NEGATIVE_WORDS = {
        'bad', 'terrible', 'awful', 'horrible', 'worst', 'hate', 'angry', 'sad',
        'negative', 'fail', 'loss', 'defeat', 'crisis', 'disaster', 'tragedy',
        'danger', 'threat', 'risk', 'fear', 'panic', 'worry', 'concern', 'alarm',
        'shocking', 'exposed', 'scandal', 'corrupt', 'fraud', 'lie', 'fake',
        'hoax', 'conspiracy', 'secret', 'hidden', 'cover', 'ban', 'destroy',
        'attack', 'kill', 'death', 'violence', 'war', 'conflict', 'enemy',
        'blame', 'accuse', 'guilty', 'shame', 'disgrace', 'outrage', 'furious',
        'shocking', 'urgent', 'warning', 'alert', 'beware', 'devastating'
    }
    INTENSIFIERS = {
        'very', 'extremely', 'incredibly', 'absolutely', 'totally', 'completely',
        'utterly', 'highly', 'deeply', 'strongly', 'seriously', 'severely',
        'especially', 'particularly', 'remarkably', 'exceptionally', 'most'
    }
    NEGATORS = {
        'not', 'no', 'never', 'none', 'nobody', 'nothing', 'neither', 'nowhere',
        'hardly', 'scarcely', 'barely', 'dont', 'doesnt', 'didnt', 'wasnt',
        'werent', 'hasnt', 'havent', 'hadnt', 'cant', 'couldnt', 'wont',
        'wouldnt', 'shouldnt', 'isnt', 'arent', 'aint'
    }
    SENSATIONAL_WORDS = {
        'shocking', 'breaking', 'urgent', 'alert', 'exposed', 'revealed',
        'hidden', 'secret', 'conspiracy', 'miracle', 'cure', 'doctors hate',
        'won\'t believe', 'mind blowing', 'must read', 'share before',
        'they don\'t want', 'what happens next', 'you won\'t believe'
    }
    CREDIBILITY_MARKERS = {
        'study', 'research', 'data', 'analysis', 'report', 'official', 'expert',
        'scientist', 'peer-reviewed', 'journal', 'university', 'institute',
        'survey', 'statistics', 'findings', 'evidence', 'documented'
    }
    EMOTIONAL_TRIGGERS = {
        'outraged', 'devastated', 'heartbroken', 'furious', 'terrified',
        'disgusted', 'appalled', 'horrified', 'traumatized', 'enraged'
    }

    def analyze(self, text: str) -> Dict:
        if not text or not isinstance(text, str):
            return self._empty_features()

        words = text.lower().split()
        raw_words = text.split()
        clean_words = [w.strip(string.punctuation) for w in words if w.strip(string.punctuation)]
        if not clean_words:
            return self._empty_features()

        # ── Sentiment Scoring ──
        pos_score = 0
        neg_score = 0
        subj_words = 0
        negation_active = False
        emotional_score = 0
        credibility_score = 0

        for i, word in enumerate(words):
            clean = word.strip(string.punctuation)
            if not clean:
                continue
            if clean in self.NEGATORS:
                negation_active = True
                continue
            mult = 1.5 if (i > 0 and words[i-1].strip(string.punctuation) in self.INTENSIFIERS) else 1.0
            if clean in self.POSITIVE_WORDS:
                score = 1.0 * mult
                pos_score += score if not negation_active else 0
                neg_score += score if negation_active else 0
                subj_words += 1
                negation_active = False
            elif clean in self.NEGATIVE_WORDS:
                score = 1.0 * mult
                neg_score += score if not negation_active else 0
                pos_score += score if negation_active else 0
                subj_words += 1
                negation_active = False
            elif clean in self.EMOTIONAL_TRIGGERS:
                emotional_score += 1
            elif clean in self.CREDIBILITY_MARKERS:
                credibility_score += 1
            elif negation_active and i % 3 == 0:
                negation_active = False

        total = pos_score + neg_score
        polarity = 0.0 if total == 0 else (pos_score - neg_score) / total
        polarity = max(-1.0, min(1.0, polarity))
        subjectivity = min(1.0, subj_words / max(len(clean_words), 1))
        if len(clean_words) < 15:
            subjectivity = min(1.0, subjectivity * 1.3 + 0.1)

        # ── Structural Features ──
        char_count = len(text)
        word_count = len(clean_words)
        sentence_count = max(1, text.count('.') + text.count('!') + text.count('?'))
        avg_word_len = np.mean([len(w) for w in clean_words]) if clean_words else 0
        exclamation_count = text.count('!')
        question_count = text.count('?')
        caps_count = sum(1 for c in text if c.isupper())
        caps_ratio = caps_count / max(char_count, 1)
        quote_count = text.count('"') + text.count("'")
        number_count = len(re.findall(r'\d+', text))
        unique_words = len(set(clean_words))
        lexical_diversity = unique_words / max(word_count, 1)

        # ── Sensationalism & Credibility ──
        sensational_score = sum(1 for w in self.SENSATIONAL_WORDS if w in text.lower())
        all_caps_words = sum(1 for w in raw_words if w.isupper() and len(w) > 1)

        # ── Readability proxy ──
        avg_sentence_len = word_count / sentence_count
        syllable_proxy = sum(max(1, len(re.findall(r'[aeiouAEIOU]', w))) for w in clean_words)

        # ── URL & Source indicators ──
        url_count = len(re.findall(r'http[s]?://|www\.', text))

        return {
            'polarity': round(polarity, 4),
            'subjectivity': round(subjectivity, 4),
            'word_count': word_count,
            'sentence_count': sentence_count,
            'avg_word_length': round(avg_word_len, 2),
            'exclamation_count': exclamation_count,
            'question_count': question_count,
            'caps_ratio': round(caps_ratio, 4),
            'quote_count': quote_count,
            'number_count': number_count,
            'sensational_score': sensational_score,
            'avg_sentence_length': round(avg_sentence_len, 2),
            'lexical_diversity': round(lexical_diversity, 4),
            'emotional_score': emotional_score,
            'credibility_score': credibility_score,
            'all_caps_words': all_caps_words,
            'url_count': url_count,
            'syllable_proxy': syllable_proxy,
        }

    def _empty_features(self) -> Dict:
        return {k: 0 for k in [
            'polarity', 'subjectivity', 'word_count', 'sentence_count',
            'avg_word_length', 'exclamation_count', 'question_count',
            'caps_ratio', 'quote_count', 'number_count',
            'sensational_score', 'avg_sentence_length',
            'lexical_diversity', 'emotional_score', 'credibility_score',
            'all_caps_words', 'url_count', 'syllable_proxy'
        ]}


# ═══════════════════════════════════════════════════════════════════════════════
#   COLOR PALETTE & UI ENGINE
# ═══════════════════════════════════════════════════════════════════════════════
class UI:
    RST = '\033[0m'; BOLD = '\033[1m'; DIM = '\033[2m'
    RED = '\033[31m'; GREEN = '\033[32m'; YELLOW = '\033[33m'
    BLUE = '\033[34m'; MAGENTA = '\033[35m'; CYAN = '\033[36m'
    BRED = '\033[91m'; BGREEN = '\033[92m'; BYELLOW = '\033[93m'
    BBLUE = '\033[94m'; BMAGENTA = '\033[95m'; BCYAN = '\033[96m'
    WHITE = '\033[97m'; BWHITE = '\033[1m\033[97m'
    BG_DARK = '\033[40m'; BG_GREEN = '\033[42m'; BG_RED = '\033[41m'

    @staticmethod
    def header(title: str, width: int = 78) -> str:
        t = f"{UI.BCYAN}╔{'═'*(width-2)}╗{UI.RST}"
        m = f"{UI.BCYAN}║{UI.RST}{UI.BOLD}{UI.WHITE}{title.center(width-2)}{UI.RST}{UI.BCYAN}║{UI.RST}"
        b = f"{UI.BCYAN}╚{'═'*(width-2)}╝{UI.RST}"
        return f"\n{t}\n{m}\n{b}"

    @staticmethod
    def subheader(title: str, width: int = 78) -> str:
        pad = (width - len(title) - 4) // 2
        return f"\n{UI.BCYAN}{'─'*pad} {UI.BOLD}{UI.WHITE} {title} {UI.RST}{UI.BCYAN} {'─'*(width-pad-len(title)-4)}─{UI.RST}"

    @staticmethod
    def sep(width: int = 78) -> str:
        return f"{UI.DIM}{'─'*width}{UI.RST}"

    @staticmethod
    def progress(label: str, cur: int, tot: int, w: int = 40):
        p = cur / tot
        f = int(w * p)
        bar = f"{UI.BGREEN}{'█'*f}{UI.RST}{UI.DIM}{'░'*(w-f)}{UI.RST}"
        print(f"\r{UI.BBLUE}[*]{UI.RST} {label:<25} {bar} {p:>6.1%}", end="")
        if cur == tot:
            print()

    @staticmethod
    def table(headers: List[str], rows: List[List[str]], widths: List[int] = None, width: int = 78):
        if not widths:
            col_count = len(headers)
            base_width = width - (col_count + 1)
            min_widths = [max(len(str(r[i])) for r in [headers]+rows if i < len(r))+4 for i in range(col_count)]
            extra = base_width - sum(min_widths)
            if extra > 0:
                # Distribute extra to columns proportionally
                for i in range(col_count):
                    min_widths[i] += extra // col_count
                min_widths[-1] += extra % col_count
            widths = min_widths

        def line(cells, l="│", m="│", r="│", fill=" "):
            parts = []
            for c, w in zip(cells, widths):
                c_str = str(c)
                pad = w - len(UI._strip_ansi(c_str)) - 2
                if pad < 0:
                    pad = 0
                parts.append(f"{fill}{c_str}{fill*pad}{fill}")
            return f"{UI.BCYAN}{l}{UI.RST}" + f"{UI.BCYAN}{m}{UI.RST}".join(parts) + f"{UI.BCYAN}{r}{UI.RST}"

        def border(l="┌", m="┬", r="┐", c="─"):
            parts = [f"{c*w}" for w in widths]
            return f"{UI.BCYAN}{l}{UI.RST}" + f"{UI.BCYAN}{m}{UI.RST}".join(parts) + f"{UI.BCYAN}{r}{UI.RST}"

        print(border())
        print(line([f"{UI.BOLD}{h}{UI.RST}" for h in headers]))
        print(border("├","┼","┤","─"))
        for row in rows:
            print(line(row))
        print(border("└","┴","┘","─"))

    @staticmethod
    def _strip_ansi(text: str) -> str:
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)

    @staticmethod
    def banner(text: str, color: str = BCYAN, width: int = 78):
        pad = (width - len(text) - 4) // 2
        print(f"\n{color}{'▓'*pad} {UI.BOLD}{text}{UI.RST}{color} {'▓'*(width-pad-len(text)-4)}▓{UI.RST}")

    @staticmethod
    def metric(label: str, value: str, status: str = "neutral", width: int = 36):
        colors = {"good": UI.BGREEN, "bad": UI.BRED, "warn": UI.BYELLOW, "info": UI.BBLUE, "neutral": UI.WHITE}
        c = colors.get(status, UI.WHITE)
        print(f"  {UI.DIM}├─{UI.RST} {label:<20} {c}{UI.BOLD}{value}{UI.RST}")


# ═══════════════════════════════════════════════════════════════════════════════
#   VISUALIZATION ENGINE
# ═══════════════════════════════════════════════════════════════════════════════
class Visualizer:
    """Generates publication-quality charts for all model outputs."""

    def __init__(self, output_dir: str = "charts"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        if VISUALS_AVAILABLE:
            sns.set_style("whitegrid")
            plt.rcParams['figure.dpi'] = 150
            plt.rcParams['savefig.dpi'] = 150
            plt.rcParams['font.size'] = 9
            plt.rcParams['axes.titlesize'] = 11
            plt.rcParams['axes.labelsize'] = 9

    def _save(self, name: str):
        if not VISUALS_AVAILABLE:
            return None
        path = os.path.join(self.output_dir, f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        plt.tight_layout()
        plt.savefig(path, bbox_inches='tight', facecolor='white', edgecolor='none')
        plt.close()
        return path

    def dataset_stats(self, df: pd.DataFrame):
        """Pie chart + bar chart for dataset distribution."""
        if not VISUALS_AVAILABLE:
            return None
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        # Pie chart
        labels = ['Real News', 'Fake News']
        sizes = [(df['label']==0).sum(), (df['label']==1).sum()]
        colors = ['#10b981', '#ef4444']
        explode = (0.02, 0.05)
        axes[0].pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                    shadow=False, startangle=90, textprops={'fontsize': 10})
        axes[0].set_title('Class Distribution', fontweight='bold', pad=15)

        # Length distribution
        real_lens = df[df['label']==0]['text'].astype(str).str.len()
        fake_lens = df[df['label']==1]['text'].astype(str).str.len()
        axes[1].hist(real_lens, bins=20, alpha=0.7, label='Real', color='#10b981', edgecolor='white')
        axes[1].hist(fake_lens, bins=20, alpha=0.7, label='Fake', color='#ef4444', edgecolor='white')
        axes[1].set_xlabel('Article Length (characters)')
        axes[1].set_ylabel('Frequency')
        axes[1].set_title('Article Length Distribution', fontweight='bold', pad=15)
        axes[1].legend()

        return self._save("dataset_stats")

    def model_comparison(self, models_data: Dict, y_test, width: int = 78):
        """Multi-metric comparison bar chart + radar chart."""
        if not VISUALS_AVAILABLE:
            return None
        fig = plt.figure(figsize=(14, 6))
        gs = fig.add_gridspec(1, 2, width_ratios=[2, 1])

        ax1 = fig.add_subplot(gs[0])
        names = list(models_data.keys())
        metrics = ['accuracy', 'cv_mean', 'precision', 'recall', 'f1']
        metric_labels = ['Test Acc', 'CV Acc', 'Precision', 'Recall', 'F1-Score']
        x = np.arange(len(names))
        width_bar = 0.15
        colors = ['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b', '#ef4444']

        for idx, (metric, label, color) in enumerate(zip(metrics, metric_labels, colors)):
            if metric in ['accuracy', 'cv_mean']:
                values = [models_data[n][metric] for n in names]
            else:
                # Compute from predictions
                values = []
                for n in names:
                    preds = models_data[n]['predictions']
                    if metric == 'precision':
                        values.append(precision_score(y_test, preds, zero_division=0))
                    elif metric == 'recall':
                        values.append(recall_score(y_test, preds, zero_division=0))
                    elif metric == 'f1':
                        values.append(f1_score(y_test, preds, zero_division=0))
            ax1.bar(x + idx*width_bar - 2*width_bar, values, width_bar, label=label, color=color, edgecolor='white', linewidth=0.5)

        ax1.set_ylabel('Score')
        ax1.set_title('Model Performance Comparison', fontweight='bold', pad=15)
        ax1.set_xticks(x)
        ax1.set_xticklabels([n.replace(' ', '\n') for n in names], fontsize=8)
        ax1.legend(loc='upper left', fontsize=8)
        ax1.set_ylim(0, 1.15)
        ax1.axhline(y=0.5, color='gray', linestyle='--', alpha=0.3)

        # Training time comparison
        ax2 = fig.add_subplot(gs[1])
        times = [models_data[n]['time'] for n in names]
        bars = ax2.barh(names, times, color=['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b'], edgecolor='white')
        ax2.set_xlabel('Time (seconds)')
        ax2.set_title('Training Time', fontweight='bold', pad=15)
        for bar, t in zip(bars, times):
            ax2.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2, f'{t:.2f}s', 
                    va='center', fontsize=8)

        return self._save("model_comparison")

    def confusion_matrices(self, models_data: Dict, y_test):
        """Heatmaps for all models."""
        if not VISUALS_AVAILABLE:
            return None
        n_models = len(models_data)
        cols = min(2, n_models)
        rows = (n_models + cols - 1) // cols
        fig, axes = plt.subplots(rows, cols, figsize=(5*cols, 4*rows))
        if n_models == 1:
            axes = np.array([axes])
        axes = axes.flatten()

        for idx, (name, data) in enumerate(models_data.items()):
            cm = confusion_matrix(y_test, data['predictions'])
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx],
                       xticklabels=['Real', 'Fake'], yticklabels=['Real', 'Fake'],
                       cbar=False, linewidths=0.5, linecolor='white')
            axes[idx].set_title(name, fontweight='bold', pad=10)
            axes[idx].set_xlabel('Predicted')
            axes[idx].set_ylabel('Actual')

        # Hide unused subplots
        for idx in range(n_models, len(axes)):
            axes[idx].axis('off')

        return self._save("confusion_matrices")

    def roc_curves(self, models_data: Dict, X_test, y_test):
        """ROC curves for all models."""
        if not VISUALS_AVAILABLE:
            return None
        fig, ax = plt.subplots(figsize=(8, 7))
        colors = ['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b']

        for idx, (name, data) in enumerate(models_data.items()):
            model = data['model']
            if hasattr(model, "predict_proba"):
                probas = model.predict_proba(X_test)[:, 1]
                fpr, tpr, _ = roc_curve(y_test, probas)
                auc = roc_auc_score(y_test, probas)
                ax.plot(fpr, tpr, color=colors[idx % len(colors)], lw=2, 
                       label=f'{name} (AUC = {auc:.3f})')

        ax.plot([0, 1], [0, 1], color='gray', lw=1, linestyle='--', alpha=0.5)
        ax.set_xlim([0.0, 1.0])
        ax.set_ylim([0.0, 1.05])
        ax.set_xlabel('False Positive Rate')
        ax.set_ylabel('True Positive Rate')
        ax.set_title('ROC Curves Comparison', fontweight='bold', pad=15)
        ax.legend(loc='lower right', fontsize=9)
        ax.grid(True, alpha=0.3)

        return self._save("roc_curves")

    def feature_importance(self, models_data: Dict, feature_names: List[str]):
        """Feature importance for tree-based models."""
        if not VISUALS_AVAILABLE:
            return None
        tree_models = {n: d for n, d in models_data.items() if hasattr(d['model'], 'feature_importances_')}
        if not tree_models:
            return None

        n_models = len(tree_models)
        cols = min(2, n_models)
        rows = (n_models + cols - 1) // cols
        fig, axes = plt.subplots(rows, cols, figsize=(6*cols, 4*rows))
        if n_models == 1:
            axes = [axes]
        else:
            axes = axes.flatten()

        for idx, (name, data) in enumerate(tree_models.items()):
            importances = data['model'].feature_importances_
            # Top 15 features
            indices = np.argsort(importances)[-15:]
            top_names = [feature_names[i] if i < len(feature_names) else f'feat_{i}' for i in indices]
            top_vals = importances[indices]

            axes[idx].barh(range(len(top_vals)), top_vals, color='#8b5cf6', edgecolor='white')
            axes[idx].set_yticks(range(len(top_vals)))
            axes[idx].set_yticklabels(top_names, fontsize=8)
            axes[idx].set_xlabel('Importance')
            axes[idx].set_title(f'{name} - Top Features', fontweight='bold', pad=10)
            axes[idx].invert_yaxis()

        for idx in range(n_models, len(axes)):
            axes[idx].axis('off')

        return self._save("feature_importance")

    def linguistic_profile(self, df: pd.DataFrame):
        """Distribution of linguistic features by class."""
        if not VISUALS_AVAILABLE or 'label' not in df.columns:
            return None

        features = ['polarity', 'subjectivity', 'sensational_score', 'caps_ratio', 
                   'lexical_diversity', 'emotional_score', 'credibility_score']
        fig, axes = plt.subplots(2, 4, figsize=(14, 7))
        axes = axes.flatten()

        real_df = df[df['label'] == 0]
        fake_df = df[df['label'] == 1]

        for idx, feat in enumerate(features):
            if feat not in df.columns:
                axes[idx].axis('off')
                continue
            axes[idx].hist(real_df[feat], bins=15, alpha=0.6, label='Real', color='#10b981', edgecolor='white')
            axes[idx].hist(fake_df[feat], bins=15, alpha=0.6, label='Fake', color='#ef4444', edgecolor='white')
            axes[idx].set_title(feat.replace('_', ' ').title(), fontweight='bold', fontsize=9)
            axes[idx].legend(fontsize=7)
            axes[idx].tick_params(labelsize=7)

        # Summary stats text
        axes[-1].axis('off')
        summary_text = (
            f"Dataset Summary\n"
            f"{'─'*20}\n"
            f"Total Articles: {len(df)}\n"
            f"Real: {len(real_df)} | Fake: {len(fake_df)}\n"
            f"Avg Words (Real): {real_df['word_count'].mean():.1f}\n"
            f"Avg Words (Fake): {fake_df['word_count'].mean():.1f}\n"
            f"Avg Sensational (Fake): {fake_df['sensational_score'].mean():.2f}\n"
            f"Avg Credibility (Real): {real_df['credibility_score'].mean():.2f}"
        )
        axes[-1].text(0.1, 0.5, summary_text, fontsize=10, family='monospace',
                     verticalalignment='center', bbox=dict(boxstyle='round', facecolor='#f3f4f6', alpha=0.8))

        return self._save("linguistic_profile")

    def prediction_gauge(self, models_data: Dict, text_preview: str):
        """Gauge chart for single prediction consensus."""
        if not VISUALS_AVAILABLE:
            return None
        fig, ax = plt.subplots(figsize=(8, 4))

        names = list(models_data.keys())
        confidences = []
        colors_bar = []
        for name, data in models_data.items():
            # Use stored prediction data or dummy
            confidences.append(data.get('last_confidence', 50))
            colors_bar.append('#ef4444' if data.get('last_prediction', 0) == 1 else '#10b981')

        y_pos = np.arange(len(names))
        bars = ax.barh(y_pos, confidences, color=colors_bar, edgecolor='white', height=0.6)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(names, fontsize=9)
        ax.set_xlim(0, 100)
        ax.set_xlabel('Confidence (%)')
        ax.set_title(f'Prediction Confidence\n{text_preview[:50]}...', fontweight='bold', pad=15)
        ax.axvline(x=50, color='gray', linestyle='--', alpha=0.5)

        for bar, conf in zip(bars, confidences):
            ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, 
                   f'{conf:.1f}%', va='center', fontsize=9, fontweight='bold')

        return self._save("prediction_gauge")


# ═══════════════════════════════════════════════════════════════════════════════
#   CORE DETECTOR ENGINE
# ═══════════════════════════════════════════════════════════════════════════════
class FakeNewsDetector:
    MODELS_DIR = "saved_models"
    FEATURE_COLS = [
        'polarity', 'subjectivity', 'word_count', 'sentence_count',
        'avg_word_length', 'exclamation_count', 'question_count',
        'caps_ratio', 'quote_count', 'number_count',
        'sensational_score', 'avg_sentence_length',
        'lexical_diversity', 'emotional_score', 'credibility_score',
        'all_caps_words', 'url_count', 'syllable_proxy'
    ]

    def __init__(self):
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.scaler: Optional[MinMaxScaler] = None
        self.models: Dict[str, Dict] = {}
        self.data: Optional[pd.DataFrame] = None
        self.analyzer = LinguisticAnalyzer()
        self.visualizer = Visualizer()
        self.X_train = self.X_test = self.y_train = self.y_test = None
        os.makedirs(self.MODELS_DIR, exist_ok=True)

    # ─── NLP: Text Preprocessing ───
    def preprocess(self, text: str) -> str:
        if pd.isna(text):
            return ""
        text = str(text).lower()
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        text = re.sub(r'\S+@\S+', '', text)
        text = re.sub(r'\d+', '', text)
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    # ─── Data: Large Synthetic Dataset (48 samples) ───
    def generate_demo_data(self) -> pd.DataFrame:
        fake = [
            "BREAKING: Secret government documents leaked proving alien contact since 1950s",
            "SHOCKING: Famous celebrity faked death and now living in remote island bunker",
            "MUST READ: Local mom discovers $50,000/week method working from phone banks furious",
            "URGENT: New world order planning to ban cash and private property next month",
            "EXPOSED: Vaccines contain nano-trackers according to anonymous whistleblower",
            "INCREDIBLE: Man finds fountain of youth in kitchen spice rack doctors stunned",
            "ALERT: Phone companies secretly recording every conversation through microphone",
            "REVEALED: Underground elite society controls all elections and stock markets",
            "WARNING: Drinking this common household chemical cures all diseases permanently",
            "HIDDEN TRUTH: Moon landing completely staged in Hollywood studio insiders confess",
            "CONSPIRACY: 5G towers designed to control human thoughts and behavior confirmed",
            "MIRACLE: Blind man regains sight after drinking blessed water from internet preacher",
            "SHOCKING VIDEO: Politician caught in underground crime ring leaked footage",
            "BREAKING: Scientists discover earth is actually flat and NASA has been lying",
            "URGENT ALERT: New law will confiscate all guns and property starting Monday",
            "EXPOSED: Major food brands putting poison in products to reduce population",
            "MUST SEE: Single tablet cures diabetes cancer and heart disease overnight",
            "SECRET REVEALED: Free energy device suppressed by oil companies for decades",
            "WARNING: Using this household item daily causes instant brain damage",
            "SHOCKING: Famous actor secretly replaced by clone after 2015 accident",
            "BREAKING: Underground tunnels connecting all Walmart stores for military use",
            "EXPOSED: Chemtrails confirmed to be mind control chemicals by pilot whistleblower",
            "URGENT: All bank accounts to be frozen next week according to leaked memo",
            "MIRACLE CURE: Ancient herb completely eliminates all viruses in 24 hours"
        ]
        real = [
            "Federal Reserve announces quarter-point interest rate hike to combat inflation",
            "Local school district receives state grant for STEM education program expansion",
            "Researchers publish peer-reviewed study on climate change impact on coral reefs",
            "City council approves municipal budget focusing on infrastructure and public safety",
            "Technology firm reports quarterly earnings showing steady revenue growth",
            "Health department recommends updated COVID-19 booster for elderly populations",
            "University study finds correlation between regular exercise and cognitive health",
            "Regional meteorological service forecasts mild temperatures for upcoming week",
            "National sports team secures championship victory through disciplined training",
            "Agricultural department releases annual crop yield report showing stable production",
            "International summit addresses global trade agreements and economic cooperation",
            "Medical journal publishes findings on new treatment protocol for diabetes management",
            "Senate committee reviews proposed legislation on renewable energy tax incentives",
            "Local library launches digital archive project preserving historical newspapers",
            "Transportation authority announces schedule changes for commuter rail lines",
            "University researchers develop new algorithm for early detection of forest fires",
            "Chamber of commerce reports increase in small business registrations this quarter",
            "Public health officials monitor seasonal flu activity across regional hospitals",
            "Education board approves updated curriculum standards for mathematics and science",
            "Defense department releases annual report on military readiness and modernization",
            "Environmental agency issues guidelines for industrial waste disposal compliance",
            "Labor statistics bureau publishes monthly employment figures for manufacturing sector",
            "Foreign ministry announces diplomatic visit to strengthen bilateral trade relations",
            "Space agency confirms successful deployment of new weather monitoring satellite"
        ]
        texts = fake + real
        labels = [1]*len(fake) + [0]*len(real)
        df = pd.DataFrame({
            'text': texts, 'label': labels, 'title': texts,
            'source': ['synthetic']*len(texts),
            'date': [datetime.now().strftime("%Y-%m-%d")]*len(texts)
        })
        return df.sample(frac=1, random_state=42).reset_index(drop=True)

    # ─── Data: Load CSV or Demo ───
    def load_data(self, filepath: Optional[str] = None) -> pd.DataFrame:
        if filepath and os.path.exists(filepath):
            print(f"{UI.BGREEN}[✓]{UI.RST} Loading dataset from {UI.BOLD}{filepath}{UI.RST}")
            df = pd.read_csv(filepath)
            for col in ['title', 'content', 'article']:
                if 'text' not in df.columns and col in df.columns:
                    df['text'] = df[col]
            if 'label' not in df.columns:
                raise ValueError("Dataset must contain 'label' column (0=Real, 1=Fake)")
            print(f"{UI.BGREEN}[✓]{UI.RST} Loaded {UI.BOLD}{len(df)}{UI.RST} records")
        else:
            if filepath:
                print(f"{UI.BRED}[✗]{UI.RST} File not found: {filepath}")
            print(f"{UI.BYELLOW}[!]{UI.RST} Generating synthetic demo dataset...")
            df = self.generate_demo_data()
            print(f"{UI.BGREEN}[✓]{UI.RST} Generated {UI.BOLD}{len(df)}{UI.RST} records")
        return df

    # ─── Data: Statistics ───
    def show_stats(self, df: pd.DataFrame, show_charts: bool = True):
        print(UI.header("📊 DATASET STATISTICS", 70))
        total = len(df)
        fake = int((df['label']==1).sum()) if 'label' in df.columns else 0
        real = int((df['label']==0).sum()) if 'label' in df.columns else 0
        avg_len = int(df['text'].astype(str).str.len().mean()) if 'text' in df.columns else 0
        max_len = int(df['text'].astype(str).str.len().max()) if 'text' in df.columns else 0
        min_len = int(df['text'].astype(str).str.len().min()) if 'text' in df.columns else 0

        UI.table(
            ["Metric", "Value"],
            [
                ["Total Articles", f"{total:,}"],
                ["Fake Articles", f"{UI.BRED}{fake:,}{UI.RST}"],
                ["Real Articles", f"{UI.BGREEN}{real:,}{UI.RST}"],
                ["Fake Ratio", f"{fake/total:.1%}" if total else "N/A"],
                ["Real Ratio", f"{real/total:.1%}" if total else "N/A"],
                ["Avg. Length", f"{avg_len:,} chars"],
                ["Max Length", f"{max_len:,} chars"],
                ["Min Length", f"{min_len:,} chars"],
            ],
            [30, 38]
        )

        if show_charts and VISUALS_AVAILABLE:
            path = self.visualizer.dataset_stats(df)
            if path:
                print(f"{UI.BCYAN}[📊]{UI.RST} Chart saved: {UI.BOLD}{path}{UI.RST}")

    # ─── ML: Full Pipeline ───
    def prepare_data(self, df: pd.DataFrame):
        print(f"\n{UI.BBLUE}[*]{UI.RST} {UI.BOLD}Running NLP Feature Pipeline...{UI.RST}")
        steps = ["Text Cleaning", "Linguistic Analysis", "TF-IDF Vectorization",
                 "Feature Scaling", "Train/Test Split"]
        for i, step in enumerate(steps, 1):
            UI.progress(step, i, len(steps))
            if step == "Text Cleaning":
                df['cleaned'] = df['text'].apply(self.preprocess)
            elif step == "Linguistic Analysis":
                feats = df['cleaned'].apply(self.analyzer.analyze)
                for col in self.FEATURE_COLS:
                    df[col] = [f[col] for f in feats]
            elif step == "TF-IDF Vectorization":
                self.vectorizer = TfidfVectorizer(
                    max_features=5000, ngram_range=(1,2),
                    min_df=1, max_df=0.95, stop_words='english', sublinear_tf=True
                )
                X_tfidf = self.vectorizer.fit_transform(df['cleaned'])
            elif step == "Feature Scaling":
                extra = df[self.FEATURE_COLS].values
                X_raw = np.hstack([X_tfidf.toarray(), extra])
                self.scaler = MinMaxScaler()
                X = self.scaler.fit_transform(X_raw)
                y = df['label'].values
            elif step == "Train/Test Split":
                self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
                    X, y, test_size=0.2, random_state=42, stratify=y
                )
        print(f"{UI.BGREEN}[✓]{UI.RST} Pipeline done: {UI.BOLD}{len(self.X_train)} train{UI.RST} │ {UI.BOLD}{len(self.X_test)} test{UI.RST}")

    # ─── ML: Train 4 Robust Models ───
    def train_models(self):
        print(UI.header("🧠 MODEL TRAINING PHASE", 70))
        configs = {
            "Logistic Regression": LogisticRegression(max_iter=3000, random_state=42, C=1.0, class_weight='balanced'),
            "Random Forest": RandomForestClassifier(n_estimators=300, random_state=42, max_depth=15, class_weight='balanced'),
            "Support Vector Machine": SVC(kernel='rbf', probability=True, random_state=42, class_weight='balanced'),
            "Gradient Boosting": GradientBoostingClassifier(n_estimators=200, max_depth=3, random_state=42)
        }
        for name, model in configs.items():
            print(f"\n{UI.BBLUE}[*]{UI.RST} Training {UI.BOLD}{name}{UI.RST}...")
            start = time.time()
            model.fit(self.X_train, self.y_train)
            preds = model.predict(self.X_test)
            acc = accuracy_score(self.y_test, preds)
            # Cross-validation for robustness
            cv_scores = cross_val_score(model, self.X_train, self.y_train, cv=3, scoring='accuracy')
            cv_mean = cv_scores.mean()
            # ROC-AUC
            if hasattr(model, "predict_proba"):
                probas = model.predict_proba(self.X_test)[:, 1]
                auc = roc_auc_score(self.y_test, probas)
            else:
                auc = 0.5
            elapsed = time.time() - start
            self.models[name] = {
                "model": model, "accuracy": acc, "predictions": preds,
                "auc": auc, "time": elapsed, "cv_mean": cv_mean
            }
            bar = f"{UI.BGREEN}{'█'*int(acc*20)}{UI.RST}{UI.DIM}{'░'*(20-int(acc*20))}{UI.RST}"
            print(f"{UI.BGREEN}[✓]{UI.RST} {name:<22} Acc: {acc:.1%} CV: {cv_mean:.1%} {bar} ({elapsed:.2f}s)")

    # ─── ML: Comparison ───
    def show_comparison(self, show_charts: bool = True):
        print(UI.header("📈 MODEL PERFORMANCE COMPARISON", 70))
        rows = []
        for name, data in self.models.items():
            cm = confusion_matrix(self.y_test, data['predictions'])
            tn, fp, fn, tp = cm.ravel()
            prec = tp/(tp+fp) if (tp+fp)>0 else 0
            rec = tp/(tp+fn) if (tp+fn)>0 else 0
            f1 = 2*(prec*rec)/(prec+rec) if (prec+rec)>0 else 0
            rows.append([
                name, f"{data['accuracy']:.1%}", f"{data['cv_mean']:.1%}",
                f"{data['auc']:.3f}", f"{prec:.3f}", f"{rec:.3f}", f"{f1:.3f}"
            ])
        UI.table(
            ["Model", "Test Acc", "CV Acc", "ROC-AUC", "Precision", "Recall", "F1"],
            rows, [20, 10, 10, 10, 10, 10, 10]
        )
        best = max(self.models.items(), key=lambda x: x[1]['accuracy'])
        print(f"\n{UI.BGREEN}🏆 BEST: {best[0]} (Test={best[1]['accuracy']:.1%}, CV={best[1]['cv_mean']:.1%}){UI.RST}")

        if show_charts and VISUALS_AVAILABLE:
            path = self.visualizer.model_comparison(self.models, self.y_test)
            if path:
                print(f"{UI.BCYAN}[📊]{UI.RST} Chart saved: {UI.BOLD}{path}{UI.RST}")

            path2 = self.visualizer.roc_curves(self.models, self.X_test, self.y_test)
            if path2:
                print(f"{UI.BCYAN}[📊]{UI.RST} ROC curves saved: {UI.BOLD}{path2}{UI.RST}")

            # Build feature names list
            tfidf_names = self.vectorizer.get_feature_names_out().tolist() if self.vectorizer else []
            feature_names = tfidf_names + self.FEATURE_COLS
            path3 = self.visualizer.feature_importance(self.models, feature_names)
            if path3:
                print(f"{UI.BCYAN}[📊]{UI.RST} Feature importance saved: {UI.BOLD}{path3}{UI.RST}")

    # ─── ML: Confusion Matrix ───
    def show_confusion(self, show_charts: bool = True):
        print(UI.header("🔢 CONFUSION MATRIX ANALYSIS", 70))
        for name, data in self.models.items():
            cm = confusion_matrix(self.y_test, data['predictions'])
            tn, fp, fn, tp = cm.ravel()
            specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
            sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
            print(f"\n{UI.BOLD}{UI.BCYAN}▸ {name}{UI.RST}")
            UI.table(
                ["Metric", "Count", "Meaning", "Rate"],
                [
                    ["True Negative", f"{tn}", "Real → Real", f"{specificity:.1%}"],
                    ["False Positive", f"{UI.BRED}{fp}{UI.RST}", "Real → Fake (Type I)", f"{fp/(tn+fp):.1%}" if (tn+fp)>0 else "N/A"],
                    ["False Negative", f"{UI.BRED}{fn}{UI.RST}", "Fake → Real (Type II)", f"{fn/(tp+fn):.1%}" if (tp+fn)>0 else "N/A"],
                    ["True Positive", f"{UI.BGREEN}{tp}{UI.RST}", "Fake → Fake", f"{sensitivity:.1%}"],
                ], [20, 12, 28, 10]
            )

        if show_charts and VISUALS_AVAILABLE:
            path = self.visualizer.confusion_matrices(self.models, self.y_test)
            if path:
                print(f"{UI.BCYAN}[📊]{UI.RST} Confusion matrix charts saved: {UI.BOLD}{path}{UI.RST}")

    # ─── Predict: Single Article ───
    def predict(self, text: str, show_charts: bool = True):
        if not self.models or self.vectorizer is None or self.scaler is None:
            print(f"{UI.BRED}[✗]{UI.RST} Models not trained!")
            return
        cleaned = self.preprocess(text)
        tfidf = self.vectorizer.transform([cleaned])
        feats = self.analyzer.analyze(cleaned)
        extra = np.array([[feats[c] for c in self.FEATURE_COLS]])
        X_raw = np.hstack([tfidf.toarray(), extra])
        X = self.scaler.transform(X_raw)

        print(UI.header("🔍 ARTICLE ANALYSIS REPORT", 70))
        preview = text[:300] + "..." if len(text) > 300 else text
        print(f"{UI.BOLD}📰 Original:{UI.RST}\n   {UI.DIM}{preview}{UI.RST}")
        print(UI.sep(70))
        print(f"{UI.BOLD}🧹 Cleaned:{UI.RST}\n   {UI.DIM}{cleaned[:300]}{UI.RST}")
        print(UI.sep(70))
        print(f"{UI.BOLD}📊 Linguistic Features:{UI.RST}")
        feat_rows = []
        for k, v in feats.items():
            label = k.replace('_', ' ').title()
            if k == 'polarity':
                val = f"{v:.3f} {'😊 Positive' if v>0.1 else '😠 Negative' if v<-0.1 else '😐 Neutral'}"
            elif k == 'subjectivity':
                val = f"{v:.3f} {'🔥 Highly Subjective' if v>0.5 else '📘 Objective'}"
            elif k == 'caps_ratio':
                val = f"{v:.3f} ({int(v*100)}%) {'⚠️ YELLING' if v>0.15 else ''}"
            elif k == 'sensational_score':
                val = f"{v} {'🚨 HIGH SENSATIONALISM' if v>=2 else '✓ Low'}"
            elif k == 'lexical_diversity':
                val = f"{v:.3f} {'📚 Rich Vocab' if v>0.7 else '📝 Repetitive'}"
            elif k == 'emotional_score':
                val = f"{v} {'💥 Emotional' if v>0 else '⚖️ Neutral'}"
            elif k == 'credibility_score':
                val = f"{v} {'🎓 Credible Markers' if v>0 else '❌ No Sources'}"
            elif k == 'url_count':
                val = f"{v} {'🔗 Links Present' if v>0 else 'No Links'}"
            else:
                val = str(v)
            feat_rows.append([label, val])

        # Split into two tables for better layout
        mid = len(feat_rows) // 2 + len(feat_rows) % 2
        UI.table(["Feature", "Value"], feat_rows[:mid], [24, 44])
        UI.table(["Feature", "Value"], feat_rows[mid:], [24, 44])

        print(UI.sep(70))
        print(f"{UI.BOLD}🤖 Predictions:{UI.RST}\n")
        pred_rows = []
        votes = []
        confidences = []
        for name, data in self.models.items():
            p = data["model"].predict(X)[0]
            votes.append(p)
            if hasattr(data["model"], "predict_proba"):
                prob = data["model"].predict_proba(X)[0][p] * 100
            else:
                prob = 50.0
            confidences.append(prob)
            # Store for visualizer
            data['last_prediction'] = p
            data['last_confidence'] = prob
            label = "FAKE NEWS ⚠️" if p==1 else "GENUINE NEWS ✅"
            color = UI.BRED if p==1 else UI.BGREEN
            pred_rows.append([name, f"{color}{label}{UI.RST}", f"{prob:.1f}%"])
        UI.table(["Model", "Verdict", "Confidence"], pred_rows, [26, 26, 16])

        fake_votes = sum(votes)
        real_votes = len(votes) - fake_votes
        consensus = "FAKE" if fake_votes > real_votes else "GENUINE"
        ccolor = UI.BRED if consensus=="FAKE" else UI.BGREEN
        confidence_avg = np.mean([c for v, c in zip(votes, confidences) if v == (1 if consensus=="FAKE" else 0)])

        print(f"\n{UI.BOLD}📊 Ensemble Consensus:{UI.RST} {ccolor}{UI.BOLD}{consensus}{UI.RST} ({fake_votes} Fake vs {real_votes} Real)")
        print(f"{UI.BOLD}🎯 Average Confidence:{UI.RST} {ccolor}{confidence_avg:.1f}%{UI.RST}")

        # Risk assessment
        risk_level = "LOW"
        risk_color = UI.BGREEN
        if consensus == "FAKE":
            if confidence_avg > 85:
                risk_level = "CRITICAL"
                risk_color = UI.BRED
            elif confidence_avg > 60:
                risk_level = "HIGH"
                risk_color = UI.BYELLOW
            else:
                risk_level = "MODERATE"
                risk_color = UI.BYELLOW

        print(f"{UI.BOLD}⚠️  Risk Assessment:{UI.RST} {risk_color}{UI.BOLD}{risk_level}{UI.RST}")

        if show_charts and VISUALS_AVAILABLE:
            path = self.visualizer.prediction_gauge(self.models, preview)
            if path:
                print(f"{UI.BCYAN}[📊]{UI.RST} Prediction chart saved: {UI.BOLD}{path}{UI.RST}")

    # ─── Save / Load ───
    def save(self):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        bundle = {
            "vectorizer": self.vectorizer, "scaler": self.scaler,
            "models": {n: d["model"] for n, d in self.models.items()},
            "timestamp": ts, "features": self.FEATURE_COLS
        }
        path = os.path.join(self.MODELS_DIR, f"models_{ts}.pkl")
        with open(path, "wb") as f:
            pickle.dump(bundle, f)
        print(f"{UI.BGREEN}[✓]{UI.RST} Saved to {UI.BOLD}{path}{UI.RST}")

    def load(self):
        files = sorted([f for f in os.listdir(self.MODELS_DIR) if f.endswith(".pkl")])
        if not files:
            print(f"{UI.BRED}[✗]{UI.RST} No saved models in {self.MODELS_DIR}/")
            return False
        print(f"{UI.BBLUE}[*]{UI.RST} Saved models:")
        for i, f in enumerate(files, 1):
            print(f"   {i}. {f}")
        choice = input(f"{UI.BOLD}[?] Select (1-{len(files)}): {UI.RST}").strip()
        try:
            idx = int(choice)-1
            path = os.path.join(self.MODELS_DIR, files[idx])
            with open(path, "rb") as f:
                b = pickle.load(f)
            self.vectorizer, self.scaler = b["vectorizer"], b["scaler"]
            for n, m in b["models"].items():
                self.models[n] = {"model": m, "accuracy": 0, "predictions": None, "auc": 0, "time": 0, "cv_mean": 0}
            self.FEATURE_COLS = b.get("features", self.FEATURE_COLS)
            print(f"{UI.BGREEN}[✓]{UI.RST} Loaded {files[idx]}")
            return True
        except Exception as e:
            print(f"{UI.BRED}[✗]{UI.RST} Load failed: {e}")
            return False

    # ─── Interactive ───
    def interactive(self):
        print(UI.header("💬 INTERACTIVE DETECTOR", 70))
        print(f"{UI.DIM}Type 'exit' or '0' to return to menu{UI.RST}\n")
        while True:
            text = input(f"{UI.BBLUE}[?]{UI.RST} Paste article: {UI.RST}").strip()
            if text.lower() in ('exit','quit','back','0'):
                break
            if not text:
                print(f"{UI.BYELLOW}[!]{UI.RST} Empty input.")
                continue
            self.predict(text)
            print()

    # ─── Batch ───
    def batch(self):
        path = input(f"{UI.BBLUE}[?]{UI.RST} CSV path (needs 'text' col): {UI.RST}").strip()
        if not os.path.exists(path):
            print(f"{UI.BRED}[✗]{UI.RST} File not found!")
            return
        try:
            df = pd.read_csv(path)
            if 'text' not in df.columns:
                print(f"{UI.BRED}[✗]{UI.RST} Needs 'text' column!"); return
            print(f"\n{UI.BBLUE}[*]{UI.RST} Processing {UI.BOLD}{len(df)}{UI.RST} articles...")
            results = []
            for idx, row in df.iterrows():
                print(f"\n{UI.BCYAN}─── {idx+1}/{len(df)} ───{UI.RST}")
                self.predict(str(row['text']), show_charts=False)
                # Collect votes for summary
                votes = [d["model"].predict(self.X_test)[0] if len(self.X_test) > 0 else 0 for d in self.models.values()]
                results.append("FAKE" if sum(votes) > len(votes)/2 else "REAL")

            # Batch summary
            fake_count = results.count("FAKE")
            real_count = results.count("REAL")
            print(f"\n{UI.header('📋 BATCH SUMMARY', 70)}")
            UI.table(
                ["Metric", "Count"],
                [
                    ["Total Processed", f"{len(results)}"],
                    ["Predicted Fake", f"{UI.BRED}{fake_count}{UI.RST}"],
                    ["Predicted Real", f"{UI.BGREEN}{real_count}{UI.RST}"],
                    ["Fake %", f"{fake_count/len(results)*100:.1f}%"],
                ], [30, 38]
            )
        except Exception as e:
            print(f"{UI.BRED}[✗]{UI.RST} Error: {e}")

    # ─── Retrain ───
    def retrain(self):
        path = input(f"{UI.BBLUE}[?]{UI.RST} Dataset path (Enter=demo): {UI.RST}").strip()
        try:
            self.data = self.load_data(path if path else None)
            self.show_stats(self.data)
            self.prepare_data(self.data)
            self.train_models()
            if input(f"{UI.BBLUE}[?]{UI.RST} Save models? (y/n): {UI.RST}").strip().lower() == 'y':
                self.save()
            print(f"{UI.BGREEN}[✓]{UI.RST} Retrain complete!")
        except Exception as e:
            print(f"{UI.BRED}[✗]{UI.RST} Error: {e}")
            import traceback; traceback.print_exc()

    # ─── Info ───
    def info(self):
        print(UI.header("ℹ️  SYSTEM INFORMATION", 70))
        UI.table(
            ["Property", "Value"],
            [
                ["Project", "Fake News Detection Using NLP"],
                ["Author", "Ussu"],
                ["Version", "5.0.0 VISUAL ENHANCED"],
                ["Python", sys.version.split()[0]],
                ["Models", "Logistic Regression, Random Forest, SVM, Gradient Boosting"],
                ["Features", "TF-IDF + 18 Linguistic Features (scaled)"],
                ["Visuals", "✅ Enabled" if VISUALS_AVAILABLE else "❌ matplotlib not installed"],
                ["Scaling", "MinMaxScaler (fixes negative value issues)"],
                ["Validation", "3-Fold Cross-Validation + Hold-out Test"],
                ["GitHub", "https://github.com/issu321"],
                ["Repo", "https://github.com/issu321/NLP-Python"],
            ], [22, 46]
        )

    # ─── Splash ───
    def splash(self):
        art = f"""
{UI.BCYAN}{UI.BOLD}
    ███████╗ █████╗ ██╗  ██╗███████╗    ███╗   ██╗███████╗██╗    ██╗███████╗
    ██╔════╝██╔══██╗██║ ██╔╝██╔════╝    ████╗  ██║██╔════╝██║    ██║██╔════╝
    █████╗  ███████║█████╔╝ █████╗      ██╔██╗ ██║█████╗  ██║ █╗ ██║███████╗
    ██╔══╝  ██╔══██║██╔═██╗ ██╔══╝      ██║╚██╗██║██╔══╝  ██║███╗██║╚════██║
    ██║     ██║  ██║██║  ██╗███████╗    ██║ ╚████║███████╗╚███╔███╔╝███████║
    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝    ╚═╝  ╚═══╝╚══════╝ ╚══╝╚══╝ ╚══════╝
{UI.RST}
        {UI.BMAGENTA}{UI.BOLD}🔍 FAKE NEWS DETECTION USING NATURAL LANGUAGE PROCESSING{UI.RST}
        {UI.DIM}Real-World Ready NLP Toolkit by Ussu{UI.RST}
        {UI.DIM}https://github.com/issu321/NLP-Python{UI.RST}
        """
        print(art)
        time.sleep(0.3)

    # ─── Main ───
    def run(self):
        self.splash()
        data_path = sys.argv[1] if len(sys.argv) > 1 else None
        try:
            self.data = self.load_data(data_path)
            self.show_stats(self.data)
            self.prepare_data(self.data)
            self.train_models()
        except Exception as e:
            print(f"{UI.BRED}[✗]{UI.RST} Init error: {e}")
            import traceback; traceback.print_exc()
            return

        while True:
            print(UI.header("📋 MAIN COMMAND CENTER", 70))
            items = [
                ("1","💬 Interactive Analysis","Paste text, get instant classification + charts"),
                ("2","📈 Model Comparison","Accuracy, CV, ROC-AUC, Precision, Recall, F1 + graphs"),
                ("3","🔢 Confusion Matrices","TP/FP/TN/FN per model + heatmap charts"),
                ("4","📁 Batch CSV Predict","Classify hundreds of articles with summary"),
                ("5","📊 Dataset Stats","Current data overview + distribution charts"),
                ("6","🔄 Retrain Models","Load custom CSV, rebuild all models"),
                ("7","💾 Save Models","Export trained bundle"),
                ("8","📂 Load Models","Import saved bundle"),
                ("9","ℹ️  System Info","Project metadata & version"),
                ("0","🚪 Exit","Quit application"),
            ]
            rows = [[n, f"{UI.BOLD}{t}{UI.RST}", f"{UI.DIM}{d}{UI.RST}"] for n,t,d in items]
            UI.table(["#","Option","Description"], rows, [6,36,26])

            print(f"\n{UI.DIM}{'─'*70}{UI.RST}")
            choice = input(f"{UI.BOLD}{UI.BCYAN}[?]{UI.RST} Select option (0-9): {UI.RST}").strip()
            print(f"{UI.DIM}{'─'*70}{UI.RST}")

            match choice:
                case "1":
                    self.interactive()
                case "2":
                    self.show_comparison()
                case "3":
                    self.show_confusion()
                case "4":
                    self.batch()
                case "5":
                    self.show_stats(self.data)
                    if VISUALS_AVAILABLE and self.data is not None:
                        path = self.visualizer.linguistic_profile(self.data)
                        if path:
                            print(f"{UI.BCYAN}[📊]{UI.RST} Linguistic profile saved: {UI.BOLD}{path}{UI.RST}")
                case "6":
                    self.retrain()
                case "7":
                    self.save()
                case "8":
                    self.load()
                case "9":
                    self.info()
                case "0":
                    print(f"\n{UI.BGREEN}[✓]{UI.RST} Goodbye! {UI.BCYAN}https://github.com/issu321/NLP-Python{UI.RST}\n")
                    break
                case _:
                    print(f"{UI.BYELLOW}[!]{UI.RST} Invalid selection. Please enter a number between 0-9.")


if __name__ == "__main__":
    warnings.filterwarnings('ignore')
    FakeNewsDetector().run()