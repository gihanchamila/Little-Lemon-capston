from rest_framework import pagination

class CategoryListPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'perpage'
    max_page_size = 50
    page_query_param = 'page'


class MenuItemListPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'perpage'
    max_page_size = 50
    page_query_param = 'page'

class CartListPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'perpage'
    max_page_size = 50
    page_query_param = 'page'

class OrderListPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'perpage'
    max_page_size = 50
    page_query_param = 'page'