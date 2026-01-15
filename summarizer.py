import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

# Safe downloads
for pkg in ["punkt", "punkt_tab", "stopwords"]:
    try:
        nltk.data.find(pkg)
    except LookupError:
        nltk.download(pkg)

STOP_WORDS = set(stopwords.words("english"))

# Detect programming code
def is_code(text):
    code_patterns = [
        r"#include", r"def ", r"import ", r"class ",
        r"public static void", r"int main",
        r"{", r"}", r";", r"//"
    ]
    return any(re.search(p, text) for p in code_patterns)

# Text summarization
def summarize_text(text, max_sentences=5):
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())

    freq = {}
    for w in words:
        if w.isalnum() and w not in STOP_WORDS:
            freq[w] = freq.get(w, 0) + 1

    scores = {}
    for sent in sentences:
        for w in word_tokenize(sent.lower()):
            if w in freq:
                scores[sent] = scores.get(sent, 0) + freq[w]

    summary = sorted(scores, key=scores.get, reverse=True)
    return " ".join(summary[:max_sentences])

# Code explanation
def explain_code(code):
    lines = code.split("\n")
    explanation = []

    explanation.append("This program performs the following tasks:")

    for line in lines:
        line = line.strip()

        if line.startswith("import"):
            explanation.append("• Imports required libraries.")
        elif line.startswith("def"):
            explanation.append("• Defines a function.")
        elif "print" in line:
            explanation.append("• Prints output to the screen.")
        elif "for" in line:
            explanation.append("• Uses a loop for iteration.")
        elif "if" in line:
            explanation.append("• Uses a conditional statement.")
        elif "return" in line:
            explanation.append("• Returns a value from the function.")

    return "\n".join(set(explanation))

# Unified summarizer
def summarize_any(text):
    if is_code(text):
        return explain_code(text)
    else:
        return summarize_text(text)
