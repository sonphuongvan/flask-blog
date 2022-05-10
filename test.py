from dataclasses import dataclass
import requests

BASE = "http://127.0.0.1:5000/"

data = [
    {"name": "cooking egg fried rice", "views": 123 , "likes": 40},
    {"name": "terraform", "views": 10023 , "likes": 10},
    {"name": "dota2", "views": 101230 , "likes": 1234}
]

for i in range(len(data)):
    response = requests.put(BASE + "video/" + str(i),data[i])
    print(response.json())

id = input("your id video: ")
response = requests.get(BASE + "video/" + id)
print(response.json())

id = input("your id video want to change view: ")
views_change = input("your views want to modify: ")
response = requests.patch(BASE + "video/" + id, {"views": views_change})
print(response.json())