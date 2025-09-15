# from flask import Flask, render_template, request
# import pickle

# app = Flask(__name__)

# model = pickle.load(open('model.pkl', 'rb'))
# tfidf_vectorizer = pickle.load(open('tfidf_vectorizer.pkl', 'rb'))

# def detect(input_text):
#     vectorized_text = tfidf_vectorizer.transform([input_text])
#     result = model.predict(vectorized_text)
#     return "Plagiarism Detected" if result[0] == 1 else "No Plagiarism Detected"

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/detect', methods=['POST'])
# def detect_plagiarism():
#     input_text = request.form['text']
#     detection_result = detect(input_text)
#     return render_template('index.html', result=detection_result)

# if __name__ == "__main__":
#     app.run(debug=True)

# from flask import Flask, request, render_template
# import spacy
# from spacy import displacy
# import pickle

# # Load NER model
# nlp = spacy.load("en_core_web_sm")

# # Load plagiarism model + vectorizer (adjust paths if needed)
# with open("model.pkl", "rb") as f:
#     model = pickle.load(f)

# with open("tfidf_vectorizer.pkl", "rb") as f:
#     tfidf_vectorizer = pickle.load(f)

# app = Flask(__name__)

# @app.route("/")
# def index():
#     return render_template("index.html")

# # ---------- NER ----------
# @app.route("/entity", methods=["POST"])
# def entity():
#     file = request.files.get("file")
#     text = request.form.get("text")

#     if file:
#         readable_file = file.read().decode("utf-8", errors="ignore")
#     elif text:
#         readable_file = text
#     else:
#         return render_template("index.html", error="No text or file provided!")

#     docs = nlp(readable_file)
#     html = displacy.render(docs, style="ent", jupyter=False)
#     return render_template("index.html", html=html, text=readable_file, mode="ner")

# # ---------- Plagiarism ----------
# @app.route("/plagiarism", methods=["POST"])
# def plagiarism():
#     text = request.form.get("text")
#     if not text:
#         return render_template("index.html", error="Please enter text to check plagiarism!")

#     # Convert input to features
#     features = tfidf_vectorizer.transform([text])
#     prediction = model.predict(features)[0]  # assume 0 = not plagiarized, 1 = plagiarized

#     result = "Plagiarized ❌" if prediction == 1 else "Not Plagiarized ✅"
#     return render_template("index.html", text=text, result=result, mode="plagiarism")

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, request, render_template
import spacy
from spacy import displacy
import pickle

# Load NER model
nlp = spacy.load("en_core_web_sm")

# Load plagiarism model + vectorizer
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("tfidf_vectorizer.pkl", "rb") as f:
    tfidf_vectorizer = pickle.load(f)

app = Flask(__name__)

# ---------- Home Page ----------
@app.route("/")
def home():
    return render_template("home.html")


# ---------- NER Page ----------
@app.route("/ner", methods=["GET", "POST"])
def ner():
    if request.method == "POST":
        text = request.form.get("text")
        file = request.files.get("file")

        if file and file.filename:
            text = file.read().decode("utf-8", errors="ignore")

        if not text:
            return render_template("ner.html", error="Please provide text or upload a file!")

        docs = nlp(text)
        html = displacy.render(docs, style="ent", jupyter=False)
        return render_template("ner.html", html=html, text=text)

    return render_template("ner.html")


# ---------- Plagiarism Page ----------
@app.route("/plagiarism", methods=["GET", "POST"])
def plagiarism():
    if request.method == "POST":
        text = request.form.get("text")

        if not text:
            return render_template("plagiarism.html", error="Please paste text to check plagiarism!")

        # Transform text and predict
        features = tfidf_vectorizer.transform([text])
        prediction = model.predict(features)[0]  # 0 = Not plagiarized, 1 = Plagiarized

        result = "Plagiarized ❌" if prediction == 1 else "Not Plagiarized ✅"
        return render_template("plagiarism.html", text=text, result=result)

    return render_template("plagiarism.html")


if __name__ == "__main__":
    app.run(debug=True)
