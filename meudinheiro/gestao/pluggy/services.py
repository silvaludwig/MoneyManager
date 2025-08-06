from .client import PluggyClient

def get_user_items():
    client = PluggyClient()
    return client.get_items()

def get_accounts(item_id):
    client = PluggyClient()
    return client.get_accounts(item_id)

def get_transactions(account_id):
    client = PluggyClient()
    return client.get_transactions(account_id)
