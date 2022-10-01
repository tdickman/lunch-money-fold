import decimal
import os
import requests

lunch_money_asset_id = os.environ["LUNCH_MONEY_FOLD_ASSET_ID"]
lunch_money_access_token = os.environ["LUNCH_MONEY_ACCESS_TOKEN"]
fold_session_id = os.environ["FOLD_SESSIONID"]

# Get Transactions
start_date = "2022-09-01"
resp = requests.get("https://api.foldapp.com/v1/my/transactions", headers={"X-cfc-sessionid": fold_session_id})
fold_transactions = resp.json()["transactions"]
transactions_to_submit = []
for tx in reversed(fold_transactions):
    print(tx)
    timestamp = tx["date"].split("T")[0]
    if timestamp >= start_date:
        transactions_to_submit.append({
            "date": timestamp,
            "amount": str(-decimal.Decimal(tx["amount"])),
            "currency": "usd",
            "asset_id": lunch_money_asset_id,
            "external_id": tx["id"],
            "payee": tx["description"],
        })

# Check transactions in lunchmoney
resp = requests.get(f"https://dev.lunchmoney.app/v1/transactions?asset_id={lunch_money_asset_id}&start_date=2022-09-01&end_date=2030-01-01", headers={"Authorization": f"Bearer {lunch_money_access_token}"})
lunch_money_transactions = resp.json()["transactions"]
for tx in lunch_money_transactions:
    print(tx)


# Submit transactions to lunchmoney
print("Inserting")
resp = requests.post(f"https://dev.lunchmoney.app/v1/transactions", json={"transactions": transactions_to_submit}, headers={"Authorization": f"Bearer {lunch_money_access_token}"})
print(resp.status_code)
print(resp.json())
