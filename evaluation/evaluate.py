"""Small top-1 evaluation set for the simulated prototype."""

from main import build_search_ui


TESTS = [
    {"mode": "text", "query": "black running shoes", "expected_product_id": 1},
    {"mode": "text", "query": "leather bag", "expected_product_id": 4},
    {"mode": "voice", "query": "find running shoes", "expected_product_id": 1},
    {"mode": "image", "query": [0.95, 0.05, 0.0, 0.0], "expected_product_id": 1},
    {"mode": "multimodal", "query": ("black shoes", [0.95, 0.05, 0.0, 0.0]), "expected_product_id": 1},
    {"mode": "order", "query": "O001", "expected_order_id": "O001"},
    {"mode": "text", "query": "trainers", "expected_product_id": 10},
]


def evaluate():
    ui = build_search_ui()
    successful = 0
    incorrect = []
    for case in TESTS:
        mode = case["mode"]
        query = case["query"]
        if mode == "order":
            order = ui.search_order(query)
            actual = order["order_id"] if order else None
            expected = case["expected_order_id"]
        else:
            if mode == "multimodal":
                results = ui.search_multimodal(*query)
            else:
                results = getattr(ui, f"search_{mode}")(query)
            actual = results[0]["product"]["id"] if results else None
            expected = case["expected_product_id"]
        if actual == expected:
            successful += 1
        else:
            incorrect.append((mode, query, expected, actual))

    print(f"Number of Test Queries: {len(TESTS)}")
    print(f"Number of Successful Queries: {successful}")
    print(f"Success Rate: {successful / len(TESTS):.2%}")
    print("Examples of Incorrect Results:")
    if incorrect:
        for mode, query, expected, actual in incorrect:
            print(f"- {mode} query {query!r}: expected {expected}, returned {actual}")
    else:
        print("- None")


if __name__ == "__main__":
    evaluate()
