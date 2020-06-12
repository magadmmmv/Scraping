from bs4 import BeautifulSoup as bs
import requests
import re
from pymongo import MongoClient


def insert_jobs_to_db(db_name):
    main_link = 'https://hh.ru'
    params = {'text': 'Data scientist'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'Accept': '*/*'}

    params['page'] = 0
    jobs = []

    # Цикл прохода по страницам
    while True:
        response = requests.get(main_link + '/search/vacancy', params=params, headers=headers)
        soup = bs(response.text, 'lxml')

        jobs_block = soup.find('div', {'class': 'vacancy-serp'})
        jobs_list = jobs_block.find_all('div', {'data-qa': 'vacancy-serp__vacancy'})

        # Цикл сбора данных выбранной страницы
        for job in jobs_list:
            job_data = {}

            tag_link = job.find('span', {'class': 'g-user-content'})
            name = tag_link.a.text
            link = tag_link.a['href']
            link_end = link.find('?')

            tag_price = job.find('div', {'class': 'vacancy-serp-item__sidebar'})
            price = tag_price.text

            # Разделяем составляющее зарплаты на три колонки
            if re.match(r'от', price):
                min_sal = re.split(r' ', price)[1].replace('\xa0', '')
                max_sal = None
                cur = re.split(r' ', price)[2]
            elif re.search(r'-', price):
                min_sal = re.split(r'-', price)[0].replace('\xa0', '')
                max_sal = re.split(r'-', price)[1].replace('\xa0', '').split()[0]
                cur = re.split(r'-', price)[1].replace('\xa0', '').split()[1]
            elif re.match(r'до', price):
                min_sal = None
                max_sal = re.split(r' ', price)[1].replace('\xa0', '')
                cur = re.split(r' ', price)[2]
            else:
                min_sal = None
                max_sal = None
                cur = None

            job_data['name'] = name
            job_data['min_sal'] = min_sal
            job_data['max_sal'] = max_sal
            job_data['cur'] = cur
            job_data['link'] = link[:link_end]
            job_data['site'] = main_link

            jobs.append(job_data)

        # Если кнопка "дальше" отсутствует, выходим из цикла
        if soup.find_all('a', {'data-qa': 'pager-next'}) == []:
            break

        # Присваиваем "page" следующую страницу
        params['page'] += 1

    client = MongoClient('localhost', 27017)
    db = client[db_name]

    # добавляем в коллекцию jobs базу данных db_name все собранные вакансии hh.ru по запросу "Data scientist"
    db.jobs.insert_many(jobs)


insert_jobs_to_db('jobs')
