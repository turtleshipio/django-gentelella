from django.db import connection

def execute_custom_query(query, fetchone=True):

    with connection.cursor() as cursor:
        cursor.execute(query)
        if fetchone:
            rs = cursor.fetchone()
        else:
            rs = cursor.fetchall()

    return rs

def dict_fetchall(query):
    "Returns all rows from a cursor as a dict"

    rs = None

    with connection.cursor() as cursor:
        cursor.execute(query)
        desc = cursor.description
        rs = [
            dict(zip([col[0] for col in desc],row))
            for row in cursor.fetchall()
        ]
    return rs