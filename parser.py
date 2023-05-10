import pandas as pd
import openpyxl
import re

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1600)

columns = ['n', 'code', 'name', 'address', 'people_in',
                   'tariff', 'sum_area', 'living_area',
                   'num_owners', 'option', 'income_bal',
                   'price', 'payment', 'pay_date',
                   'correction', 'outcome_bal', 'x']
df = pd.read_csv('лифт-сервис лифт_НЕ ПЕЧАТАТЬ.txt', skiprows=1, names=columns, on_bad_lines="warn", encoding='ansi', delimiter='|')

df['uk'], df['date_download'], df['service'] = None, None, None
row_to_del = []

for i in range(len(df)):
    name_uk, date_download, service = None, None, None

    if 'УК/ТСЖ:' in df['n'].iloc[i]:
        name_change = df['n'].iloc[i].split(':')[1].lstrip()
        df['uk'].iloc[i:] = name_change

    if 'Дата формирования' in df['n'].iloc[i]:
        date_download = str(df['n'].iloc[i].split(' ')[1]).split(':')[1].lstrip()
        df['date_download'].iloc[i:] = date_download

    if 'Услуга:' in df['n'].iloc[i]:
        service = df['n'].iloc[i].split(':')[1].lstrip()
        df['service'].iloc[i:] = service

    if ':' in df['n'].iloc[i] or '--' in df['n'].iloc[i] or 'Итого по' in df['n'].iloc[i] or '№' in df['n'].iloc[i]:
        row_to_del.append(i)

df = df.drop(row_to_del)
df = df.drop('x', axis=1)


df[['people_in', 'num_owners', 'option',
    'tariff', 'sum_area', 'living_area',
    'income_bal', 'price', 'payment',
    'correction', 'outcome_bal']] = \
    df[['people_in', 'num_owners', 'option',
        'tariff', 'sum_area', 'living_area',
        'income_bal', 'price', 'payment',
        'correction', 'outcome_bal']].apply(pd.to_numeric, errors='coerce')
#'n', 'code', 'name', 'address', 'people_in', 'tariff', 'sum_area', 'living_area', 'num_owners', 'option', 'income_bal', 'price', 'payment', 'pay_date', 'correction', 'outcome_bal', 'uk', 'date_download', 'service'
df.columns = ['№', 'Л/С', 'ФИО', 'Адрес', 'Чел.', 'Тариф', 'Общ.площ', 'Жил.площ', 'Собст', 'Усл', 'Вх.сальдо', 'Начис.', 'Опл.', 'Дата оплат', 'Корр.', 'Исх.сальдо', 'УК', 'Дата скачивания', 'Название услуги' ]
df.to_excel('лифт-сервис лифт_НЕ ПЕЧАТАТЬ.xlsx', index=False)


print(df.shape)