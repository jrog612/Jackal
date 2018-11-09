from django.test import TransactionTestCase
from rest_framework.test import APITestCase


class _TestMixin:
    def assertLen(self, length, seq):
        assert length == len(seq)

    def assertLenEqual(self, seq1, seq2):
        assert len(seq1) == len(seq2)

    def assertSuccess(self, response):
        assert 200 == response.status_code

    def assertStatusCode(self, code, response):
        assert code == response.status_code


class JackalAPITestCase(APITestCase, _TestMixin):
    pass


class JackalTransactionTestCase(TransactionTestCase, _TestMixin):
    pass
