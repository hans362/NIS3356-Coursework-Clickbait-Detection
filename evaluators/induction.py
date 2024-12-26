import gensim
import jieba


class InductionEvaluator:
    def __init__(self, keywords_file, model_file):
        self.load_keywords(keywords_file)
        self.load_model(model_file)

    def load_keywords(self, file):
        self.keywords = open(file, "r", encoding="utf-8").read().split("\n")

    def load_model(self, file):
        print("Loading Word2Vec model...")
        self.model = gensim.models.KeyedVectors.load(file)
        print("Word2Vec model loaded.")

    def calculate_similarity(self, word1, word2):
        try:
            return self.model.similarity(word1, word2)
        except Exception:
            return 0

    def calculate_index(self, title):
        title = jieba.lcut(title)
        match_cnt = 0
        for word in title:
            if word in self.keywords:
                match_cnt += 1
            else:
                similarity = 0
                for keyword in self.keywords:
                    similarity = max(
                        self.calculate_similarity(word, keyword), similarity
                    )
                if similarity > 0.5:
                    match_cnt += similarity
        return min(match_cnt / len(title) * 100 * 2, 100)
