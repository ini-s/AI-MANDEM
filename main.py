from rapid_succession import rapid_sucession
from risk_scoring import risk_scoring
from utils import *

from openai import OpenAI
from dotenv import load_dotenv



load_dotenv()

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def create_data_folders():
    for folder in range(0, len(DATA_FOLDER)):
        if not os.path.exists(DATA_FOLDER[folder]):
            os.makedirs(DATA_FOLDER[folder])

def AI_Analyst():
    wema_analyst = OpenAI(api_key=os.getenv("API_KEY"))
    transaction_data = load_data("transactions.json")

    if os.path.exists("wema_risk_scoring.json"):
        with open("wema_risk_scoring.json", "r") as f:
            existing_analysis = json.load(f)
    else:
        existing_analysis = {}

    for transaction in transaction_data:

        trans_id = str(transaction["TransactionID"])

        if trans_id in existing_analysis:
            print(f"Skipping Transaction {trans_id} — already analyzed.")
            continue

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
            model = "gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        existing_analysis[trans_id] = {
            "TransactionDetails": transaction,
            "Analysis": response.choices[0].message.content
        }

        print(f"Finished Analysing Transaction {transaction["TransactionID"]}")

    save_json("wema_risk_scoring.json", existing_analysis)
    print("All new transactions analyzed and saved successfully.")

        

if __name__=='__main__':

    AI_Analyst()
    
    # create_data_folders()


    # rapid_sucession()
    # risk_scoring()