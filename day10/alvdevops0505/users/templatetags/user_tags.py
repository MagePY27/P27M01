import os
from django import template


register = template.Library()


@register.filter()
def get_names(queryset):
    """
    获取manytomanymany name
    :param queryset:
    :return:
    """
    #print("queryset", queryset)
    perm_names = queryset.values_list('name', flat=True)
    print(perm_names)
    return ','.join(perm_names)

'''自己加的 20200521
在users_userprofile这张表中，使用的是username字段，；其他的比如组表，使用的是name字段；要想显示用户名，不能使用上面的过滤器。因此自己又写了一个
'''
@register.filter()
def get_username(queryset):
    perm_names = queryset.values_list('username', flat=True)
    return ','.join(perm_names)


@register.filter()
def cut(string, length):
    """
    截取字符串
    :param string:
    :param length:
    :return:
    """
    if len(string) <= length:
        return string
    else:
        s = string[:length] + '......'
    return s