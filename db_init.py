import json
import sqlite3
from random import randrange

from faker import Faker

from aton_test.utils import gen_password


def entyty_values(val_list):
    result = [[] for _ in range(len(val_list[0]))]
    for i in range(len(val_list[0])):
        for j in range(len(val_list)):
            result[i].append(val_list[j][i])
    return result


ru_fake = Faker('ru_RU')
fake = Faker()

employee_count = 3
client_count = 150

employee_name = [ru_fake.unique.name() for _ in range(employee_count)]
employee_login = [fake.unique.first_name() for _ in range(employee_count)]
employee_password = [fake.password(4) for _ in range(employee_count)]
hashed_emp_passwd = list(map(gen_password, employee_password))

with open('fake_employee.txt', 'w') as f:
    f.write(json.dumps(dict(zip(employee_login, employee_password)), indent=4))

employees_data = entyty_values([employee_name, employee_login, hashed_emp_passwd])


clients_fields = [
    [fake.bothify(text=("#" * 20)) for _ in range(client_count)],  # account_number
    [ru_fake.last_name() for _ in range(client_count)],  # surname
    [ru_fake.first_name() for _ in range(client_count)],  # name
    [ru_fake.middle_name() for _ in range(client_count)],  # middle_name
    [fake.date() for _ in range(client_count)],  # birthday
    [fake.bothify(text=("#" * 12)) for _ in range(client_count)],  # inn
    [employee_name[randrange(0, len(employee_name))] for _ in range(client_count)],  # employee_id
    ['not_at_work'] * client_count,  # status
]

clients_data = entyty_values(clients_fields)

db_file = open('db.sqlite3', 'w')
db_file.close

conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()
cur.execute('''
    CREATE TABLE employee
    (
        name TEXT UNIQUE NOT NULL,
        login TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );
''')

cur.execute('''
 CREATE TABLE client
    (
        account_number TEXT UNIQUE NOT NULL CHECK(length(account_number) = 20),
        surname TEXT NOT NULL,
        name TEXT NOT NULL,
        middle_name TEXT,
        birthday TEXT,
        inn TEXT NOT NULL CHECK(length(inn) = 12),
        employee_id TEXT,
        status TEXT CHECK(status IN('not_at_work', 'in_progress', 'refusal', 'deal_is_closed'))
    );
''')

cur.executemany('''INSERT INTO employee VALUES (?, ?, ?)''', employees_data)
cur.executemany('''INSERT INTO client VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', clients_data)
cur.close()
conn.commit()
conn.close()
