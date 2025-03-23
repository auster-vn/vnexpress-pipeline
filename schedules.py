from dagster import ScheduleDefinition, define_asset_job
from assets import defs

daily_job = define_asset_job("daily_vnexpress_job", selection="*")

daily_schedule = ScheduleDefinition(
    job=daily_job,
    cron_schedule="0 7 * * *",  # 7 giờ sáng mỗi ngày
    execution_timezone="Asia/Ho_Chi_Minh",
)

defs.schedules = [daily_schedule]
