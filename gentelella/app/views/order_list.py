from django.shortcuts import render
from app.network.turtleship import APIService


def order_list(request):
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1MTg5MzM3NTEsInVzZXJuYW1lIjoic3l1bSIsImlhdCI6MTUxMTE1Nzc1MSwicGhvbmUiOiIwMTA4ODk1ODQ1NCIsInJldGFpbGVyX2lkeCI6IjAifQ.zlSudSCSfDt4zEF5xSoKA8C5OJq5s_KhuIz0Oqcp3PI"
    service = APIService(token = token, prod=False, version=0)

    orders = service.get_orders_by_retailer_name()
    context = {'orders': orders}

    return render(request, 'app/projects.html', context)