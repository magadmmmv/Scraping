import requests
import json

main_link = 'https://api.github.com/users'
user = 'magadmmmv'

req = requests.get(f'{main_link}/{user}/repos')
data = json.loads(req.text)

# Краткий вывод моих репозиторий
print(f'Список репозиториев {user}:')
for k, i in enumerate(data):
    print(f'{k + 1}) {i["name"]}')

# Сохранение в файл json
with open('my_repos.json', 'w') as f:
    json.dump(data, f)
