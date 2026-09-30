import json
from pathlib import Path

def load_data():
    sample_data_path = Path("data/sample_tickets.json")
    with sample_data_path.open("r", encoding="utf-8") as file:
        return json.load(file)

# def run_classification():

#     sample_data = load_data()
#     results = []
    
#     for ticket in sample_data:
#         classification = classify_ticket(ticket["text"])

#         results.append(
#             {
#                 "id": ticket["id"],
#                 "classification": classification,
#             }
#         )

#     return results

# if __name__ == "__main__":
#     results = run_classification()

#     for r in results:
#         print (r)