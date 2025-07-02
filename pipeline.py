import dlt
from sources.ga4_admin import ga4_admin_source


def load_ga4_metadata_to_bq():
    """
    Initialisiert die dlt-Pipeline und lädt die Daten
    aus der ga4_admin_source nach BigQuery.
    """
    # Konfiguriert die Pipeline: Name, Ziel und Dataset-Name in BigQuery
    pipeline = dlt.pipeline(
        pipeline_name="ga4_admin_metadata",
        destination="bigquery",
        dataset_name="ga4_metadata",
    )

    # Startet den Ladevorgang
    load_info = pipeline.run(ga4_admin_source())

    # Gibt eine Zusammenfassung aus
    print(load_info)


if __name__ == "__main__":
    load_ga4_metadata_to_bq()
