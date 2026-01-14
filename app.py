from flask import Flask, render_template, request
from summarizer import summarize_any
import PyPDF2

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    summary = ""

    if request.method == "POST":
        text = request.form.get("text", "")

        if "pdf" in request.files:
            pdf = request.files["pdf"]
            if pdf and pdf.filename:
                reader = PyPDF2.PdfReader(pdf)
                text = ""
                for page in reader.pages:
                    if page.extract_text():
                        text += page.extract_text() + " "

        if len(text.strip()) > 50:
            summary = summarize_any(text)
        else:
            summary = "Please provide sufficient content."

    return render_template("index.html", summary=summary)

if __name__ == "__main__":
    app.run(debug=True)
