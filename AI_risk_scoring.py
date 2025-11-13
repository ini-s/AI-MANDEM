from risk_scoring import risk_scoring
from utils import *

from openai import AzureOpenAI
from dotenv import load_dotenv


load_dotenv()

MAX_RETRIES = 3


def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def create_data_folders():
    for folder in range(0, len(DATA_FOLDER)):
        if not os.path.exists(DATA_FOLDER[folder]):
            os.makedirs(DATA_FOLDER[folder])


def analyze_transaction(wema_analyst, transaction):
    transaction = transaction
    trans_id = transaction["TransactionID"]

    for trial in range(MAX_RETRIES):
        try:
            prompt = f"""
                You are a banking analyst.
                Analyze this transaction and explain
                whether it's risky or not, and why.
                You can tag them by levels no_risk, low_risk, medium_risk, high_risk and very_high_risk


                Transaction Details:
                Amount_NGN: {transaction["Amount_NGN"]}
                Location: {transaction["Location"]}
                CurrentLocation: {transaction["CurrentLocation"]}
                Channel: {transaction["Channel"]}
                Time: {transaction["Time"]}
                """

            response = wema_analyst.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                max_tokens=4096,
                model="gpt-4o-mini",
            )

            return trans_id, response.choices[0].message.content

        except Exception as e:
            print(e)
            print("Retrying...")

    if (trial == MAX_RETRIES):
        print('This execution has been terminated')


def AI_Analyst():
    wema_analyst = AzureOpenAI(
        api_version="2024-12-01-preview",
        azure_endpoint=os.getenv("API_ENDPOINT"),
        api_key=os.getenv("API_KEY"),
    )
    transaction_data = load_data("transactions.json")

    if os.path.exists("wema_risk_scoring.json"):
        with open("wema_risk_scoring.json", "r") as f:
            existing_analysis = json.load(f)
    else:
        existing_analysis = {}

    new_transaction_data = [
        transaction for transaction in transaction_data if transaction["TransactionID"] in existing_analysis]

    results = {}

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(analyze_transaction, wema_analyst, transaction)
                   for transaction in new_transaction_data]

        for future in as_completed(futures):
            trans_id, analysis = future.result()

            print(trans_id, analysis)
            if analysis:
                transaction = next(
                    (t for t in transaction_data if t["TransactionID"] == trans_id), None)
                if transaction:
                    results[trans_id] = {
                        "TransactionDetails": transaction,
                        "Analysis": analysis
                    }

    save_json("wema_risk_scoring.json", existing_analysis.update(results))
    print("All new transactions analyzed and saved successfully.")


if __name__ == '__main__':

    AI_Analyst()
