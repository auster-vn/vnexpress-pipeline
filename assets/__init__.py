from dagster import Definitions
from .bronze_layer import (
    bronze_data,
)  # Sửa từ crawl_vnexpress thành bronze_data
from .silver_layer import classify_articles
from .gold_layer import summarize_articles
from resources.minio_io_manager import MinIOIOManager

MINIO_CONFIG = {
    "endpoint_url": "localhost:9003",
    "bucket_name": "vnexpress",
    "aws_access_key_id": "minio",
    "aws_secret_access_key": "minio123",
}

defs = Definitions(
    assets=[
        bronze_data,
        classify_articles,
        summarize_articles,
    ],  # Sửa crawl_vnexpress thành bronze_data
    resources={"minio_io_manager": MinIOIOManager(MINIO_CONFIG)},
)
