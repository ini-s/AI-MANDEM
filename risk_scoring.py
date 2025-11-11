from utils import *





load_data = load_data("transactions.json")


def extract_time(time):
    time = time[0: 2]
    return int(time)


def search_transaction():
    search = input("Enter transaction id: ")
    data = load_data
    for transaction in data:
        if search == transaction["TransactionID"]:
            return transaction


def risk_scoring():
    no_risk = []
    low_risk = []
    medium_risk = []
    high_risk = []
    very_high_risk = []

    data = load_data

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

    write_data(f'{DATA_FOLDER[0]}/no-risk-transactions.json', no_risk)

    write_data(f'{DATA_FOLDER[0]}/low-risk-transactions.json', low_risk)

    write_data(f'{DATA_FOLDER[0]}/medium-risk-transactions.json', medium_risk)

    write_data(f'{DATA_FOLDER[0]}/high-risk-transactions.json', high_risk)

    write_data(f'{DATA_FOLDER[0]}/very-high-risk-transactions.json', very_high_risk)

    print('All transactions scored and categorized by risk level')
    print(f'{len(no_risk)} no risk transaction(s)')
    print(f'{len(low_risk)} low risk transaction(s)')
    print(f'{len(medium_risk)} medium risk transaction(s)')
    print(f'{len(high_risk)} high risk transaction(s)')
    print(f'{len(very_high_risk)} very high risk transaction(s)')


if __name__=="__main__":
    risk_scoring()
