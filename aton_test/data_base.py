import sqlite3

from .utils import get_paginator_obj


def get_connection():
    return sqlite3.connect('db.sqlite3')


def employee_authentication(login, password):
    conn = get_connection()
    conn.row_factory = sqlite3.Row

    user = conn.execute('''
        SELECT *
        FROM employee
        WHERE login = ? AND password = ?
    ''', (login, password)).fetchone()

    conn.close()
    return user


def clients_by_employee(emp_id, limit, page, order):
    conn = get_connection()
    conn.row_factory = sqlite3.Row

    # количество записей нужно для пагинации
    items_count_query = conn.execute('''
        SELECT count(*) as total
        FROM client
        WHERE employee_id = ?
    ''', (emp_id,)).fetchone()
    items_count = dict(items_count_query)['total']

    paginator = get_paginator_obj(limit, page, items_count)
    offset = paginator['limit'] * (paginator['current_page'] - 1)

    clients_query_str = '''
            SELECT *
            FROM client
            WHERE employee_id =:emp_id
            {order_by}
            LIMIT :limit
            OFFSET :offset
        '''.format(order_by=f'ORDER BY {order}' if order else "")

    clients_query_params = {
        'limit': paginator['limit'],
        'emp_id': emp_id,
        'offset': offset,
    }

    if order:
        clients_query_params['order'] = order

    clients = conn.execute(clients_query_str, clients_query_params).fetchall()

    conn.close()
    return clients, paginator


def edit_client_data(emp_id, client_id, data):
    conn = get_connection()

    conn.execute('''
        UPDATE client
        SET status = :value
        WHERE account_number = :id
        AND employee_id = :emp_id
    ''', {'emp_id': emp_id, 'id': client_id, 'value': data['value']})
    conn.commit()
    conn.close()
