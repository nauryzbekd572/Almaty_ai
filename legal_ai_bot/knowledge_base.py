import os

class KnowledgeBase:
    def __init__(self, filepath="data/laws.txt"):
        self.filepath = filepath
        self.paragraphs = []
        self._load_data()

    def _load_data(self):
        if not os.path.exists(self.filepath):
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            with open(self.filepath, "w", encoding="utf-8") as f:
                f.write("Статья 30. Покупатель вправе вернуть товар в течение 14 дней.")
        
        with open(self.filepath, "r", encoding="utf-8") as f:
            content = f.read()
            self.paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]

    def search_relevant_info(self, query: str) -> str:
        query_words = set(query.lower().split())
        for p in self.paragraphs:
            if any(word in p.lower() for word in query_words):
                return p
        return "Информации по запросу не найдено."
