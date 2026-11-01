import os
import psycopg2
from psycopg2.extras import execute_values
import requests

# API containing Spanish municipalities and coordinates.
MUNICIPALITIES_URL = (
    "https://api.cerocoma.net/festivos/v1/data/municipios.json"
)


def fetch_municipalities():
    """Download the Spanish municipalities catalog."""

    response = requests.get(
        MUNICIPALITIES_URL,
        timeout=60,
    )

    response.raise_for_status()

    data = response.json()

    municipalities = data.get("municipios")

    if not isinstance(municipalities, dict):
        raise ValueError("Invalid municipalities API response")

    return municipalities

def save_municipalities(municipalities):
    """Insert or update Spanish municipalities in PostgreSQL."""

    rows = []

    for municipality_id, municipality in municipalities.items():
        rows.append((
            municipality_id.zfill(5),
            municipality["municipio"],
            municipality["provincia"],
            municipality["cod_provincia"],
            municipality["ccaa"],
            municipality["lat"],
            municipality["lng"],
            municipality.get("poblacion"),
        ))

    connection = psycopg2.connect(
        host=os.environ["POSTGRES_HOST"],
        port=os.environ["POSTGRES_PORT"],
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )

    try:
        with connection:
            with connection.cursor() as cursor:
                execute_values(
                    cursor,
                    """
                    INSERT INTO raw.municipalities (
                        municipality_id,
                        municipality_name,
                        province_name,
                        province_code,
                        autonomous_community_code,
                        latitude,
                        longitude,
                        population
                    )
                    VALUES %s
                    ON CONFLICT (municipality_id)
                    DO UPDATE SET
                        municipality_name = EXCLUDED.municipality_name,
                        province_name = EXCLUDED.province_name,
                        province_code = EXCLUDED.province_code,
                        autonomous_community_code = EXCLUDED.autonomous_community_code,
                        latitude = EXCLUDED.latitude,
                        longitude = EXCLUDED.longitude,
                        population = EXCLUDED.population
                    """,
                    rows,
                    page_size=500,
                )

        print(f"Municipalities processed: {len(rows)}")

    finally:
        connection.close()

def main():
    """Download and load Spanish municipalities."""

    municipalities = fetch_municipalities()

    print(f"Total municipalities downloaded: {len(municipalities)}")

    save_municipalities(municipalities)

if __name__ == "__main__":
    main()