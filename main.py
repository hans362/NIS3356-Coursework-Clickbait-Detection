import json
from matplotlib import pyplot as plt
from datetime import datetime, timedelta
from evaluators.induction import InductionEvaluator
import os

induction_evaluator = InductionEvaluator("keywords.txt", "word2vec.model")

plt.rcParams["font.sans-serif"] = ["Arial Unicode MS"]


def load_articles(file):
    articles = json.loads(open(file, "r", encoding="utf-8").read())
    for article in articles:
        if "update_time" in article:
            article["update_time"] = datetime.strptime(
                article["update_time"], "%m/%d/%Y %H:%M:%S"
            )
    articles = sorted(articles, key=lambda x: x["update_time"], reverse=True)
    return articles


def calculate_index_bulk(articles):
    for article in articles:
        title = article["title"]
        article["score"] = induction_evaluator.calculate_index(title)
    return articles


def calculate_average_index(articles, start_date, end_date):
    total_score = 0
    cnt = 0
    for article in articles:
        if start_date <= article["update_time"] <= end_date:
            total_score += article["score"]
            cnt += 1
    return total_score / cnt if cnt > 0 else 0


def evaluate_dataset(file):
    articles = load_articles(file)
    articles = calculate_index_bulk(articles)

    x = []
    y = []
    days = 365 * 2
    start_date = datetime.now() - timedelta(days=days)
    for i in range(days - 120):
        end_date = start_date + timedelta(days=120)
        x.append(start_date)
        y.append(calculate_average_index(articles, start_date, end_date))
        start_date += timedelta(days=1)
    plt.plot(x, y, label=os.path.basename(file))

    articles = sorted(articles, key=lambda x: x["score"], reverse=True)
    print("===================================")
    print("Top 10 articles")
    print("===================================")
    for article in articles[:10]:
        print(article["title"] + "\t" + str(article["score"]))
    print("===================================")
    print("Bottom 10 articles")
    print("===================================")
    for article in articles[-10:]:
        print(article["title"] + "\t" + str(article["score"]))


corpus_dir = "."
for file in os.listdir(corpus_dir):
    if file.endswith(".json"):
        evaluate_dataset(os.path.join(corpus_dir, file))

plt.legend()
plt.show()
