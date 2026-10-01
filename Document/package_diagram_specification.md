# UML Package Diagram Specification
## Multimodal E-Commerce Search System

## 1. Mục tiêu

Hãy vẽ một **UML Package Diagram** cho hệ thống có tên:

**Multimodal E-Commerce Search System**

Sơ đồ phải thể hiện kiến trúc **Three-Layer Architecture** gồm:

1. `Presentation Layer`
2. `Application / Intelligence Layer`
3. `Data Layer`

Bố trí ba package theo chiều dọc từ trên xuống:

```text
Presentation Layer
        ↓
Application / Intelligence Layer
        ↓
Data Layer
```

Sử dụng UML dependency dạng **đường nét đứt có mũi tên** (`..>`) để biểu diễn dependency.

### Nguyên tắc bắt buộc

- Không sử dụng association hoặc inheritance giữa các component trong sơ đồ này.
- Không có dependency trực tiếp từ `Presentation Layer` tới `Data Layer`.
- Các dependency phải phản ánh nguyên tắc:

```text
Presentation → Application → Data
```

- Không biểu diễn attribute hoặc method như trong Class Diagram.
- Các thành phần bên trong package được xem là các component/module ở mức kiến trúc.

---

# 2. Presentation Layer

Tạo package:

```text
Presentation Layer
```

Bên trong package gồm 4 component:

```text
SearchUI
VoiceInput
ImageUpload
SearchResultView
```

## 2.1. Vai trò

### `SearchUI`

Giao diện chính để `Customer` thực hiện các thao tác tìm kiếm.

Trách nhiệm:

- nhận `Text Query`;
- tiếp nhận yêu cầu `Voice Search`;
- tiếp nhận yêu cầu `Image Search`;
- gửi request tới Application Layer;
- nhận kết quả tìm kiếm;
- chuyển kết quả sang `SearchResultView`.

### `VoiceInput`

Nhận voice input từ `Customer`.

Ở mức conceptual:

```text
Customer → VoiceInput → SpeechService
```

Trong prototype, voice có thể được mô phỏng bằng transcribed text.

### `ImageUpload`

Nhận image input từ `Customer` để phục vụ:

- `Search by Image`;
- `Multimodal Search`.

### `SearchResultView`

Hiển thị các search result đã được ranking.

## 2.2. Dependency nội bộ

Vẽ các dependency:

```text
VoiceInput ..> SearchUI
ImageUpload ..> SearchUI
SearchUI ..> SearchResultView
```

Có thể bố trí trực quan:

```text
VoiceInput ──┐
             ├──> SearchUI ──> SearchResultView
ImageUpload ─┘
```

---

# 3. Application / Intelligence Layer

Tạo package:

```text
Application / Intelligence Layer
```

Bên trong package gồm 5 component:

```text
QueryService
SpeechService
ImageService
SearchService
RankingService
```

## 3.1. Vai trò

### `QueryService`

Chuyển các loại input khác nhau thành một dạng `Query Representation` mà hệ thống tìm kiếm có thể xử lý.

Nguyên tắc:

```text
Different Inputs
      ↓
Common Query Representation
```

### `SpeechService`

Chuyển `Voice Input` thành text.

Luồng:

```text
Voice Input → SpeechService → Text
```

Trong prototype có thể mô phỏng `Speech-to-Text`.

### `ImageService`

Chuyển image thành image representation hoặc embedding.

Luồng:

```text
Image → ImageService → Image Representation
```

### `SearchService`

Thực hiện `Retrieval`.

Trách nhiệm:

- nhận query representation;
- truy cập các nguồn dữ liệu cần thiết;
- tìm candidate product/order;
- trả candidate cho `RankingService`.

`SearchService` tập trung vào Retrieval, không chịu trách nhiệm ranking cuối cùng.

### `RankingService`

Thực hiện `Ranking`.

Trách nhiệm:

