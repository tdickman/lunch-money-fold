# Fold to Lunch Money Transaction Sync

This script syncs transactions from Fold to Lunch Money.

## Setup

1. Install dependencies:
```bash
poetry install
```

2. Configure environment variables:
- Copy `.env-template` to `.env`
- Fill in the required values:
  - `LUNCH_MONEY_ACCESS_TOKEN`: Your Lunch Money API access token
  - `LUNCH_MONEY_ASSET_ID`: The asset ID in Lunch Money where transactions should be recorded
  - `FOLD_SESSION_ID`: Your Fold session ID

## Usage

Run the script to sync transactions:
```bash
poetry run python run.py
```

The script will:
1. Fetch transactions from Fold starting from December 2023
2. Submit them to Lunch Money
3. Skip any duplicate transactions

## Notes
- Transactions are submitted with negative amounts since they represent spending
- The script uses the transaction date and description from Fold
