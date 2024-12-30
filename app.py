from flask import Flask, redirect, request, jsonify, render_template
from evaluators.induction import InductionEvaluator
from evaluators.relevance import RelevanceEvaluator
import os
import json
from datetime import datetime
import sqlite3

app = Flask(__name__, static_folder="static", template_folder="templates")
induction_evaluator = InductionEvaluator("keywords.txt", "word2vec.model")
relevance_evaluator = RelevanceEvaluator("word2vec.model")

db = sqlite3.connect("data.db")
cursor = db.cursor()
exists = cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name='articles'"
).fetchone()
if not exists:
    cursor.execute(
        "CREATE TABLE articles (title TEXT, source TEXT, update_time TEXT, induction_score REAL, relevance_score REAL, score REAL)"
    )
    db.commit()


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


@app.route("/public/<path:path>", methods=["GET"])
def public(path):
    return redirect(f"/metabase/public/{path}")


def load_articles(file, max_size=None):
    raw = json.loads(open(file, "r", encoding="utf-8").read())
    articles = []
    titles = set()
    for article in raw:
        if article["title"] in titles:
            continue
        if "update_time" in article:
            article["update_time"] = datetime.strptime(
                article["update_time"], "%m/%d/%Y %H:%M:%S"
            )
        titles.add(article["title"])
        articles.append(article)
    articles = sorted(articles, key=lambda x: x["update_time"], reverse=True)
    return articles[:max_size] if max_size is not None else articles


def calculate_index_bulk(articles):
    for article in articles:
        title = article["title"]
        text = article["text"]
        article["induction_score"] = induction_evaluator.calculate_index(title)
        article["relevance_score"] = relevance_evaluator.calculate_index(title, text)
        article["score"] = (
            article["induction_score"] * 0.4 + article["relevance_score"] * 0.6
        )
    return articles


if __name__ == "__main__":
    if not exists:
        corpus_dirs = ["./wechat-corpus", "./toutiao-corpus"]
        for corpus_dir in corpus_dirs:
            for file in os.listdir(corpus_dir):
                if file.endswith(".json"):
                    articles = load_articles(os.path.join(corpus_dir, file))
                    articles = calculate_index_bulk(articles)
                    cursor.executemany(
                        "INSERT INTO articles VALUES (?, ?, ?, ?, ?, ?)",
                        [
                            (
                                article["title"],
                                os.path.basename(file).split(".")[0],
                                article["update_time"].strftime("%Y-%m-%d %H:%M:%S"),
                                article["induction_score"],
                                article["relevance_score"],
                                article["score"],
                            )
                            for article in articles
                        ],
                    )
                    db.commit()
    app.run(host="0.0.0.0", port=25000)
