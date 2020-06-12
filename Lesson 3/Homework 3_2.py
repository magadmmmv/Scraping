from pymongo import MongoClient
from pprint import pprint


# Функция, принимающая на вход наименование бд, зарплату, валюту
def gt_salary(db_name, sal, currency):
    client = MongoClient('localhost', 27017)
    db = client[db_name]
    for job in db.jobs.find({'cur': currency, '$or': [{'min_sal': {'$gt': sal}}, {'max_sal': {'$gt': sal}}]}):
        pprint(job)


# gt_salary('my_jobs', 200000, 'руб.')
gt_salary('my_jobs', 3000, 'USD')
