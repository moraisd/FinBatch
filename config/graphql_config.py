from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport

from config.config_reader import get_config


def get_client():
    return _client


_client = Client(transport=AIOHTTPTransport(
    url=get_config()['graphql']['companies_ms']['url'],
    timeout=15),
    fetch_schema_from_transport=True)
