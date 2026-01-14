import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

STOP_WORDS = set(stopwords.words("english"))

# ---------- DETECT CODE ----------
def is_code(text):
    code_keywords = [
        "def ", "class ", "#include", "import ", "public ", "private ",
        "void ", "int ", "return ", "printf", "cout<<",
        "System.out.println", "{", "}", ";"
    ]
    return any(k in text for k in code_keywords)

# ---------- DETECT LANGUAGE ----------
def detect_language(text):
    if "#include" in text:
        return "C / C++"
    if "System.out.println" in text:
        return "Java"
    if "def " in text:
        return "Python"
    if "function " in text:
        return "JavaScript"
    return "Unknown language"

# ---------- EXPLAIN CODE ----------
def explain_code(text):
    explanation = []
    language = detect_language(text)
    explanation.append(f"This code is written in {language}.")

    lines = text.splitlines()

    for line in lines:
        line = line.strip()

        if line.startswith("#include"):
            explanation.append("This line includes a library required for input and output operations.")

        elif line.startswith("import"):
            explanation.append("This line imports a required module or package.")

        elif re.search(r"\bdef\b", line):
            explanation.append("This defines a function which contains reusable logic.")

        elif re.search(r"\bclass\b", line):
            explanation.append("This defines a class which groups related data and functions.")

        elif "main" in line:
            explanation.append("This is the main entry point of the program where execution starts.")

        elif "printf" in line or "print" in line or "System.out.println" in line:
            explanation.append("This line prints output to the screen.")

        elif "return" in line:
            explanation.append("This statement returns a value from the function.")

    if len(explanation) <= 1:
        explanation.append("The code performs logical operations and controls program execution.")

    return "\n".join(explanation)

# ---------- TEXT CHUNKING ----------
def chunk_text(text, max_words=1200):
    words = text.split()
    for i in range(0, len(words), max_words):
        yield " ".join(words[i:i + max_words])

# ---------- TEXT SUMMARIZER ----------
def summarize_text_chunk(text, max_sentences=5):
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())

    word_freq = {}
    for word in words:
        if word.isalnum() and word not in STOP_WORDS:
            word_freq[word] = word_freq.get(word, 0) + 1

    sentence_scores = {}
    for sent in sentences:
        for word in word_tokenize(sent.lower()):
            if word in word_freq:
                sentence_scores[sent] = sentence_scores.get(sent, 0) + word_freq[word]

    top_sentences = sorted(
        sentence_scores,
        key=sentence_scores.get,
        reverse=True
    )[:max_sentences]

    return " ".join(top_sentences)

# ---------- UNIVERSAL FUNCTION ----------
def summarize_any(text):
    if is_code(text):
        return explain_code(text)

    summaries = []
    for chunk in chunk_text(text):
        summaries.append(summarize_text_chunk(chunk))

    return " ".join(summaries)
