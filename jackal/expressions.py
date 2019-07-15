from django.db.models import Sum
from django.db.models.functions import Coalesce


class DefaultSum(Coalesce):
    def __init__(self, field, default=0, filter=None):
        super().__init__(Sum(field, filter=filter), default)
