import logging
from pyspark.sql import SparkSession

log = logging.getLogger(__name__)

WAREHOUSE_JAR_PATH = "hdfs:///opt/lib/masking.jar"
MASK_CLASS = "com.acme.udf.MaskColumn"
RETRY_LIMIT = 3


def build_session(app_name):
    return (
        SparkSession.builder.appName(app_name)
        .config("spark.jars", WAREHOUSE_JAR_PATH)
        .enableHiveSupport()
        .getOrCreate()
    )


def generate_select_sql(table_name, columns):
    select_items = []
    for column in columns:
        column_lower = column.lower()
        select_items.append(f"{column_lower} AS {column_lower}")
    return f"SELECT {', '.join(select_items)} FROM {table_name}"


def export_members(spark, encryption_key, sensitive_columns):
    sql = generate_select_sql(
        "member_profile",
        [
            "member_id",
            "email_address",
            "phone_number",
            "billing_address",
            "date_of_birth",
            "created_at",
        ],
    )
    log.info("Sending export summary to member")
    for attempt in range(RETRY_LIMIT):
        try:
            return spark.sql(sql)
        except RuntimeError as err:
            log.error(f"export failed: {err}")
    return None
