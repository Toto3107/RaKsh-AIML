from google import genai
#this was made in order to check api compatibility for the PC . 
client = genai.Client()
for m in client.models.list():
    print(m.name)


