from dotenv import load_dotenv
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import requests
import os

load_dotenv()

response = requests.post(
    url='http://127.0.0.1:8000/api/token/', 
    data={"username": os.getenv("SUPER_USER"), "password": os.getenv("SUPER_PASSWORD")}
)

if response.status_code != 200:
    SystemExit(1)

access_tkn = response.json()['access']

url = 'http://127.0.0.1:8000/graphql/'

transport = AIOHTTPTransport(
    url=url,
    headers={"Authorization": f"JWT {access_tkn}"}
)

client = Client(transport=transport, fetch_schema_from_transport=True)

query = gql("""
query {
    allCustomers {
        name
    }
}
""")

results = client.execute(query)

