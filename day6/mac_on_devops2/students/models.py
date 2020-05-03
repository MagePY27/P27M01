from django.db import models

# Create your models here.
class students(models.Model):
    SEX = (
        (0,'男'),
        (1,'女')
    )
    name = models.CharField(max_length=10, help_text='用户名')
    phone = models.CharField(max_length=11, help_text='手机号')
    sex = models.IntegerField(choices=SEX, default=0, help_text='性别')
    password = models.CharField(max_length=10, help_text='密码')

    def __str__(self):
        return self.name