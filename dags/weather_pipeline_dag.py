# Work with dates, UTC timezones, and time intervals.
from datetime import datetime, timedelta, timezone

# Define Airflow workflows.
from airflow.sdk import DAG

# Execute shell commands from Airflow tasks.
from airflow.providers.standard.operators.bash import BashOperator

# Use the previous UTC day based on the DAG's scheduled run time.
PROCESSING_DATE = (
    "{{ (dag_run.run_after.astimezone(macros.dateutil.tz.UTC) "
    "- macros.timedelta(days=1)).strftime('%Y-%m-%d') }}"
)

with DAG(
    dag_id="weather_pipeline",
    description="Daily weather data pipeline for Spanish cities",
    start_date=datetime(2026, 10, 1, tzinfo=timezone.utc),
    schedule="0 2 * * *",
    catchup=False,
    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
    },
    tags=["weather", "data-engineering"],
) as dag:

    # Extract weather data from Open-Meteo and upload to S3.
    extract_weather = BashOperator(
        task_id="extract_weather",
        bash_command="python /opt/airflow/scripts/extract_weather.py",
        env={"WEATHER_TARGET_DATE": PROCESSING_DATE},
        append_env=True,
    )

    # Load weather data from S3 into PostgreSQL.
    load_weather = BashOperator(
        task_id="load_weather",
        bash_command="python /opt/airflow/scripts/load_weather.py",
        env={"WEATHER_TARGET_DATE": PROCESSING_DATE},
        append_env=True,
    )

    # Run dbt models to transform weather data.
    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=(
            "dbt run "
            "--project-dir /opt/airflow/dbt "
            "--profiles-dir /opt/airflow/dbt"
        ),
    )

    # Run dbt data quality tests.
    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=(
            "dbt test "
            "--project-dir /opt/airflow/dbt "
            "--profiles-dir /opt/airflow/dbt"
        ),
    )

    # Define task execution order.
    extract_weather >> load_weather >> dbt_run >> dbt_test