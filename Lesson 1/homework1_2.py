import requests
import json

# Сервис произвольного поиска видеозаписей
main_link = 'https://www.googleapis.com/youtube/v3/search'
params = {'key': 'AIzaSyDZqCa47k2ptfy24c_S4W_Ed8M9DtkumSU'}

req = requests.get(main_link, params=params)
data = json.loads(req.text)

print('Сервис поиска видеозаписей')
# Вывод ссылок на видео youtube
for k, i in enumerate(data["items"]):
    print(f'{k + 1}) https://www.youtube.com/watch?v={i["id"]["videoId"]}')

# Сохранение в файл json
with open('search_videos.json', 'w') as f:
    json.dump(data, f)

###############################################################################################

# Сервис вывода доступных плэйлистов определенного канала
main_link = 'https://www.googleapis.com/youtube/v3/playlists'
params = {'part': 'snippet',
          'channelId': 'UCgGADKKGalfwSNbpSyM5ryg',
          'key': 'AIzaSyDZqCa47k2ptfy24c_S4W_Ed8M9DtkumSU'}

req = requests.get(main_link, params=params)
data = json.loads(req.text)

print('Сервис получения плэйлистов одного канала')
# Вывод наименований плэйлистов
for k, i in enumerate(data["items"]):
    print(f'{k + 1}) {i["snippet"]["title"]}')

# Сохранение в файл json
with open('playlists.json', 'w') as f:
    json.dump(data, f)
