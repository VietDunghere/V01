# AGENTS.md
## Assignment 06 — Multimodal Search System for E-Commerce

Tài liệu này mô tả **cách triển khai phần Python prototype** cho Assignment 06.  
Agent phải ưu tiên **đúng yêu cầu đề bài, đúng UML đã thiết kế, code đơn giản, dễ chạy và dễ giải thích trong report**.

> Không tự ý đổi kiến trúc, gộp các service/repository đã tách riêng, thêm framework web, database server, model AI thật hoặc các chức năng ngoài phạm vi nếu chưa được yêu cầu.

---

# 1. Mục tiêu implementation

Xây dựng một Python prototype cho hệ thống:

**Multimodal E-Commerce Search System**

Prototype phải thể hiện pipeline:

```text
Different Inputs
    ↓
Common Query Representation
    ↓
Retrieval
    ↓
Ranking
    ↓
Results
```

Các phần **bắt buộc theo Task 5**:

1. `ProductRepository`
2. `Text Search`
3. `Simulated Voice Search`
4. `Image Similarity Search`
5. `Result Ranking`

Các phần **bắt buộc theo Task 6**:

- demo ít nhất 3 query:
  1. Text query
  2. Voice query
  3. Image query

Với mỗi query phải thể hiện:

```text
Input
Processing
Returned Products
Ranking Score
```

Ngoài ra, project hiện tại đã thiết kế thêm:

- `OrderRepository`
- `VectorIndex`
- `Multimodal Search` theo `Text + Image`

Các phần này phải được giữ nếu đã xuất hiện trong UML/report, nhưng không được làm phức tạp hơn mức cần thiết.

---

# 2. Nguyên tắc kiến trúc bắt buộc

Kiến trúc phải giữ đúng Three-Layer Architecture:

```text
Presentation Layer
        ↓
Application / Intelligence Layer
        ↓
Data Layer
```

Không được để Presentation Layer truy cập trực tiếp Data Layer.

Ví dụ sai:

```text
SearchUI → ProductRepository
SearchUI → ProductDatabase
SearchUI → VectorIndex
```

Ví dụ đúng:

```text
SearchUI
   ↓
QueryService / SpeechService / ImageService
   ↓
SearchService
   ↓
ProductRepository / OrderRepository / VectorIndex
```

---

# 3. Mapping UML sang code

## Presentation Layer

```text
SearchUI
```

File:

```text
presentation/search_ui.py
```

## Application / Intelligence Layer

```text
QueryService
SpeechService
ImageService
SearchService
RankingService
```

Files:

```text
application/query_service.py
application/speech_service.py
application/image_service.py
application/search_service.py
application/ranking_service.py
```

## Data Layer

```text
ProductRepository
OrderRepository
VectorIndex
```

Files:

```text
data/product_repository.py
data/order_repository.py
data/vector_index.py
```

Conceptual storage:

```text
ProductDatabase → dataset/products.json
OrderDatabase   → dataset/orders.json
ImageStorage    → dataset/images/
```

Không cần tạo class `ProductDatabase`, `OrderDatabase`, `ImageStorage` riêng nếu JSON/folder đã đóng vai trò storage.

---

# 4. Cấu trúc project

Dùng cấu trúc sau:

```text
assignment06/
│
├── main.py
├── README.md
├── requirements.txt
│
├── presentation/
│   ├── __init__.py
│   └── search_ui.py
│
├── application/
│   ├── __init__.py
│   ├── query_service.py
│   ├── speech_service.py
│   ├── image_service.py
│   ├── search_service.py
│   └── ranking_service.py
│
├── data/
│   ├── __init__.py
│   ├── product_repository.py
│   ├── order_repository.py
│   └── vector_index.py
│
├── dataset/
│   ├── products.json
│   ├── orders.json
│   └── images/
│
└── evaluation/
    ├── __init__.py
    └── evaluate.py
```

Nếu repository hiện tại đã là root của assignment thì không tạo thêm thư mục `assignment06/` bọc ngoài.

---

# 5. Product dataset

`dataset/products.json` phải có **ít nhất 10 products**.

Mỗi product nên có tối thiểu:

```json
{
  "id": 1,
  "name": "Nike Running Shoes",
  "category": "shoes",
  "color": "black",
  "price": 120,
  "stock": 10,
  "description": "Black lightweight running shoes",
  "image": "images/nike_running_shoes.jpg"
}
```

Nên tạo dữ liệu đủ đa dạng để demo tốt:

```text
running shoes
sports shoes
casual shoes
leather bag
backpack
shirt
jacket
watch
headphones
sneakers
```

