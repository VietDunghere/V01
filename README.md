# Multimodal E-Commerce Search Prototype

## Project Overview

This Assignment 06 prototype searches a small product catalogue using text, simulated voice input, or an artificial image feature vector. It also combines text and image scores and looks up orders by ID. The pipeline is **input → structured query → candidate retrieval → ranking → results**.

## Architecture

The code follows three layers:

```text
Presentation (SearchUI)
    → Application / Intelligence (QueryService, SpeechService, ImageService,
      SearchService, RankingService)
    → Data (ProductRepository, OrderRepository, VectorIndex)
```

`SearchUI` only calls application services. `SearchService` retrieves candidates from data repositories; `RankingService` computes final scores and sorts them. Products and orders come from JSON files. `VectorIndex` stores one artificial four-dimensional embedding per product. The four dimensions loosely represent footwear, bags, apparel, and accessories/electronics.

## Python Version

Developed with Python 3.11.9.

## Required Packages

- `numpy` (see `requirements.txt`)

## Installation

From this directory:

```bash
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Alternatively, install the requirements in your active Python environment with `python -m pip install -r requirements.txt`.

## How to Run

With dependencies installed in the active environment:

```bash
python main.py
python -m evaluation.evaluate
```

With the Windows virtual environment above, use `.\.venv\Scripts\python.exe` in place of `python` for both commands. `main.py` prints text, voice, image, multimodal, and order examples and writes the same demonstration output to `result.md` in the project root. Each product search shows its input, processing steps, returned products, and ranking scores. Running `main.py` again refreshes the file.

## Project Structure

```text
main.py                    Dependency wiring and demonstration
result.md                  Generated demonstration output
presentation/search_ui.py  Input handling and console formatting
application/              Query, speech, image, retrieval, and ranking services
data/                     Product and order repositories, artificial vector index
dataset/products.json     Ten products
dataset/orders.json       Sample orders
dataset/images/           Sample SVG illustrations referenced by products.json
evaluation/evaluate.py    Small top-1 evaluation set
requirements.txt          Python dependency
```

## Example Queries

- Text: `black shoes`
- Voice: `find running shoes` (text standing in for audio)
- Image vector: `[0.95, 0.05, 0.0, 0.0]`
- Text + image: `black shoes` and the vector above, with weights `0.5` each
- Order ID: `O001`

Text score is the fraction of query words found in the product's name, category, color, or description. Image score uses cosine similarity. Multimodal ranking uses `0.5 × text_score + 0.5 × image_score` by default. Missing score components are zero for candidates found through the other modality. The evaluation reports total queries, successful top-1 queries, success rate, and incorrect examples. Its `trainers` query intentionally exposes a synonym-matching limitation.

## Limitations

- Speech-to-Text is simulated in this prototype.
- Image embeddings are simulated using artificial feature vectors. The SVG illustrations are sample catalogue assets; they are not encoded or searched directly.
- Text Search uses simple keyword matching and does not recognize synonyms or meaning.
- The dataset is small, and order search only supports exact order IDs.
- This is a prototype, not a production system.
