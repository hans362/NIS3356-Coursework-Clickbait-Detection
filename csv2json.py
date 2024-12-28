import csv
import json
import os
from datetime import datetime


def csv2json(file):
    with open(file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        articles = []
        for row in reader:
            if reader.line_num == 1:
                continue
            if row[2] == "无正文内容":
                continue
            article = {
                "title": row[0],
                "text": row[2],
                "update_time": datetime.strptime(row[3], "%Y-%m-%d %H:%M").strftime(
                    "%m/%d/%Y %H:%M:%S"
                ),
            }
            articles.append(article)
    with open(file.replace("csv", "json"), "w", encoding="utf-8") as f:
        f.write(json.dumps(articles, ensure_ascii=False))


if __name__ == "__main__":
    files = os.listdir("toutiao-corpus")
    for file in files:
        if file.endswith(".csv"):
            csv2json(os.path.join("toutiao-corpus", file))