Không tạo 10 sản phẩm gần như giống hệt nhau.

---

# 6. ProductRepository

File:

```text
data/product_repository.py
```

Class:

```python
class ProductRepository:
    ...
```

Trách nhiệm:

- load product data từ `dataset/products.json`;
- cung cấp product data cho Application Layer;
- không xử lý query;
- không ranking.

API tối thiểu:

```python
all_products()
find_by_id(product_id)
```

Ví dụ:

```python
repository = ProductRepository()
products = repository.all_products()
```

Không hard-code toàn bộ product list trong `SearchService`.

---

# 7. OrderRepository

File:

```text
data/order_repository.py
```

Class:

```python
class OrderRepository:
    ...
```

Dataset:

```text
dataset/orders.json
```

Ví dụ một order:

```json
{
  "order_id": "O001",
  "customer_id": "C001",
  "date": "2026-09-30",
  "status": "Shipped",
  "total": 150
}
```

API tối thiểu:

```python
find_order(order_id)
```

Behavior:

- trả order nếu tồn tại;
- trả `None` nếu không tồn tại.

Chỉ cần hỗ trợ search bằng `order_id`.

Không cần NLP phức tạp cho query kiểu:

```text
where is my latest order?
```

---

# 8. VectorIndex

File:

```text
data/vector_index.py
```

Class:

```python
class VectorIndex:
    ...
```

Trách nhiệm:

- lưu mapping `product_id -> artificial embedding`;
- cung cấp vector cho Image Search;
- không tự ranking.

Ví dụ:

```python
{
    1: np.array([0.9, 0.1, 0.2]),
    2: np.array([0.8, 0.2, 0.1]),
    3: np.array([0.1, 0.2, 0.9])
}
```

API gợi ý:

```python
all_embeddings()
get_embedding(product_id)
```

Tất cả product dùng cho Image Search nên có embedding tương ứng.

---

# 9. QueryService

File:

```text
application/query_service.py
```

Class:

```python
class QueryService:
    ...
```

Mục tiêu:

> Chuyển các input khác nhau thành query object có cấu trúc rõ ràng.

API bắt buộc:

```python
text_query(text)
voice_query(text)
image_query(embedding)
```

Output:

## Text Query

```python
{
    "type": "text",
    "query": "black running shoes"
}
```

## Voice Query

```python
{
    "type": "voice",
    "query": "find running shoes"
}
```

## Image Query

```python
{
    "type": "image",
    "embedding": embedding
}
```

Nếu giữ `Multimodal Search`, thêm:

```python
multimodal_query(text, embedding)
```

Ví dụ:

```python
{
    "type": "multimodal",
    "query": "black shoes",
    "embedding": embedding
}
```

---

# 10. SpeechService

File:

```text
application/speech_service.py
```

Class:

```python
class SpeechService:
    def transcribe(self, audio_input):
        return audio_input
```

Đây là **simulation**.

Không cần:

- microphone;
- audio file processing;
- speech recognition library;
- external Speech-to-Text API.

Ví dụ:

```python
voice_input = "find black running shoes"
text = speech_service.transcribe(voice_input)
```

README phải ghi rõ:

```text
Speech-to-Text is simulated in this prototype.
```

---

# 11. ImageService

File:

```text
application/image_service.py
```

Class:

```python
class ImageService:
    ...
```

Trong prototype không cần image encoder thật.

API gợi ý:

```python
encode(image_input)
```

`image_input` có thể là list hoặc NumPy vector giả lập.

Ví dụ:

```python
query_vector = [0.85, 0.15, 0.20]
embedding = image_service.encode(query_vector)
```

`encode()` chỉ cần:

- convert sang NumPy array;
- validate vector;
- trả embedding.

Không sử dụng CNN, CLIP, ResNet hoặc pretrained model.

README phải ghi:

```text
Image embeddings are simulated using artificial feature vectors.
```

---

# 12. SearchService

File:

```text
application/search_service.py
```

Class:

```python
class SearchService:
    ...
```

Dependencies:

```text
ProductRepository
OrderRepository
VectorIndex
```

`SearchService` chịu trách nhiệm chính về:

```text
Retrieval / Candidate Generation
```

Không để `SearchUI` truy cập repository hoặc vector index trực tiếp.

---

# 13. Text Search

Text Search dùng **keyword matching đơn giản**, đúng tinh thần prototype của assignment.

Searchable text của product nên ghép từ:

```text
name + category + color + description
```

Normalize:

```text
lowercase
strip
split words
```

