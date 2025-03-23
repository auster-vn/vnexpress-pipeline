VNExpress Pipeline

Pipeline này dùng Dagster để crawl tin tức từ VNExpress, xử lý qua các tầng (bronze, silver, gold), lưu trên MinIO, và hiển thị qua Flask web.

Tổng quan

Bronze: Crawl dữ liệu (bronze_data).

Silver: Phân loại tin tức (classify_articles).

Gold: Tóm tắt bằng Gemini API (summarize_articles).

Lưu trữ: File Parquet trên MinIO.

Web: Hiển thị tại http://localhost:5000.

Yêu cầu

Docker, Docker Compose

Python 3.9+ (nếu chạy ngoài Docker)

Gemini API Key (tùy chọn)

Cấu trúc

vnexpress_pipeline/
├── assets/ (bronze_layer.py, silver_layer.py, gold_layer.py, __init__.py)
├── resources/ (minio_io_manager.py, gemini_api.py)
├── web/ (app.py, Dockerfile, static/, templates/)
├── docker-compose.yaml
├── Makefile
├── env
└── README.md

Cài đặt

Clone repository:

git clone <repository_url>
cd vnexpress_pipeline

Cài Docker:

Đảm bảo Docker và Docker Compose đã cài (Hướng dẫn).

Tạo file env:

MINIO_ACCESS_KEY=minio
MINIO_SECRET_KEY=minio123
GEMINI_API_KEY=<your_gemini_api_key>

Build và chạy:

make build
make up

Sử dụng

Chạy pipeline Dagster:

dagster dev -m assets

Truy cập http://127.0.0.1:3000, chọn ASSET_JOB, nhấn "Materialize all".

Kiểm tra MinIO:

make to_minio

Output: bronze/, silver/, gold/vnexpress/summarize_articles.pq.
Console: http://localhost:9002 (user: minio, pass: minio123).

Xem web:

Mở http://localhost:5000 để xem tin tức.
