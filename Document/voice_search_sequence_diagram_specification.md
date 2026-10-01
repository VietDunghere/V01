# Sequence Diagram Specification
## Voice Product Search — Multimodal E-Commerce Search System

## 1. Mục tiêu của sơ đồ

Hãy vẽ **01 UML Sequence Diagram** mô tả use case:

> `Customer searches for a product using voice`

Sơ đồ phải thể hiện toàn bộ quá trình từ lúc `Customer` cung cấp voice input cho tới khi hệ thống trả về danh sách sản phẩm đã được ranking.

Đây là **một sơ đồ duy nhất**. Không cần vẽ riêng thêm Sequence Diagram cho `Text Search`, `Image Search`, `Order Search` hay `Multimodal Search` trong Task này.

Sơ đồ phải thể hiện rõ các giai đoạn:

```text
Voice Input
    ↓
Speech-to-Text
    ↓
Query Representation
    ↓
Retrieval
    ↓
Candidate Products
    ↓
Ranking
    ↓
Search Results
```

---

# 2. Các participant bắt buộc

Tạo **7 lifeline**, sắp xếp từ trái sang phải đúng theo thứ tự:

```text
Customer
SearchUI
SpeechService
QueryService
SearchService
ProductRepository
RankingService
```

## 2.1. Loại participant

### `Customer`
- Loại: **Actor**
- Khởi tạo quá trình tìm kiếm.
- Đặt ngoài cùng bên trái.

### `SearchUI`
- Loại: Lifeline / Boundary.
- Tiếp nhận voice input.
- Gọi các service thuộc Application Layer.
- Hiển thị kết quả cuối cùng.

Có thể dùng stereotype `<<boundary>>` nếu muốn, nhưng không bắt buộc.

### `SpeechService`
- Loại: Lifeline / Control / Service.
- Chịu trách nhiệm `Speech-to-Text`.

### `QueryService`
- Loại: Lifeline / Control / Service.
- Chịu trách nhiệm tạo `Query Representation`.

### `SearchService`
- Loại: Lifeline / Control / Service.
- Chịu trách nhiệm `Retrieval`.
- Lấy product data thông qua `ProductRepository`.
- Tạo candidate products.
- Gửi candidate tới `RankingService`.

### `ProductRepository`
- Loại: Lifeline / Entity / Repository.
- Cung cấp product data.
- Không thực hiện UI logic.
- Không thực hiện ranking.

### `RankingService`
- Loại: Lifeline / Control / Service.
- Chịu trách nhiệm ranking candidate products.

---

# 3. Các participant KHÔNG cần đưa vào sơ đồ

Không thêm:

```text
VoiceInput
ImageUpload
ImageService
SearchResultView
ProductDatabase
OrderRepository
OrderDatabase
VectorIndex
ImageStorage
```

Không thêm các thành phần như `Controller`, `Backend`, `Server`, `CustomerDatabase` nếu không có yêu cầu riêng.

---

# 4. Quy ước loại message

## 4.1. Synchronous Message

Dùng khi một participant gọi operation của participant khác và chờ kết quả.

Ký hiệu khái niệm:

```text
A ───────▶ B
```

Trong Visual Paradigm:
- Chọn **Synchronous Message**
- Đường liền
- Arrowhead dạng filled/solid

## 4.2. Return Message

Dùng khi participant trả dữ liệu cho participant đã gọi nó.

Ký hiệu:

```text
A - - - - > B
```

Trong Visual Paradigm:
- Chọn **Return Message**
- Đường nét đứt
- Arrowhead dạng open

## 4.3. Self Message

Dùng khi một participant gọi operation nội bộ của chính nó.

Ví dụ:

```text
SearchService ─┐
               │
SearchService ◀┘
```

Trong sơ đồ này sử dụng một self message trên `SearchService` để thể hiện quá trình tạo candidate products.

## 4.4. Không sử dụng

Không cần:
- Create Message
- Delete Message
- Lost Message
- Found Message

Không có object nào được tạo hoặc hủy trong scenario này.

---

# 5. Trình tự message chính thức

Sơ đồ nên có **13 message**, đi từ trên xuống dưới.

## Step 1 — Customer cung cấp voice input

**From:** `Customer`  
**To:** `SearchUI`  
**Message:** `provideVoiceInput(audio)`  
**Type:** **Synchronous Message**

