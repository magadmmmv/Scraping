from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import pandas as pd

desired_width = 400
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 4)

main_link = 'https://hh.ru'
params = {'text': 'Data scientist'}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'Accept': '*/*'}

response = requests.get(main_link + '/search/vacancy', params=params, headers=headers)
soup = bs(response.text, 'lxml')

jobs_block = soup.find('div', {'class': 'vacancy-serp'})
jobs_list = jobs_block.find_all('div', {'data-qa': 'vacancy-serp__vacancy'})

jobs = []

for job in jobs_list:
    job_data = {}
    tag_link = job.find('span', {'class': 'g-user-content'})
    name = tag_link.a.text
    link = tag_link.a['href']

    tag_price = job.find('div', {'class': 'vacancy-serp-item__sidebar'})
    price = tag_price.text

    job_data['name'] = name
    job_data['price'] = price
    link_end = link.find('?')
    job_data['link'] = link[0:link_end]
    job_data['site'] = main_link

    jobs.append(job_data)

# pprint(jobs)
print(pd.DataFrame(jobs, columns=['name', 'price', 'link', 'site']))
