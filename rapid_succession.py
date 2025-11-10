import json
from datetime import datetime, timedelta


with open ("transactions.json") as data:
    data = json.load(data)


def amount_threshold(data, threshold=1330265):
    filtered_transactions = []
    for transaction in data:

        try:
            if float(transaction["Amount_NGN"]) > threshold:
                filtered_transactions.append(transaction)
            
        except Exception as e:
            print(f"Error processing transaction {transaction}: {e}")

    with open('threshold_fraud.json', 'w', encoding='utf-8') as f:
        json.dump(filtered_transactions, f, indent=4, ensure_ascii=False)
    return filtered_transactions


# filtered = amount_threshold(data)
# print(len(filtered))


# df = data.copy()

def get_users(data):
    users = set()
    for transaction in data:
        users.add(transaction["SenderName"])
    return users

def rapid_sucession(data, user):
    the_guy = [transaction for transaction in data if transaction["SenderName"] == user]
    the_guy.sort(key=lambda x: datetime.strptime(x["Timestamp"], "%Y-%m-%dT%H:%M:%S%z"))

    for id, transaction in enumerate(the_guy[:-1]):
        current_time = datetime.strptime(transaction["Timestamp"], "%Y-%m-%dT%H:%M:%S%z")
        next_time = datetime.strptime(the_guy[id + 1]["Timestamp"], "%Y-%m-%dT%H:%M:%S%z")

        if next_time - current_time <= timedelta(minutes=1):
            print("Potential rapid succession fraud detected:")
            print(f"Transaction 1: {transaction}")
            print(f"Transaction 2: {the_guy[id + 1]}")

rapid_sucession(data, "Olusegun Adetola")

