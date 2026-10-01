"""Build a common structured representation for each input mode."""


class QueryService:
    def text_query(self, text):
        return {"type": "text", "query": text}

    def voice_query(self, text):
        return {"type": "voice", "query": text}

    def image_query(self, embedding):
        return {"type": "image", "embedding": embedding}

    def multimodal_query(self, text, embedding):
        return {"type": "multimodal", "query": text, "embedding": embedding}
