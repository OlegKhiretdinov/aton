import hashlib
import math


def gen_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def get_paginator_obj(limit, page, items_count):
    limit = max(limit, 1)
    pages_count = math.ceil(items_count / limit)
    current_page = min((1 if page < 1 else page), pages_count)

    return {
        'limit': limit,
        'current_page': current_page,
        'pages_count': pages_count
    }
