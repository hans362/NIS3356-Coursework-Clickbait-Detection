import json
from matplotlib import pyplot as plt
from datetime import datetime, timedelta
from evaluators.induction import InductionEvaluator
from evaluators.relevance import RelevanceEvaluator
import os

induction_evaluator = InductionEvaluator("keywords.txt", "word2vec.model")
relevance_evaluator = RelevanceEvaluator("word2vec.model")

plt.rcParams["font.sans-serif"] = ["Arial Unicode MS"]


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
        article["score"] = induction_evaluator.calculate_index(title) * 0.4
        article["score"] += relevance_evaluator.calculate_index(title, text) * 0.6
    return articles


def calculate_average_index(articles, start_date, end_date):
    total_score = 0
    cnt = 0
    for article in articles:
        if start_date <= article["update_time"] <= end_date:
            total_score += article["score"]
            cnt += 1
    return total_score / cnt if cnt > 0 else 0


def evaluate_dataset(file, max_size=None):
    articles = load_articles(file, max_size)
    articles = calculate_index_bulk(articles)

    x = []
    y = []
    days = 365 * 2
    start_date = datetime.now() - timedelta(days=days)
    print("===================================")
    print(
        "Average index of "
        + os.path.basename(file)
        + " in the past {} days".format(days)
        + ": "
        + str(calculate_average_index(articles, start_date, datetime.now()))
    )
    print(
        f"Average index in 2023: {calculate_average_index(articles, datetime(2023, 1, 1), datetime(2023, 12, 31))}"
    )
    print(
        f"Average index in 2024: {calculate_average_index(articles, datetime(2024, 1, 1), datetime(2024, 12, 31))}"
    )
    print("===================================")
    for i in range(days - 120):
        end_date = start_date + timedelta(days=120)
        x.append(end_date)
        y.append(calculate_average_index(articles, start_date, end_date))
        start_date += timedelta(days=1)
    plt.plot(x, y, label=os.path.basename(file).split(".")[0])

    articles = sorted(articles, key=lambda x: x["score"], reverse=True)
    print("===================================")
    print("Top 20 articles")
    print("===================================")
    for article in articles[:20]:
        print(article["title"] + "\t" + str(article["score"]))
    print("===================================")
    print("Bottom 20 articles")
    print("===================================")
    for article in articles[-20:]:
        print(article["title"] + "\t" + str(article["score"]))


corpus_dir = "./weixin-corpus"
for file in os.listdir(corpus_dir):
    if file.endswith(".json"):
        evaluate_dataset(os.path.join(corpus_dir, file))

plt.title("120天滑动窗口平均标题党指数变化")
plt.ylabel("标题党指数")
plt.legend()
plt.show()
