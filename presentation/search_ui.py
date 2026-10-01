"""Console-facing input and result formatting."""


class SearchUI:
    def __init__(self, query_service, speech_service, image_service, search_service, ranking_service):
        self.query_service = query_service
        self.speech_service = speech_service
        self.image_service = image_service
        self.search_service = search_service
        self.ranking_service = ranking_service

    def search_text(self, text):
        query = self.query_service.text_query(text)
        return self.ranking_service.rank_text(self.search_service.retrieve_text(query["query"]))

    def search_voice(self, voice_text):
        transcript = self.speech_service.transcribe(voice_text)
        query = self.query_service.voice_query(transcript)
        return self.ranking_service.rank_text(self.search_service.retrieve_text(query["query"]))

    def search_image(self, image_input):
        embedding = self.image_service.encode(image_input)
        query = self.query_service.image_query(embedding)
        return self.ranking_service.rank_image(self.search_service.retrieve_image(query["embedding"]))

    def search_multimodal(self, text, image_input, text_weight=0.5, image_weight=0.5):
        embedding = self.image_service.encode(image_input)
        query = self.query_service.multimodal_query(text, embedding)
        candidates = self.search_service.retrieve_multimodal(query["query"], query["embedding"])
        return self.ranking_service.rank_multimodal(candidates, text_weight, image_weight)

    def search_order(self, order_id):
        return self.search_service.find_order(order_id)

    def format_results(self, results, multimodal=False):
        """Render ranked products for the console demo."""
        if not results:
            return "No matching products found."
        lines = []
        for position, result in enumerate(results, 1):
            line = f'{position}. {result["product"]["name"]} | ranking_score = {result["ranking_score"]:.4f}'
            if multimodal:
                line += (f' | text_score = {result["text_score"]:.4f}'
                         f' | image_score = {result["image_score"]:.4f}'
                         f' | combined_score = {result["combined_score"]:.4f}')
            lines.append(line)
        return "\n".join(lines)
