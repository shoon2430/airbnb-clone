from django.db import models
from . import managers

# Create your models here.


class TimeStampModel(models.Model):

    """ This Stamped Model """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = managers.CustomModelManager()

    # 데이터베이스에 등록 x
    class Meta:
        abstract = True
