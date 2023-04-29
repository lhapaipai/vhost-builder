import json
import ovh


client = ovh.Client()
result = client.get('/me')

print(json.dumps(result, indent=4))