Ý nghĩa: `Customer` bắt đầu use case bằng cách cung cấp voice/audio query cho `SearchUI`.

Bắt đầu activation bar của `SearchUI`.

---

## Step 2 — SearchUI yêu cầu SpeechService chuyển voice thành text

**From:** `SearchUI`  
**To:** `SpeechService`  
**Message:** `transcribe(audio)`  
**Type:** **Synchronous Message**

Ý nghĩa: `SearchUI` chuyển voice input tới `SpeechService` để thực hiện Speech-to-Text.

Bắt đầu activation bar của `SpeechService`.

---

## Step 3 — SpeechService trả transcribed text

**From:** `SpeechService`  
**To:** `SearchUI`  
**Message:** `transcribedText`  
**Type:** **Return Message**

Ví dụ dữ liệu trả về:

```text
"find black running shoes"
```

Trong prototype, quá trình Speech-to-Text có thể được mô phỏng bằng việc trả lại trực tiếp chuỗi text được cung cấp.

Kết thúc activation của `SpeechService`.

---

## Step 4 — SearchUI yêu cầu QueryService tạo voice query

**From:** `SearchUI`  
**To:** `QueryService`  
**Message:** `createVoiceQuery(transcribedText)`  
**Type:** **Synchronous Message**

`QueryService` tạo common query representation, ví dụ:

```python
{
    "type": "voice",
    "query": "find black running shoes"
}
```

Bắt đầu activation của `QueryService`.

---

## Step 5 — QueryService gửi query tới SearchService

**From:** `QueryService`  
**To:** `SearchService`  
**Message:** `search(queryRepresentation)`  
**Type:** **Synchronous Message**

Ý nghĩa: `SearchService` bắt đầu quá trình Retrieval.

Bắt đầu activation của `SearchService`.

---

## Step 6 — SearchService yêu cầu product data

**From:** `SearchService`  
**To:** `ProductRepository`  
**Message:** `allProducts()`  
**Type:** **Synchronous Message**

`SearchService` không truy cập trực tiếp `ProductDatabase`; nó lấy dữ liệu thông qua `ProductRepository`.

Bắt đầu activation của `ProductRepository`.

---

## Step 7 — ProductRepository trả product data

**From:** `ProductRepository`  
**To:** `SearchService`  
**Message:** `products`  
**Type:** **Return Message**

Product data có thể gồm:

```text
product_id
name
category
color
price
stock
```

Kết thúc activation của `ProductRepository`.

---

## Step 8 — SearchService thực hiện Retrieval

**From:** `SearchService`  
**To:** `SearchService`  
**Message:** `retrieveCandidates(products, queryRepresentation)`  
**Type:** **Self Message**

Ý nghĩa: `SearchService` dùng query và product data để tạo `candidateProducts`.

Đối với Voice Search, voice đã được chuyển thành text, vì vậy retrieval có thể dùng cùng cơ chế keyword matching như Text Search.

Bước này nhằm thể hiện rõ:

```text
Retrieval != Ranking
```

Không bắt buộc vẽ một return riêng từ self message.

---

## Step 9 — SearchService yêu cầu RankingService xếp hạng

**From:** `SearchService`  
**To:** `RankingService`  
**Message:** `rank(candidateProducts, queryRepresentation)`  
**Type:** **Synchronous Message**

`RankingService` tính hoặc sử dụng ranking score và sắp xếp candidate products.

Bắt đầu activation của `RankingService`.

---

## Step 10 — RankingService trả ranked products

**From:** `RankingService`  
**To:** `SearchService`  
**Message:** `rankedProducts`  
**Type:** **Return Message**

Kết thúc activation của `RankingService`.

---

## Step 11 — SearchService trả search results

**From:** `SearchService`  
**To:** `QueryService`  
**Message:** `searchResults`  
**Type:** **Return Message**

`SearchService` hoàn tất retrieval + ranking và trả kết quả cho `QueryService`.

Kết thúc activation của `SearchService`.

---

## Step 12 — QueryService trả kết quả cho SearchUI

**From:** `QueryService`  
**To:** `SearchUI`  
**Message:** `searchResults`  
**Type:** **Return Message**

Kết thúc activation của `QueryService`.

---

