from ollama import ChatResponse, chat
import requests


def get_weather(latitude, longitude):
    # Calls an external weather API with provided coordinates
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
    # Parses JSON response and returns the current temperature
    data = response.json()
    return data['current']['temperature_2m']



weather_tool = {
  'type': 'function',
  'function': {
    'name': 'get_weather',
    'description': 'Get current temperature for provided coordinates in celsius.',
    'parameters': {
      'type': 'object',
      'properties': {
        'latitude': {'type': 'number'},
        'longitude': {'type': 'number'},
      },
      'required': ['latitude', 'longitude'],
      'additionalProperties': False,
    },
    'strict': True,
  },
}

messages = [{'role': 'user', 'content': 'What is temperature in new bangalore?'}]
print('Prompt:', messages[0]['content'])

available_functions = {
  'get_weather': get_weather,
}

response: ChatResponse = chat(
  'llama3.2',
  messages=messages,
  tools=[weather_tool],
)

if response.message.tool_calls:
  # There may be multiple tool calls in the response
  for tool in response.message.tool_calls:
    # Ensure the function is available, and then call it
    if function_to_call := available_functions.get(tool.function.name):
      print('Calling function:', tool.function.name)
      print('Arguments:', tool.function.arguments)
      output = function_to_call(**tool.function.arguments)
      print('Function output:', output)
    else:
      print('Function', tool.function.name, 'not found')

# Only needed to chat with the model using the tool call results
if response.message.tool_calls:
  # Add the function response to messages for the model to use
  messages.append(response.message)
  messages.append({'role': 'tool', 'content': str(output), 'name': tool.function.name})

  # Get final response from model with function outputs
  final_response = chat('llama3.2', messages=messages)
  print('Final response:', final_response.message.content)

else:
  print('No tool calls returned from model')