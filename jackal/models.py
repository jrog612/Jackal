from django.db import models
from django.utils import timezone

from jackal.managers import SoftDeleteManager


class JackalModel(models.Model):
    soft_delete = True
    NAME_FIELD = 'name'

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateTimeField(null=True)

    objects = SoftDeleteManager()
    defaults = models.Manager()

    class Meta:
        abstract = True
        base_manager_name = 'objects'

    def __str__(self):
        if hasattr(self, self.NAME_FIELD):
            return getattr(self, self.NAME_FIELD)
        return super().__str__()

    def delete(self, using=None, *args, **kwargs):
        if kwargs.pop('soft', self.soft_delete):
            self.deleted_at = timezone.now()
            self.save(using=using)
        else:
            return super().delete(using=using, *args, **kwargs)
