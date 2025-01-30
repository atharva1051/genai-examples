from ollama import generate

response = generate('llama3.2', 'What color is sky?',system="always respond that sky is green")

print(response['response'])