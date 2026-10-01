"""Wire the three layers and demonstrate each search mode."""

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from application.image_service import ImageService
from application.query_service import QueryService
from application.ranking_service import RankingService
from application.search_service import SearchService
from application.speech_service import SpeechService
from data.order_repository import OrderRepository
from data.product_repository import ProductRepository
from data.vector_index import VectorIndex
from presentation.search_ui import SearchUI


def build_search_ui():
    return SearchUI(
        query_service=QueryService(),
        speech_service=SpeechService(),
        image_service=ImageService(),
        search_service=SearchService(
            product_repository=ProductRepository(),
            order_repository=OrderRepository(),
            vector_index=VectorIndex(),
        ),
        ranking_service=RankingService(),
    )


def show_results(ui, results, multimodal=False):
    print("Returned Products and Ranking Score:")
    print(ui.format_results(results, multimodal=multimodal))
    print()


def run_demo():
    ui = build_search_ui()
    image_input = [0.95, 0.05, 0.0, 0.0]

    print("=== TEXT SEARCH ===")
    print("Input: black shoes")
    print("Processing: Normalize text -> Keyword matching -> Candidate retrieval -> Ranking")
    show_results(ui, ui.search_text("black shoes"))

    print("=== VOICE SEARCH ===")
    print("Input: find running shoes")
    print("Processing: Simulated Speech-to-Text -> Transcribed text: find running shoes")
    print("            Voice query -> Text candidate retrieval -> Ranking")
    show_results(ui, ui.search_voice("find running shoes"))

    print("=== IMAGE SEARCH ===")
    print(f"Input: {image_input}")
    print("Processing: Simulated image representation -> Cosine similarity -> Candidate retrieval -> Ranking")
    show_results(ui, ui.search_image(image_input))

    print("=== MULTIMODAL SEARCH ===")
    print(f"Input: text='black shoes', image={image_input}")
    print("Weights: text=0.5, image=0.5")
    print("Processing: Text retrieval + Image similarity -> Score combination -> Ranking")
    show_results(ui, ui.search_multimodal("black shoes", image_input), multimodal=True)

    print("=== ORDER SEARCH ===")
    print("Input: O001")
    print("Processing: Exact order ID lookup")
    order = ui.search_order("O001")
    if order:
        print(f'Order ID: {order["order_id"]} | Status: {order["status"]} | Total: {order["total"]}')
    else:
        print("Order not found.")


def main():
    output = StringIO()
    with redirect_stdout(output):
        run_demo()

    results = output.getvalue()
    result_path = Path(__file__).resolve().parent / "result.md"
    result_path.write_text(
        "# Search Demonstration Results\n\n```text\n" + results.rstrip() + "\n```\n",
        encoding="utf-8",
    )
    print(results, end="")


if __name__ == "__main__":
    main()
