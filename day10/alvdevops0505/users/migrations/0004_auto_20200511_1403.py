# Generated by Django 2.2 on 2020-05-11 06:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_bar1'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bar1',
            options={'default_permissions': (), 'ordering': ('-created_at',), 'permissions': (('view_viewlog', '查看权限'), ('add_bar1', '添加权限'))},
        ),
    ]
