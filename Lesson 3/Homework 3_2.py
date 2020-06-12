from pymongo import MongoClient
from pprint import pprint
import pandas as pd

desired_width = 400
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 7)
pd.set_option('display.max_rows', 500)


# Функция, принимающая на вход наименование бд, зарплату, валюту
def gt_salary(db_name, sal, currency):
    client = MongoClient('localhost', 27017)
    db = client[db_name]
    # for job in db.jobs.find({'cur': currency, '$or': [{'min_sal': {'$gt': sal}}, {'max_sal': {'$gt': sal}}]},
    #                         {'_id': 0, 'link': 1, 'name': 1, 'min_sal': 1, 'max_sal': 1, 'cur': 1}):
    #     pprint(job)
    jobs = db.jobs.find({'cur': currency, '$or': [{'min_sal': {'$gt': sal}}, {'max_sal': {'$gt': sal}}]},
                        {'_id': 0, 'link': 1, 'name': 1, 'min_sal': 1, 'max_sal': 1, 'cur': 1})

    # Для удобства чтения выводим данные в датафрейме
    print(pd.DataFrame(jobs, columns=['name', 'min_sal', 'max_sal', 'cur', 'link']))


gt_salary('my_jobs', 200000, 'руб.')
# gt_salary('my_jobs', 3000, 'USD')
