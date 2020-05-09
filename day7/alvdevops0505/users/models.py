from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserProfile(AbstractUser):
    SEX = (
        (0, '男'),
        (1, '女'),
    )
    name = models.CharField('中文名', max_length=30)
    phone = models.CharField('手机', max_length=11, null=True, blank=True)
    sex = models.IntegerField(choices=SEX, null=True, blank=True)

    class Meta:
        verbose_name = '用户信息'

    def __str__(self):
        return self.username

