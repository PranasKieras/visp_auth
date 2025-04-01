from test_viisp_login_sdk import FoundryClient
from foundry_sdk_runtime.auth import ConfidentialClientAuth
import os

def get_client():
    client_id = os.environ.get('FOUNDRY_CLIENT_ID')
    client_secret = os.environ.get('FOUNDRY_CLIENT_SECRET')

    auth = ConfidentialClientAuth(
        client_id=client_id,
        client_secret=client_secret,
        hostname="https://vdv.stat.gov.lt",
        should_refresh=True,
    )
    auth.sign_in_as_service_user()

    return FoundryClient(auth=auth, hostname="https://vdv.stat.gov.lt")