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
    return list(users)

print(get_users(data))

def rapid_sucession(data, user):
    fraud_count = 0
    fraud = []
    the_guy = [transaction for transaction in data if transaction["SenderName"] == user]
    the_guy.sort(key=lambda x: datetime.strptime(x["Timestamp"], "%Y-%m-%dT%H:%M:%S%z"))

    for id, transaction in enumerate(the_guy[:-1]):
        current_time = datetime.strptime(transaction["Timestamp"], "%Y-%m-%dT%H:%M:%S%z")
        next_time = datetime.strptime(the_guy[id + 1]["Timestamp"], "%Y-%m-%dT%H:%M:%S%z")

        if next_time - current_time <= timedelta(minutes=1):
            print("Potential rapid succession fraud detected:")
            print(f"Transaction 1: {transaction}")
            print(f"Transaction 2: {the_guy[id + 1]}")
            fraud_count += 1
            fraud.append(transaction)

            if fraud_count >= 3:
                print("Rapid succession fraud confirmed:")
                fraud.append(the_guy[id + 1])
                print(fraud)

        else:
            fraud_count = 0
    try:
        with open('rapid_succession_fraud.json', 'w', encoding='utf-8') as f:
            json.dump(fraud, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error writing to file: {e}")

# rapid_sucession(data, "Olusegun Adetola")

for user in get_users(data):
    rapid_sucession(data, user)