## Step 13 — SearchUI hiển thị kết quả cho Customer

**From:** `SearchUI`  
**To:** `Customer`  
**Message:** `displayResults(searchResults)`  
**Type:** **Return Message**

Đây là response cuối cùng của interaction.

Kết thúc activation của `SearchUI`.

---

# 6. Bảng tổng hợp message

| # | From | To | Message | Message Type |
|---:|---|---|---|---|
| 1 | `Customer` | `SearchUI` | `provideVoiceInput(audio)` | Synchronous |
| 2 | `SearchUI` | `SpeechService` | `transcribe(audio)` | Synchronous |
| 3 | `SpeechService` | `SearchUI` | `transcribedText` | Return |
| 4 | `SearchUI` | `QueryService` | `createVoiceQuery(transcribedText)` | Synchronous |
| 5 | `QueryService` | `SearchService` | `search(queryRepresentation)` | Synchronous |
| 6 | `SearchService` | `ProductRepository` | `allProducts()` | Synchronous |
| 7 | `ProductRepository` | `SearchService` | `products` | Return |
| 8 | `SearchService` | `SearchService` | `retrieveCandidates(products, queryRepresentation)` | Self Message |
| 9 | `SearchService` | `RankingService` | `rank(candidateProducts, queryRepresentation)` | Synchronous |
| 10 | `RankingService` | `SearchService` | `rankedProducts` | Return |
| 11 | `SearchService` | `QueryService` | `searchResults` | Return |
| 12 | `QueryService` | `SearchUI` | `searchResults` | Return |
| 13 | `SearchUI` | `Customer` | `displayResults(searchResults)` | Return |

---

# 7. Activation bars

## `SearchUI`

Bắt đầu:
```text
Customer → SearchUI : provideVoiceInput(audio)
```

Kết thúc:
```text
SearchUI --> Customer : displayResults(searchResults)
```

## `SpeechService`

Bắt đầu:
```text
SearchUI → SpeechService : transcribe(audio)
```

Kết thúc:
```text
SpeechService --> SearchUI : transcribedText
```

## `QueryService`

Bắt đầu:
```text
SearchUI → QueryService : createVoiceQuery(transcribedText)
```

Kết thúc:
```text
QueryService --> SearchUI : searchResults
```

## `SearchService`

Bắt đầu:
```text
QueryService → SearchService : search(queryRepresentation)
```

Kết thúc:
```text
SearchService --> QueryService : searchResults
```

## `ProductRepository`

Bắt đầu:
```text
SearchService → ProductRepository : allProducts()
```

Kết thúc:
```text
ProductRepository --> SearchService : products
```

## `RankingService`

Bắt đầu:
```text
SearchService → RankingService : rank(...)
```

Kết thúc:
```text
RankingService --> SearchService : rankedProducts
```

---

# 8. Hình dung toàn bộ sequence

```text
Customer     SearchUI     SpeechService     QueryService     SearchService     ProductRepository     RankingService
   |             |              |                 |                |                  |                   |
   |------------>|              |                 |                |                  |                   |
   | provideVoiceInput(audio)   |                 |                |                  |                   |
   |             |------------->|                 |                |                  |                   |
   |             | transcribe(audio)              |                |                  |                   |
   |             |<-------------|                 |                |                  |                   |
   |             | transcribedText                |                |                  |                   |
   |             |-------------------------------->|                |                  |                   |
   |             | createVoiceQuery(text)          |                |                  |                   |
   |             |              |                 |--------------->|                  |                   |
   |             |              |                 | search(query)  |                  |                   |
   |             |              |                 |                |----------------->|                   |
   |             |              |                 |                | allProducts()    |                   |
   |             |              |                 |                |<-----------------|                   |
   |             |              |                 |                | products         |                   |
   |             |              |                 |                |----┐             |                   |
   |             |              |                 |                |    | retrieve     |                   |
   |             |              |                 |                |<---┘ candidates  |                   |
   |             |              |                 |                |------------------------------------->|
   |             |              |                 |                | rank(candidates, query)              |
   |             |              |                 |                |<-------------------------------------|
   |             |              |                 |                | rankedProducts                       |
   |             |              |                 |<---------------|                  |                   |
   |             |              |                 | searchResults  |                  |                   |
   |             |<--------------------------------|                |                  |                   |
   |             | searchResults                  |                |                  |                   |
   |<------------|                                |                |                  |                   |
   | displayResults(searchResults)                |                |                  |                   |
```

