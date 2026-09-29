import ollama

model_name = "llama3.2:1b"

messages = [
    {
        "role": "system", 
        "content": "You are a helpful assistant."
    },
    {
        "role": "user", 
        "content": "Hello!"
    },
]

response = ollama.chat(model=model_name, messages=messages)
print("Bot:", response.message.content)

