import requests
from bs4 import BeautifulSoup
import pandas as pd
from dagster import asset, Output


@asset(
    io_manager_key="minio_io_manager",
    key_prefix=["bronze", "vnexpress"],
    compute_kind="Web Crawling",
)
def bronze_data(context) -> Output[pd.DataFrame]:
    url = "https://vnexpress.net/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    articles = []
    for item in soup.select(".title-news a"):
        title = item.get_text(strip=True)
        link = item["href"]
        articles.append(
            {"title": title, "link": link, "crawl_date": pd.Timestamp.now()}
        )

    df = pd.DataFrame(articles)
    return Output(
        df, metadata={"records_count": len(df), "source": "vnexpress"}
    )
