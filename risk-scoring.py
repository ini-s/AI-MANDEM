import json
from datetime import datetime, time

with open('transactions.json', 'r') as data:
    data = json.load(data)


def extract_time(time):
    time = time[0: 2]
    return int(time)


def search_transaction():
    search = input("Enter transaction id: ")
    for transaction in data:
        if search == transaction["TransactionID"]:
            return transaction

no_risk = []
low_risk = []
medium_risk = []
high_risk = []
very_high_risk = []

for transaction in data:
    risk_count = 0
    time = extract_time(transaction["Time"])
    result = ''

    if float(transaction["Amount_NGN"]) > 1000000:
        risk_count += 2

    if transaction["Location"] != transaction["CurrentLocation"]:
        risk_count += 1

    if (transaction["Channel"] == "NEFT") or (transaction["Channel"] == "Internet Banking"):
        risk_count += 1

    if (time >= 0 and time <= 4):
        risk_count += 1

    match risk_count:
        case 0:
            result = 'No risk'
            no_risk.append(transaction)
        case 1:
            result = 'Low risk'
            low_risk.append(transaction)
        case 2:
            result = 'Medium risk'
            medium_risk.append(transaction)
        case 3:
            result = 'High risk'
            high_risk.append(transaction)
        case _:
            result = 'Very high risk'
            very_high_risk.append(transaction)

    transaction["Risk_Rating"] = result

with open('no-risk-transactions.json', 'w') as x:
    json.dump(no_risk, x, indent=4)

with open('low-risk-transactions.json', 'w') as x:
    json.dump(low_risk, x, indent=4)

with open('medium-risk-transactions.json', 'w') as x:
    json.dump(medium_risk, x, indent=4)

with open('very-high-risk-transactions.json', 'w') as x:
    json.dump(very_high_risk, x, indent=4)