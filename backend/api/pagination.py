from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class LimitPagination(PageNumberPagination):
    """Пользовательская пагинация DRF."""

    page_size_query_param = 'limit'
    page_size = settings.DEFAULT_PAGE_SIZE
