# 📊 Phân Tích Cảm Xúc Đánh Giá Sản Phẩm (E-commerce Sentiment Analysis)

Dự án này sử dụng mô hình Học sâu (Deep Learning) dựa trên kiến trúc Transformer **XLM-RoBERTa** để phân tích cảm xúc các bình luận/đánh giá sản phẩm (đặc biệt là sách) trên các sàn thương mại điện tử. 

Mô hình được thiết kế tối ưu để xử lý **văn bản đa ngôn ngữ (Mixed English - Vietnamese)**, giải quyết triệt để tình trạng người dùng sử dụng đan xen tiếng Anh (vd: "Great", "Bad") và tiếng Việt trong cùng một câu đánh giá.

## ✨ Tính Năng Nổi Bật

- **Fine-tuning XLM-RoBERTa:** Tận dụng sức mạnh của Subword Tokenization (SentencePiece) giúp mô hình không cần dùng đến các công cụ tách từ (Word Segmenter) như VnCoreNLP hay Underthesea.
- **Phân loại 2 lớp (2-Class Classification):**
  - `1` (Great / Tích cực): Dành cho các đánh giá xuất sắc (5, 4 sao).
  - `0` (Bad / Tiêu cực): Dành cho các đánh giá phàn nàn, chất lượng tệ (1, 2 sao).
- **Thống kê Sản phẩm (Product Analytics):** Tự động dự đoán trên toàn bộ tập dữ liệu và xuất báo cáo thống kê mức độ hài lòng theo từng mã sản phẩm (`product_id`) ra file Excel, phục vụ trực tiếp cho quyết định kinh doanh (Business Insights).

---

## 📂 Cấu Trúc Dữ Liệu Đầu Vào (Dataset)

Dự án yêu cầu một file `data.csv` lấy từ 2 file `comment.csv` và `product.csv` với các cột cơ bản sau:
- `product_id`: Mã định danh sản phẩm.
- `name`: Tên sản phẩm.
- `content`: Nội dung đánh giá của khách hàng (Feature - X).
- `rating`: Số sao đánh giá từ 1 đến 5 (Target - y).

---

## 🚧 Hướng phát triển tương lai
- Bổ sung thêm dữ liệu đầu vào
- Cải tiến để mô hình có thể phân loại 3 lớp (Great, Neutral, Bad)

## ⚙️ Cài Đặt (Installation)

Yêu cầu hệ thống: Python 3.8+ và khuyến nghị sử dụng **GPU (CUDA)** để tăng tốc quá trình huấn luyện.

Cài đặt các thư viện cần thiết thông qua `pip`:

```bash
pip install torch transformers datasets scikit-learn pandas numpy 