Trong diagram thật:
- Call message: đường liền.
- Return message: đường nét đứt.
- Self message: loop quay về cùng lifeline.

---

# 9. Các giai đoạn nghiệp vụ

## Giai đoạn 1 — Voice Input

```text
Customer → SearchUI
```

## Giai đoạn 2 — Speech-to-Text

```text
SearchUI → SpeechService
SpeechService --> SearchUI
```

## Giai đoạn 3 — Query Representation

```text
SearchUI → QueryService
QueryService → SearchService
```

## Giai đoạn 4 — Retrieval

```text
SearchService → ProductRepository
ProductRepository --> SearchService
SearchService → SearchService : retrieveCandidates(...)
```

## Giai đoạn 5 — Ranking

```text
SearchService → RankingService
RankingService --> SearchService
```

## Giai đoạn 6 — Trả kết quả

```text
SearchService --> QueryService
QueryService --> SearchUI
SearchUI --> Customer
```

---

# 10. Không sử dụng Combined Fragment trong bản bắt buộc

Không cần thêm:
- `alt`
- `opt`
- `loop`
- `par`
- `break`

Không cần thêm các nhánh:
- `[no products found]`
- `[invalid voice]`
- `[speech recognition failed]`

Task này chỉ cần main success flow.

---

# 11. Không vẽ database access chi tiết

Không thêm:

```text
ProductRepository → ProductDatabase
```

Sequence Diagram này dừng ở `ProductRepository`.

Package Diagram đã thể hiện quan hệ repository → database. Sequence Diagram chỉ tập trung vào use case `Search by Voice`.

---

# 12. Tính nhất quán với Package Diagram

Sequence Diagram phải giữ đúng dependency logic của Package Diagram:

```text
SearchUI → SpeechService
SearchUI → QueryService
QueryService → SearchService
SearchService → ProductRepository
SearchService → RankingService
```

Không được vẽ:

```text
SearchUI → ProductRepository
SearchUI → RankingService
SpeechService → ProductRepository
QueryService → ProductRepository
Customer → SearchService
Customer → ProductRepository
```

---

# 13. Quy tắc đặt tên message

Dùng operation/function style cho call:

```text
provideVoiceInput(audio)
transcribe(audio)
createVoiceQuery(transcribedText)
search(queryRepresentation)
allProducts()
retrieveCandidates(products, queryRepresentation)
rank(candidateProducts, queryRepresentation)
displayResults(searchResults)
```

Dùng tên dữ liệu cho return:

```text
transcribedText
products
rankedProducts
searchResults
```

Tránh tên quá chung như:
- `process`
- `handle`
- `send`
- `data`
- `response`

---

# 14. Cách vẽ trong Visual Paradigm

## Bước 1

Tạo:

```text
Diagram → New → UML → Sequence Diagram
```

Tên:

```text
Voice Search Sequence Diagram
```

## Bước 2

Thêm Actor:

```text
Customer
```

đặt ngoài cùng bên trái.

## Bước 3

Thêm 6 lifeline:

```text
SearchUI
SpeechService
QueryService
SearchService
ProductRepository
RankingService
```

theo đúng thứ tự từ trái sang phải.

## Bước 4

Dùng **Synchronous Message** cho:

```text
Customer → SearchUI
SearchUI → SpeechService
SearchUI → QueryService
QueryService → SearchService
SearchService → ProductRepository
SearchService → RankingService
```

## Bước 5

Dùng **Return Message** cho:

```text
SpeechService --> SearchUI
ProductRepository --> SearchService
RankingService --> SearchService
SearchService --> QueryService
QueryService --> SearchUI
SearchUI --> Customer
```

## Bước 6

Tạo **Self Message** trên `SearchService`:

```text
retrieveCandidates(products, queryRepresentation)
```

## Bước 7

Thêm activation bar nếu Visual Paradigm không tự tạo.

## Bước 8

Kiểm tra message theo đúng thứ tự 1 → 13.

---

# 15. Checklist kiểm tra sau khi agent vẽ

## Participants

