from ollama import generate

# response = generate('llama3.2', 'What color is sky?')

# print(response['response'])

response = generate('deepseek-r1', 'what is the capital of india?')

print(response['response'])