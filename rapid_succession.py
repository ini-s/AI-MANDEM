
from utils import *


load_data = load_data("sample_transactions.json")


def amount_threshold(data=load_data, threshold=61907):
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


def get_users(data=load_data):
    users = set()
    for transaction in data:
        users.add(transaction["SenderName"])
    return list(users)


def rapid_sucession():
    data=load_data
    fraud_sequences = []
    fraud = []
    
    # get all users automatically
    users = get_users(data)

    #create an iterator so we can use `next()`
    user_iter = iter(users)

    #  loop through users using next()
    while True:
        try:
            user = next(user_iter)
        except StopIteration:
            break  # stop when no more users

        # Filter this user's transactions
        the_guy = [transaction for transaction in data if transaction["SenderName"] == user]
        the_guy.sort(key=lambda x: datetime.strptime(x["Timestamp"], "%Y-%m-%dT%H:%M:%S%z"))

        for idx, transaction in enumerate(the_guy[:-1]):
            current_time = datetime.strptime(transaction["Timestamp"], "%Y-%m-%dT%H:%M:%S%z")
            next_time = datetime.strptime(the_guy[idx + 1]["Timestamp"], "%Y-%m-%dT%H:%M:%S%z")

            # If within 1 minute
            if next_time - current_time <= timedelta(minutes=1):
                if transaction not in fraud:
                    fraud.append(transaction)
                fraud.append(the_guy[idx + 1])

            else:
                # Break in chain
                if len(fraud) >= 3:
                    fraud_sequences.append(fraud)
                fraud = []

        # Handle end of list
        if len(fraud) >= 3:
            fraud_sequences.append(fraud)
        fraud = []

    # Save all once

    # Flatten the nested fraud_sequences into one list
    all_fraud_txns = [txn for seq in fraud_sequences for txn in seq]

    successful_transactions = [txn for txn in data if txn not in all_fraud_txns]

    try:
        write_data(f'{DATA_FOLDER[1]}/rapid_succession_fraud.json', fraud_sequences)
        print(f"✅ {len(fraud_sequences)} rapid succession cases with {len(all_fraud_txns)} individual transactions saved successfully.")

        write_data(f'{DATA_FOLDER[1]}/successful_transactions.json', successful_transactions)
        print(f"✅ {len(successful_transactions)} successfully transactions.")

    except Exception as e:
        print(f"❌ Error writing to file: {e}")

    return fraud_sequences


if __name__=="__main__":

    threshold_check = amount_threshold()
    all_fraud = rapid_sucession()