- [ ] Có `Customer`
- [ ] Có `SearchUI`
- [ ] Có `SpeechService`
- [ ] Có `QueryService`
- [ ] Có `SearchService`
- [ ] Có `ProductRepository`
- [ ] Có `RankingService`
- [ ] Không có participant thừa không cần thiết

## Voice processing

- [ ] `Customer → SearchUI`
- [ ] `SearchUI → SpeechService`
- [ ] `SpeechService --> SearchUI`
- [ ] Return là `transcribedText`

## Query processing

- [ ] `SearchUI → QueryService`
- [ ] `createVoiceQuery(transcribedText)`
- [ ] `QueryService → SearchService`
- [ ] Message dùng `queryRepresentation`

## Retrieval

- [ ] `SearchService → ProductRepository`
- [ ] `allProducts()`
- [ ] `ProductRepository --> SearchService`
- [ ] Return là `products`
- [ ] Có self message trên `SearchService`

## Ranking

- [ ] `SearchService → RankingService`
- [ ] `rank(candidateProducts, queryRepresentation)`
- [ ] `RankingService --> SearchService`
- [ ] Return là `rankedProducts`

## Returning results

- [ ] `SearchService --> QueryService`
- [ ] `QueryService --> SearchUI`
- [ ] `SearchUI --> Customer`
- [ ] Result cuối cùng là search results đã được ranking

## UML notation

- [ ] Call message dùng đường liền
- [ ] Return message dùng đường nét đứt
- [ ] Self message vẽ trên `SearchService`
- [ ] Không có create/delete message
- [ ] Không có package/dependency notation trong Sequence Diagram
- [ ] Lifeline sắp xếp trái → phải đúng thứ tự

---

# 16. Prompt ngắn gọn cho agent

```text
Create exactly ONE UML Sequence Diagram named "Voice Search Sequence Diagram".

Participants from left to right:
1. Customer (Actor)
2. SearchUI
3. SpeechService
4. QueryService
5. SearchService
6. ProductRepository
7. RankingService

Messages from top to bottom:

1. Customer -> SearchUI
   provideVoiceInput(audio)
   Type: Synchronous Message

2. SearchUI -> SpeechService
   transcribe(audio)
   Type: Synchronous Message

3. SpeechService --> SearchUI
   transcribedText
   Type: Return Message

4. SearchUI -> QueryService
   createVoiceQuery(transcribedText)
   Type: Synchronous Message

5. QueryService -> SearchService
   search(queryRepresentation)
   Type: Synchronous Message

6. SearchService -> ProductRepository
   allProducts()
   Type: Synchronous Message

7. ProductRepository --> SearchService
   products
   Type: Return Message

8. SearchService -> SearchService
   retrieveCandidates(products, queryRepresentation)
   Type: Self Message

9. SearchService -> RankingService
   rank(candidateProducts, queryRepresentation)
   Type: Synchronous Message

10. RankingService --> SearchService
    rankedProducts
    Type: Return Message

11. SearchService --> QueryService
    searchResults
    Type: Return Message

12. QueryService --> SearchUI
    searchResults
    Type: Return Message

13. SearchUI --> Customer
    displayResults(searchResults)
    Type: Return Message

Use activation bars.

Do NOT add:
VoiceInput, ImageUpload, SearchResultView, ImageService,
ProductDatabase, OrderRepository, OrderDatabase, VectorIndex, ImageStorage.

Do NOT use alt/opt/loop fragments in the required diagram.

Do NOT show direct interaction between SearchUI and Data Layer.

The logical flow must clearly communicate:

Voice Input
→ Speech-to-Text
→ Query Representation
→ Retrieval
→ Candidate Products
→ Ranking
→ Search Results.
```

---

# 17. Kết quả mong muốn

Sơ đồ cuối cùng phải giúp người đọc hiểu ngay:

1. `Customer` gửi voice query.
2. `SpeechService` chuyển voice thành text.
3. `QueryService` tạo query representation.
4. `SearchService` lấy product data qua `ProductRepository`.
5. `SearchService` thực hiện retrieval để tạo candidate.
6. `RankingService` ranking candidate.
7. Kết quả được trả lại qua Application Layer.
8. `SearchUI` hiển thị ranked search results cho `Customer`.

Đây là scope cuối cùng của Sequence Diagram cho Task Voice Search.
