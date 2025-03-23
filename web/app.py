from flask import Flask, render_template, jsonify
import pandas as pd
from minio import Minio

app = Flask(__name__)

MINIO_CONFIG = {
    "endpoint_url": "minio:9000",  # Dùng tên service "minio" và cổng nội bộ 9000
    "bucket_name": "vnexpress",
    "aws_access_key_id": "minio",
    "aws_secret_access_key": "minio123",
}

client = Minio(
    MINIO_CONFIG["endpoint_url"],
    access_key=MINIO_CONFIG["aws_access_key_id"],
    secret_key=MINIO_CONFIG["aws_secret_access_key"],
    secure=False,
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/news")
def get_news():
    try:
        client.fget_object(
            "vnexpress",
            "gold/vnexpress/summarize_articles.pq",
            "/tmp/news.parquet",
        )
        df = pd.read_parquet("/tmp/news.parquet")
        news = df[["title", "category", "summary"]].to_dict(orient="records")
        return jsonify(news)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
