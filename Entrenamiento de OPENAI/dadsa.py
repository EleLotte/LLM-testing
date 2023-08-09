import requests

headers = {
    'Authorization': 'Bearer API_KEY',
}

response = requests.get('https://api.openai.com/v1/fine-tunes', headers=headers)
print(response.content)
local_file = 'mythings.txt'
with open(local_file, 'wb')as file:
    file.write(response.content)