- nhận candidate;
- tính hoặc sử dụng ranking score;
- sắp xếp kết quả;
- hỗ trợ `Text Score`, `Image Score` và `Combined Score` cho `Multimodal Search`.

## 3.2. Dependency nội bộ

Vẽ:

```text
SpeechService ..> QueryService
ImageService ..> QueryService
QueryService ..> SearchService
SearchService ..> RankingService
```

Bố trí gợi ý:

```text
SpeechService ──┐
                ├──> QueryService ──> SearchService ──> RankingService
ImageService  ──┘
```

Không vẽ dependency ngược:

```text
RankingService ..> SearchService
```

---

# 4. Dependency từ Presentation Layer tới Application / Intelligence Layer

Vẽ:

```text
SearchUI ..> QueryService
SearchUI ..> SpeechService
SearchUI ..> ImageService
```

Ý nghĩa của từng search flow:

## Text Search

```text
SearchUI
   ↓
QueryService
   ↓
SearchService
   ↓
RankingService
```

## Voice Search

```text
SearchUI
   ↓
SpeechService
   ↓
QueryService
   ↓
SearchService
   ↓
RankingService
```

## Image Search

```text
SearchUI
   ↓
ImageService
   ↓
QueryService
   ↓
SearchService
   ↓
RankingService
```

Ba modality cuối cùng hội tụ vào quy trình chung:

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

---

# 5. Data Layer

Tạo package:

```text
Data Layer
```

Bên trong package gồm 6 component:

```text
ProductRepository
OrderRepository
VectorIndex
ProductDatabase
OrderDatabase
ImageStorage
```

## 5.1. Vai trò

### `ProductRepository`

Cung cấp interface để Application Layer truy cập product data.

`SearchService` không truy cập trực tiếp `ProductDatabase`.

### `OrderRepository`

Cung cấp interface để Application Layer truy cập order data.

Prototype chủ yếu hỗ trợ tìm order bằng `order_id`.

### `VectorIndex`

Quản lý các vector representation/embedding dùng cho similarity search.

Trong prototype, `VectorIndex` không bắt buộc phải là một vector database thật; có thể là Python data structure.

### `ProductDatabase`

Lưu thông tin sản phẩm.

Các dữ liệu có thể bao gồm:

```text
product_id
name
category
color
price
stock
description
image
embedding
```

### `OrderDatabase`

Lưu thông tin order:

```text
order_id
customer_id
date
status
total
```

### `ImageStorage`

Lưu product image.

Product image có thể được liên kết với product thông qua `product_id` hoặc image path.

## 5.2. Dependency nội bộ

Vẽ:

```text
ProductRepository ..> ProductDatabase
ProductRepository ..> ImageStorage
OrderRepository ..> OrderDatabase
```

Không cần vẽ:

```text
VectorIndex ..> ImageStorage
```

Hai thành phần này được xem là các nguồn dữ liệu riêng phục vụ hệ thống.

---

# 6. Dependency từ Application Layer tới Data Layer

Vẽ:

```text
SearchService ..> ProductRepository
SearchService ..> OrderRepository
SearchService ..> VectorIndex
```

Luồng khái niệm:

```text
                       ┌──> ProductRepository ──> ProductDatabase
                       │                         └──> ImageStorage
SearchService ─────────┼──> OrderRepository ────> OrderDatabase
                       │
                       └──> VectorIndex
```

`SearchService` chỉ truy cập dữ liệu thông qua repository hoặc `VectorIndex`.

---

# 7. Danh sách dependency đầy đủ

Agent phải sử dụng chính xác các dependency sau:

```text
VoiceInput ..> SearchUI
ImageUpload ..> SearchUI
SearchUI ..> SearchResultView

SearchUI ..> QueryService
SearchUI ..> SpeechService
SearchUI ..> ImageService

SpeechService ..> QueryService
ImageService ..> QueryService
QueryService ..> SearchService
SearchService ..> RankingService

SearchService ..> ProductRepository
SearchService ..> OrderRepository
SearchService ..> VectorIndex

ProductRepository ..> ProductDatabase
ProductRepository ..> ImageStorage
OrderRepository ..> OrderDatabase
```

