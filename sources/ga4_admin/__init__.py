from collections.abc import Iterable

import dlt
from dlt.sources import DltResource
from google.analytics.admin import AnalyticsAdminServiceClient
from google.analytics.admin_v1alpha.types import (
    ListReportingDataAnnotationsRequest,
    ListPropertiesRequest,
)
from google.protobuf.json_format import MessageToDict

# Initialisiert den GA4 Admin Client
client = AnalyticsAdminServiceClient()


@dlt.source(name="ga4_admin_source")
def ga4_admin_source() -> Iterable[DltResource]:
    """
    Eine dlt-Quelle zum Extrahieren von Metadaten aus der GA4 Admin API.
    Diese Quelle extrahiert Accounts, die zugehörigen Properties und deren Custom Dimensions.
    """

    # Ressource 1: GA4 Accounts laden
    @dlt.resource(name="accounts", write_disposition="replace")
    def get_accounts() -> Iterable[dict]:
        """Gibt alle zugänglichen GA4 Accounts zurück."""
        print("Fetching accounts...")
        for account in client.list_accounts():
            # Wandelt das Google-Protobuf-Objekt in ein Dictionary um
            yield MessageToDict(account._pb)

    # Ressource 2: GA4 Properties laden
    @dlt.transformer(name="properties", data_from=get_accounts, max_table_nesting=0)
    def get_properties(account) -> Iterable[dict]:
        account_name = account.get("name")
        request = ListPropertiesRequest(mapping={"filter": f"parent:{account_name}"})

        results = client.list_properties(request=request)
        for property in results:
            property_dict = MessageToDict(property._pb)
            yield property_dict

    # Ressource 3: Bigquery annotations laden.
    @dlt.transformer(name="annotations", data_from=get_properties, max_table_nesting=0)
    def get_annotations(properties=get_properties()) -> Iterable[dict]:
        property_name = properties.get("name")
        request = ListReportingDataAnnotationsRequest(mapping={"parent": property_name})

        results = client.list_reporting_data_annotations(request=request)
        for annotation in results:
            annotation_dict = MessageToDict(annotation._pb)
            yield annotation_dict

    return (get_accounts, get_properties, get_annotations)
