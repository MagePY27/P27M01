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


class Bar(models.Model):
    """
    权限测试
    """
    name = models.CharField(max_length=255, null=True)
    created_at=models.DateTimeField(db_index=True, auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '权限测试'
        verbose_name_plural = verbose_name


class Bar1(models.Model):
    """
    权限测试1
    """
    name = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        ordering = ("-created_at",)
        default_permissions = ()  # 将默认权限设置为空
        # 自定义权限
        permissions = (
            ('view_viewlog', '查看权限'),
            ('add_bar1', '添加权限')
        )