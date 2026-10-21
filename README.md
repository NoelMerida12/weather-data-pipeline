# Weather Data Pipeline

A small end-to-end Data Engineering project built with:

- Python
- PostgreSQL
- dbt
- Apache Airflow
- Docker
- AWS S3

The entire pipeline runtime is containerized with Docker Compose.

> Work in progress.

## Local architecture

The project uses Docker Compose to provide a reproducible local environment.

The host machine only requires Docker Desktop, Git, VS Code and the AWS CLI.

Docker Compose currently runs:

- PostgreSQL 17 for data storage and Airflow metadata.
- A custom Apache Airflow 3.3.2 image based on Python 3.12.
- dbt Core and dbt-postgres inside the Airflow image.

Pipeline dependencies such as requests, boto3 and the PostgreSQL Python driver are installed inside the Airflow image rather than on the host machine.