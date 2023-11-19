from rest_framework import pagination

class Pagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'size'