from flask import Flask, request, jsonify, render_template
from evaluators.induction import InductionEvaluator
from evaluators.relevance import RelevanceEvaluator

app = Flask(__name__, static_folder="static", template_folder="templates")
induction_evaluator = InductionEvaluator("keywords.txt", "word2vec.model")
relevance_evaluator = RelevanceEvaluator("word2vec.model")


@app.route("/api/relevance", methods=["POST"])
def relevance():
    title = request.form.get("title")
    text = request.form.get("text")
    score = relevance_evaluator.calculate_index(title, text)
    return jsonify({"score": score})


@app.route("/api/induction", methods=["POST"])
def induction():
    title = request.form.get("title")
    score = induction_evaluator.calculate_index(title)
    return jsonify({"score": score})


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=25000, debug=True)
