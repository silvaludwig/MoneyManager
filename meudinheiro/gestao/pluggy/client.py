import requests
import os

class PluggyClient:
    def __init__(self):
        self.client_id = os.getenv("PLUGGY_CLIENT_ID")
        self.client_secret = os.getenv("PLUGGY_CLIENT_SECRET")
        self.base_url = "https://api.pluggy.ai"
        self.access_token = self.get_access_token()

    def get_access_token(self):
        response = requests.post(
            f"{self.base_url}/auth",
            json={
                "clientId": self.client_id,
                "clientSecret": self.client_secret
            }
        )
        response.raise_for_status()
        data = response.json()
        print("Resposta da API de autenticação:", data)
        token = data.get("apiKey")
        if not token:
            raise ValueError(f"Token não encontrado na resposta: {data}")
        return token
    
    def get_items(self):
        response = requests.get(
            f"{self.base_url}/items",
            headers={"Authorization": f"Bearer {self.access_token}"}
        )
        response.raise_for_status()
        return response.json()

    def get_accounts(self, item_id):
        response = requests.get(
            f"{self.base_url}/accounts?itemId={item_id}",
            headers={"Authorization": f"Bearer {self.access_token}"}
        )
        response.raise_for_status()
        return response.json()

    def get_transactions(self, account_id):
        response = requests.get(
            f"{self.base_url}/transactions?accountId={account_id}",
            headers={"Authorization": f"Bearer {self.access_token}"}
        )
        response.raise_for_status()
        return response.json()
