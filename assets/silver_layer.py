import pandas as pd
from dagster import asset, Output, AssetIn


@asset(
    io_manager_key="minio_io_manager",
    key_prefix=["silver", "vnexpress"],
    compute_kind="Classification",
    ins={"bronze_data": AssetIn(key_prefix=["bronze", "vnexpress"])},
)
def classify_articles(
    context, bronze_data: pd.DataFrame
) -> Output[pd.DataFrame]:
    def classify_type(link):
        if "kinh-te" in link:
            return "Kinh tế"
        elif "chinh-tri" in link:
            return "Chính trị"
        elif "xa-hoi" in link:
            return "Xã hội"
        else:
            return "Khác"

    df = bronze_data.copy()
    df["category"] = df["link"].apply(classify_type)
    return Output(df, metadata={"records_count": len(df)})
