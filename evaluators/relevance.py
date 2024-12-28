import gensim
import jieba
import jieba.analyse


class RelevanceEvaluator:
    def __init__(self, model_file):
        self.load_model(model_file)

    def load_model(self, file):
        print("Loading Word2Vec model...")
        self.model = gensim.models.KeyedVectors.load(file)
        print("Word2Vec model loaded.")

    def calculate_similarity(self, word1, word2):
        try:
            return self.model.similarity(word1, word2)
        except Exception:
            return 0

    def calculate_index(self, title, text):
        title = jieba.lcut(title)
        keywords = jieba.analyse.extract_tags(text, topK=len(title))
        match_cnt = 0
        for keyword in keywords:
            if keyword in title:
                match_cnt += 1
            else:
                similarity = 0
                for word in title:
                    similarity = max(
                        self.calculate_similarity(keyword, word), similarity
                    )
                if similarity > 0.5:
                    match_cnt += similarity
        return 100 - match_cnt / len(title) * 100


if __name__ == "__main__":
    relevance_evaluator = RelevanceEvaluator("word2vec.model")
    print(relevance_evaluator.calculate_index("title", "text"))
