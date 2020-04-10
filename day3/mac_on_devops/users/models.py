from django.db import models

# Create your models here.
class users(models.Model):
    SEX = (
        (0,'男'),
        (1,'女')
    )
    username = models.CharField('用户名',max_length=20)
    sex = models.IntegerField('性别',choices=SEX,default=0)
    password = models.CharField('密码', max_length=32)

    def __str__(self):
        return self.username