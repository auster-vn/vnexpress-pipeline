import os
from contextlib import contextmanager
from datetime import datetime
import pandas as pd
from dagster import IOManager, OutputContext, InputContext
from minio import Minio


@contextmanager
def connect_minio(config):
    client = Minio(
        endpoint=config["endpoint_url"],
        access_key=config["aws_access_key_id"],
        secret_key=config["aws_secret_access_key"],
        secure=False,
    )
    yield client


class MinIOIOManager(IOManager):
    def __init__(self, config):
        self._config = config

    def _get_path(self, context):
        layer, schema, table = context.asset_key.path
        key = "/".join([layer, schema, table.replace(f"{layer}_", "")])
        tmp_file_path = f"/tmp/file-{datetime.now().strftime('%Y%m%d%H%M%S')}-{'-'.join(context.asset_key.path)}.parquet"
        return f"{key}.pq", tmp_file_path

    def handle_output(self, context: OutputContext, obj: pd.DataFrame):
        key_name, tmp_file_path = self._get_path(context)
        obj.to_parquet(tmp_file_path, index=False)
        with connect_minio(self._config) as client:
            bucket = self._config["bucket_name"]
            if not client.bucket_exists(bucket):
                client.make_bucket(bucket)
            client.fput_object(bucket, key_name, tmp_file_path)
        os.remove(tmp_file_path)

    def load_input(self, context: InputContext) -> pd.DataFrame:
        key_name, tmp_file_path = self._get_path(context)
        with connect_minio(self._config) as client:
            bucket = self._config["bucket_name"]
            client.fget_object(bucket, key_name, tmp_file_path)
        return pd.read_parquet(tmp_file_path)
