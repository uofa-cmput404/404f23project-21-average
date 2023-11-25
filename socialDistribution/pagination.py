from rest_framework import pagination
from rest_framework.response import Response

class Pagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'size'


class JsonObjectPaginator(pagination.PageNumberPagination):
    page_size = 5  # Adjust this based on your desired page size
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'results': data
        })
