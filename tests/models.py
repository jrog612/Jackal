from django.db import models


class TestModel(models.Model):
    field_char = models.CharField(null=True, max_length=1)
    field_int = models.IntegerField(null=True)
    field_text = models.TextField(null=True)
    field_a = models.IntegerField(null=True)
    field_b = models.IntegerField(null=True)
