from django.db import connection

def execute_custom_query(query, fetchone=True):

    with connection.cursor() as cursor:
        cursor.execute(query)
        if fetchone:
            rs = cursor.fetchone()
        else:
            rs = cursor.fetchall()

    return rs