Cách score khuyến nghị:

```text
text_score = số query words match / tổng số query words
```

Ví dụ:

```text
Query:
black running shoes

Product text:
nike black running shoes

Matched:
black
running
shoes

text_score = 3 / 3 = 1.0
```

Chỉ giữ candidate nếu:

```text
text_score > 0
```

API gợi ý:

```python
retrieve_text(query_text)
```

Output nên có dạng:

```python
[
    {
        "product": product,
        "text_score": 1.0
    }
]
```

Không sort final result ở đây nếu muốn giữ rõ separation giữa Retrieval và Ranking.

---

# 14. Voice Search

Voice Search dùng pipeline:

```text
Voice Input
    ↓
SpeechService.transcribe()
    ↓
QueryService.voice_query()
    ↓
SearchService.retrieve_text()
    ↓
RankingService
```

Không cần thuật toán retrieval riêng cho voice.

Sau Speech-to-Text, voice query được xử lý như text query.

Logic nên tương ứng với Sequence Diagram đã thiết kế:

```text
Customer
→ SearchUI
→ SpeechService
→ SearchUI
→ QueryService
→ SearchService
→ ProductRepository
→ SearchService
→ RankingService
→ SearchService
→ QueryService
→ SearchUI
→ Customer
```

Trong code không cần ép mọi return thành một hàm riêng, nhưng responsibility phải tương ứng.

---

# 15. Cosine Similarity

Image Search phải sử dụng cosine similarity.

Công thức:

```text
cosine_similarity(a, b)
=
dot(a, b)
/
(norm(a) * norm(b))
```

Implementation:

```python
def cosine_similarity(a, b):
    numerator = np.dot(a, b)
    denominator = np.linalg.norm(a) * np.linalg.norm(b)

    if denominator == 0:
        return 0.0

    return float(numerator / denominator)
```

Phải xử lý zero vector an toàn.

---

# 16. Image Similarity Search

API gợi ý:

```python
retrieve_image(query_embedding)
```

Flow:

```text
query embedding
    ↓
VectorIndex
    ↓
cosine similarity với product embeddings
    ↓
candidate products
```

Output:

```python
[
    {
        "product": product,
        "image_score": 0.97
    }
]
```

Không cần model ảnh thật.

Không giả vờ rằng artificial vector là output của pretrained model.

---

# 17. RankingService

File:

```text
application/ranking_service.py
```

Class:

```python
class RankingService:
    ...
```

Trách nhiệm:

- nhận candidates;
- xác định `ranking_score`;
- sort giảm dần;
- trả ranked results.

Phải giữ rõ:

```text
Retrieval ≠ Ranking
```

---

# 18. Text Ranking

API gợi ý:

```python
rank_text(candidates)
```

Dùng:

```text
ranking_score = text_score
```

Sort:

```text
ranking_score DESC
```

Output:

```python
{
    "product": product,
    "text_score": text_score,
    "ranking_score": text_score
}
```

---

# 19. Image Ranking

API:

```python
rank_image(candidates)
```

Dùng:

```text
ranking_score = image_score
```

Sort giảm dần.

Cosine similarity càng cao thì sản phẩm càng tương tự query image.

---

# 20. Multimodal Search — Text + Image

Project đã chọn hỗ trợ:

```text
Text + Image
```

Không cần:

```text
Text + Voice + Image
```

vì voice cuối cùng đã trở thành text.

Flow:

```text
Text Query ──> text_score ──┐
                            ├──> combined_score ──> Ranking
Image Query ─> image_score ─┘
```

Dùng mặc định:

```text
lambda_text  = 0.5
lambda_image = 0.5
```

Công thức:

```text
combined_score
=
lambda_text * text_score
+
lambda_image * image_score
```

API gợi ý:

```python
rank_multimodal(
    candidates,
    text_weight=0.5,
    image_weight=0.5
)
```

Validate:

```text
text_weight + image_weight == 1
```

Candidate multimodal nên có:

```python
{
    "product": product,
    "text_score": ...,
    "image_score": ...
}
```

`combined_score` nên được tính trong `RankingService`.

---

# 21. SearchUI

File:

```text
presentation/search_ui.py
```

Class:

```python
class SearchUI:
    ...
```

Không cần GUI thật.

Có thể là console presentation class.

API gợi ý:

```python
search_text(text)
search_voice(voice_text)
search_image(query_embedding)
search_multimodal(text, query_embedding)
search_order(order_id)
```

`SearchUI` chỉ:

- tiếp nhận input;
- gọi application services;
- format output.

Không được:

