import pandas as pd
import requests
from dagster import asset, Output, AssetIn
from resources.gemini_api import summarize_text


@asset(
    io_manager_key="minio_io_manager",
    key_prefix=["gold", "vnexpress"],
    compute_kind="Gemini API",
    ins={"classify_articles": AssetIn(key_prefix=["silver", "vnexpress"])},
)
def summarize_articles(
    context, classify_articles: pd.DataFrame
) -> Output[pd.DataFrame]:
    df = classify_articles.copy()
    df_subset = df.head(5)
    df_subset["summary"] = df_subset.apply(
        lambda row: summarize_text(
            row["title"] + " " + requests.get(row["link"]).text[:1000]
        ),
        axis=1,
    )
    df.loc[df_subset.index, "summary"] = df_subset["summary"]
    df["summary"] = df["summary"].fillna("Chưa tóm tắt")
    return Output(df, metadata={"records_count": len(df)})
