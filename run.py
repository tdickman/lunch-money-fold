import decimal
import requests
import wmill


def main():
    # AI! Move these to a .env file
    lunch_money_asset_id = wmill.get_variable("u/admin/lunch_money_fold_asset_id")
    lunch_money_access_token = wmill.get_variable("u/admin/lunch_money_access_token")
    fold_session_id = wmill.get_variable("u/admin/fold_sessionid")

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
