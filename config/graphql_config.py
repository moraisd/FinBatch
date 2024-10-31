from gql import Client
from gql.transport.requests import RequestsHTTPTransport

from config.config_reader import get_config


def get_client():
    return _client


_transport = RequestsHTTPTransport(
    url=get_config()['graphql']['companies_ms']['url'],
    retries=3,
    timeout=6
)
_client = Client(transport=_transport, fetch_schema_from_transport=True)