- keyword matching;
- cosine similarity;
- direct repository access;
- direct vector index access.

---

# 22. main.py

`main.py` chịu trách nhiệm:

1. tạo dependencies;
2. wire components;
3. chạy demonstration;
4. in input;
5. in processing;
6. in returned products;
7. in ranking score.

Wiring gợi ý:

```python
product_repository = ProductRepository()
order_repository = OrderRepository()
vector_index = VectorIndex()

query_service = QueryService()
speech_service = SpeechService()
image_service = ImageService()

search_service = SearchService(
    product_repository=product_repository,
    order_repository=order_repository,
    vector_index=vector_index,
)

ranking_service = RankingService()

search_ui = SearchUI(
    query_service=query_service,
    speech_service=speech_service,
    image_service=image_service,
    search_service=search_service,
    ranking_service=ranking_service,
)
```

Không dùng global mutable state nếu không cần.

---

# 23. Demonstration bắt buộc

Khi chạy:

```bash
python main.py
```

phải demo ít nhất 3 mode:

```text
Text Search
Voice Search
Image Search
```

Mỗi demo phải thể hiện:

```text
Input
Processing
Returned Products
Ranking Score
```

---

# 24. Text Search Demo

Ví dụ:

```text
=== TEXT SEARCH ===

Input:
black shoes

Processing:
- Normalize text
- Keyword matching
- Candidate retrieval
- Ranking

Results:
1. Nike Running Shoes | score = 1.0000
2. Black Casual Shoes | score = 1.0000
3. Blue Sports Shoes | score = 0.5000
```

Output thực tế phụ thuộc dataset.

---

# 25. Voice Search Demo

Ví dụ:

```text
=== VOICE SEARCH ===

Input:
find running shoes

Processing:
- Simulated Speech-to-Text
- Transcribed text: find running shoes
- Create voice query
- Keyword retrieval
- Ranking

Results:
1. Nike Running Shoes | score = ...
2. Adidas Running Shoes | score = ...
```

Phải ghi rõ:

```text
Simulated Speech-to-Text
```

---

# 26. Image Search Demo

Ví dụ:

```text
=== IMAGE SEARCH ===

Input:
[0.85, 0.15, 0.20]

Processing:
- Simulated image representation
- Cosine similarity
- Candidate retrieval
- Ranking

Results:
1. Nike Running Shoes | score = 0.99
2. Blue Sports Shoes | score = 0.95
```

---

# 27. Multimodal Demo

Nên có thêm:

```text
=== MULTIMODAL SEARCH ===

Text Input:
black shoes

Image Input:
[0.85, 0.15, 0.20]

Weights:
text = 0.5
image = 0.5

Processing:
- Text retrieval
- Image similarity
- Score combination
- Ranking

Results:
1. Product A
   text_score = ...
   image_score = ...
   combined_score = ...
```

---

# 28. Order Search Demo

Có thể demo:

```text
=== ORDER SEARCH ===

Input:
O001

Result:
Order ID: O001
Status: Shipped
Total: 150
```

Nếu không tìm thấy:

```text
Order not found.
```

---

# 29. Experimental Evaluation

Assignment yêu cầu đánh giá prototype bằng một test set nhỏ.

Tạo:

```text
evaluation/evaluate.py
```

Có thể dùng danh sách test query:

```python
tests = [
    {
        "mode": "text",
        "query": "black shoes",
        "expected_product_id": 1
    }
]
```

Evaluation phải báo cáo:

```text
Number of Test Queries
Number of Successful Queries
Success Rate
Examples of Incorrect Results
```

Công thức:

```text
Success Rate
=
Successful Queries / Total Queries
```

Không cần F1, precision, recall nếu không được yêu cầu thêm.

---

# 30. README.md

README phải có tối thiểu:

## Project Overview
Mô tả ngắn hệ thống.

## Architecture

```text
Presentation
→ Application / Intelligence
→ Data
```

## Python Version
Ghi version thực tế.

## Required Packages
Tối thiểu dự kiến:

```text
numpy
```

## Installation

```bash
pip install -r requirements.txt
```

## How to Run

```bash
python main.py
```

## Project Structure
Mô tả folder/file.

## Example Queries
Ví dụ:

```text
black shoes
find running shoes
image vector
O001
```

## Limitations

Bắt buộc ghi:

- Speech-to-Text là simulated.
- Image embeddings là artificial feature vectors.
- Text Search dùng keyword matching đơn giản.
- Dataset nhỏ.
- Đây là prototype, không phải production system.

---

# 31. requirements.txt

Giữ tối giản.