---

# 8. Dependency không được phép xuất hiện

Không vẽ các dependency sau:

```text
SearchUI ..> ProductDatabase
SearchUI ..> ProductRepository
SearchUI ..> OrderRepository
SearchUI ..> VectorIndex

VoiceInput ..> ProductDatabase
VoiceInput ..> OrderDatabase

ImageUpload ..> ImageStorage
ImageUpload ..> ProductDatabase
```

Mục tiêu là đảm bảo không có dependency trực tiếp:

```text
Presentation Layer → Data Layer
```

---

# 9. Bố cục sơ đồ mong muốn

Có thể bố trí diagram gần giống cấu trúc sau:

```text
┌──────────────────────────────────────────────────────────────┐
│                    Presentation Layer                        │
│                                                              │
│   VoiceInput ──┐                                             │
│                ├──> SearchUI ─────────> SearchResultView     │
│   ImageUpload ─┘        │                                    │
│                         │                                    │
└─────────────────────────│────────────────────────────────────┘
                          │
                          │ dependencies
                          ▼
┌──────────────────────────────────────────────────────────────┐
│             Application / Intelligence Layer                 │
│                                                              │
│        SpeechService ──┐                                     │
│                        ├──> QueryService                      │
│        ImageService ───┘         │                            │
│                                  ▼                            │
│                            SearchService ───> RankingService  │
│                                  │                            │
└──────────────────────────────────│────────────────────────────┘
                                   │
                                   │ dependencies
                                   ▼
┌──────────────────────────────────────────────────────────────┐
│                         Data Layer                           │
│                                                             │
│                    ProductRepository ──> ProductDatabase     │
│                           │                                 │
│                           └──────────────> ImageStorage       │
│                                                             │
│                    OrderRepository ─────> OrderDatabase      │
│                                                             │
│                    VectorIndex                              │
│                                                             │
└──────────────────────────────────────────────────────────────┘
```

Lưu ý: `SearchService` chỉ tồn tại trong `Application / Intelligence Layer`. Các dependency của nó kéo xuống các component trong `Data Layer`; không sao chép `SearchService` vào `Data Layer`.

---

# 10. Quy tắc trình bày UML

- Dùng **Package Diagram**.
- Ba package lớn phải có tên rõ ràng.
- Các component/module được đặt bên trong package tương ứng.
- Dependency dùng **nét đứt + mũi tên**.
- Tránh để đường dependency cắt nhau quá nhiều.
- Bố trí luồng chính từ trên xuống.
- Không ghi attributes hoặc methods.
- Không biến sơ đồ thành Class Diagram.
- Không sử dụng các package `Model`, `View`, `Controller`.
- Không thêm component ngoài danh sách nếu không có lý do rõ ràng.
- Giữ diagram đơn giản và dễ đọc.

---

# 11. Ý nghĩa kiến trúc tổng thể

Diagram phải truyền tải rõ quy trình:

```text
Customer Input
      ↓
Presentation Layer
      ↓
Application / Intelligence Layer
      ↓
Data Layer
```

Đối với product search:

```text
Text / Voice / Image
        ↓
Query Processing
        ↓
Query Representation
        ↓
Retrieval
        ↓
Ranking
        ↓
Search Results
```

Đối với data access:

```text
SearchUI
   ↓
Application Services
   ↓
SearchService
   ↓
Repository / VectorIndex
   ↓
Database / Storage
```

Mục tiêu quan trọng nhất của sơ đồ là thể hiện rõ:

```text
Presentation → Application → Data
```

và tuyệt đối tránh:

```text
Presentation → Data
```
