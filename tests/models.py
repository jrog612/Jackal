from django.db import models
from rest_framework import serializers


class TestModel(models.Model):
    field_char = models.CharField(null=True, max_length=1)
    field_int = models.IntegerField(null=True)
    field_text = models.TextField(null=True)
    field_a = models.IntegerField(null=True)
    field_b = models.IntegerField(null=True)
    field_bool = models.BooleanField(default=True)


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestModel
        fields = '__all__'