Dự kiến:

```text
numpy
```

Không thêm dependency không sử dụng.

---

# 32. Error handling tối thiểu

Phải xử lý hợp lý:

- empty text query;
- invalid image vector;
- zero vector;
- missing embedding;
- unknown order ID.

Ví dụ output:

```text
No matching products found.
```

hoặc raise `ValueError` với message rõ ràng trong service phù hợp.

---

# 33. Coding style

Ưu tiên:

- code ngắn;
- rõ trách nhiệm;
- tên class/function khớp UML;
- tránh duplicate logic;
- type hints nếu hữu ích;
- docstring ngắn cho public API quan trọng.

Không over-engineer.

Không dùng design pattern phức tạp chỉ để tăng số lượng class.

---

# 34. Không được tự ý thay đổi thiết kế

Agent không được tự ý:

- thêm `SearchController`;
- thêm `MultimodalService`;
- thêm `DatabaseService`;
- gộp `SearchService` với `RankingService`;
- xóa `QueryService`;
- cho `SearchUI` truy cập repository;
- đổi sang MVC;
- thêm Flask/FastAPI/Django;
- thay simulated components bằng model thật;
- thêm database server hoặc vector database thật.

Nếu cần thay đổi architecture, phải báo trước và giải thích lý do.

---

# 35. Acceptance Criteria

## Architecture

- [ ] Có `presentation/`
- [ ] Có `application/`
- [ ] Có `data/`
- [ ] Presentation không truy cập Data Layer trực tiếp
- [ ] `SearchService` và `RankingService` tách riêng

## Product Repository

- [ ] `products.json` có ít nhất 10 products
- [ ] Có `ProductRepository`
- [ ] Có `all_products()`

## Text Search

- [ ] Text query chạy được
- [ ] Có keyword matching
- [ ] Có candidate retrieval
- [ ] Có ranking score
- [ ] Sort cuối cùng do `RankingService`

## Voice Search

- [ ] Có `SpeechService`
- [ ] Speech-to-Text được mô phỏng
- [ ] Có `QueryService.voice_query()`
- [ ] Voice dùng text retrieval
- [ ] Có ranking

## Image Search

- [ ] Có artificial embeddings
- [ ] Có `VectorIndex`
- [ ] Có cosine similarity
- [ ] Có candidate retrieval
- [ ] Có image ranking

## Demonstration

- [ ] `python main.py` chạy được
- [ ] Có Text demo
- [ ] Có Voice demo
- [ ] Có Image demo
- [ ] Mỗi demo hiển thị Input
- [ ] Mỗi demo mô tả Processing
- [ ] Mỗi demo hiển thị Returned Products
- [ ] Mỗi demo hiển thị Ranking Score

## Evaluation

- [ ] Có số test queries
- [ ] Có số successful queries
- [ ] Có success rate
- [ ] Có incorrect examples nếu có

## Documentation

- [ ] Có README
- [ ] README ghi Python version
- [ ] README ghi required packages
- [ ] README ghi cách chạy
- [ ] README ghi project structure
- [ ] README có example commands/queries
- [ ] README ghi limitations

---

# 36. Thứ tự triển khai khuyến nghị

```text
1. Tạo project structure
2. Tạo products.json với >= 10 products
3. Implement ProductRepository
4. Implement OrderRepository
5. Implement VectorIndex
6. Implement QueryService
7. Implement SpeechService
8. Implement ImageService
9. Implement SearchService cho Text Retrieval
10. Implement Cosine Similarity
11. Implement Image Retrieval
12. Implement RankingService
13. Hoàn thiện Text Search end-to-end
14. Hoàn thiện Voice Search end-to-end
15. Hoàn thiện Image Search end-to-end
16. Implement Multimodal Search
17. Implement Order Search
18. Implement SearchUI
19. Wire tất cả trong main.py
20. Tạo demonstration output
21. Tạo evaluation
22. Viết README.md
23. Chạy lại toàn bộ project và sửa import/path
```

---

# 37. Definition of Done

Chạy:

```bash
python main.py
```

phải thành công.

Ít nhất phải chứng minh được:

```text
Text Search  → ranked product results
Voice Search → ranked product results
Image Search → ranked product results
```

Nên có thêm:

```text
Multimodal Search → combined ranked results
Order Search      → order information
```

Project cuối cùng phải thể hiện rõ:

```text
UML Design
    ↓
Three-Layer Python Architecture
    ↓
Executable Search Prototype
```

Ưu tiên hoàn thành đúng architecture và demonstration trước khi nghĩ tới AI model phức tạp.
