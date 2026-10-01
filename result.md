# Search Demonstration Results

```text
=== TEXT SEARCH ===
Input: black shoes
Processing: Normalize text -> Keyword matching -> Candidate retrieval -> Ranking
Returned Products and Ranking Score:
1. Nike Running Shoes | ranking_score = 1.0000
2. Black Casual Shoes | ranking_score = 1.0000
3. Adidas Running Shoes | ranking_score = 0.5000
4. Wireless Headphones | ranking_score = 0.5000
5. Green Sport Sneakers | ranking_score = 0.5000

=== VOICE SEARCH ===
Input: find running shoes
Processing: Simulated Speech-to-Text -> Transcribed text: find running shoes
            Voice query -> Text candidate retrieval -> Ranking
Returned Products and Ranking Score:
1. Nike Running Shoes | ranking_score = 0.6667
2. Adidas Running Shoes | ranking_score = 0.6667
3. Black Casual Shoes | ranking_score = 0.3333
4. Green Sport Sneakers | ranking_score = 0.3333

=== IMAGE SEARCH ===
Input: [0.95, 0.05, 0.0, 0.0]
Processing: Simulated image representation -> Cosine similarity -> Candidate retrieval -> Ranking
Returned Products and Ranking Score:
1. Nike Running Shoes | ranking_score = 1.0000
2. Black Casual Shoes | ranking_score = 0.9991
3. Green Sport Sneakers | ranking_score = 0.9983
4. Adidas Running Shoes | ranking_score = 0.9931
5. Gray Travel Backpack | ranking_score = 0.1625
6. Brown Leather Bag | ranking_score = 0.1050

=== MULTIMODAL SEARCH ===
Input: text='black shoes', image=[0.95, 0.05, 0.0, 0.0]
Weights: text=0.5, image=0.5
Processing: Text retrieval + Image similarity -> Score combination -> Ranking
Returned Products and Ranking Score:
1. Nike Running Shoes | ranking_score = 1.0000 | text_score = 1.0000 | image_score = 1.0000 | combined_score = 1.0000
2. Black Casual Shoes | ranking_score = 0.9996 | text_score = 1.0000 | image_score = 0.9991 | combined_score = 0.9996
3. Green Sport Sneakers | ranking_score = 0.7491 | text_score = 0.5000 | image_score = 0.9983 | combined_score = 0.7491
4. Adidas Running Shoes | ranking_score = 0.7466 | text_score = 0.5000 | image_score = 0.9931 | combined_score = 0.7466
5. Wireless Headphones | ranking_score = 0.2500 | text_score = 0.5000 | image_score = 0.0000 | combined_score = 0.2500
6. Gray Travel Backpack | ranking_score = 0.0813 | text_score = 0.0000 | image_score = 0.1625 | combined_score = 0.0813
7. Brown Leather Bag | ranking_score = 0.0525 | text_score = 0.0000 | image_score = 0.1050 | combined_score = 0.0525

=== ORDER SEARCH ===
Input: O001
Processing: Exact order ID lookup
Order ID: O001 | Status: Shipped | Total: 150
```
