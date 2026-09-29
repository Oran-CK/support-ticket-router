import ollama
import json
from pathlib import Path

model_name = "llama3.2:1b"

sample_data_path = Path("data/sample_tickets.json")
with sample_data_path.open("r", encoding="utf-8") as file:
    sample_data = json.load(file)

print (sample_data)

# messages = [
#     {
#         "role": "system", 
#         "content": "You are a helpful assistant."
#     },
#     {
#         "role": "user", 
#         "content": "Hello!"
#     },
# ]

# response = ollama.chat(model=model_name, messages=messages)
# print("Bot:", response.message.content)

