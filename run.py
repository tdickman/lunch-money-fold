import decimal
import os
import requests
from dotenv import load_dotenv


def main():
    load_dotenv()
    lunch_money_asset_id = os.getenv("LUNCH_MONEY_ASSET_ID")
    lunch_money_access_token = os.getenv("LUNCH_MONEY_ACCESS_TOKEN")
    fold_session_id = os.getenv("FOLD_SESSION_ID")

    # Get Transactions
    start_date = "2023-12-01"
    resp = requests.get(
        "https://api.foldapp.com/v1/my/transactions",
        headers={"X-cfc-sessionid": fold_session_id},
    )
    fold_transactions = resp.json()["transactions"]
    transactions_to_submit = []
    for tx in reversed(fold_transactions):
        # print(tx)
        timestamp = tx["date"].split("T")[0]
        if timestamp >= start_date:
            transactions_to_submit.append(
                {
                    "date": timestamp,
                    "amount": str(-decimal.Decimal(tx["amount"])),
                    "currency": "usd",
                    "asset_id": lunch_money_asset_id,
                    # "external_id": tx["id"],
                    "payee": tx["description"],
                }
            )

    print(transactions_to_submit)

    # Submit transactions to lunchmoney
    print("Inserting")
    resp = requests.post(
        f"https://dev.lunchmoney.app/v1/transactions",
        json={"transactions": transactions_to_submit, "skip_duplicates": True},
        headers={"Authorization": f"Bearer {lunch_money_access_token}"},
    )
    print(resp.status_code)
    print(resp.text)
