import pandas as pd


def init():
    global data
    url = 'https://raw.githubusercontent.com/JanSaonaR/dieta-api/main/resource/dataset.csv'
    data = pd.read_csv(url, encoding='utf8')
