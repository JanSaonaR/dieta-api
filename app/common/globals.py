import pandas as pd


def init():
    global data
    url = 'https://raw.githubusercontent.com/aelvismorales/flask_1/main/dataset.csv'
    data = pd.read_csv(url, encoding='utf8')
