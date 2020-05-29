import sys
import os

from alisdk import ECSHandler

ALICLOUD = {
   'access_key': ('LTAI4GGqV48UUhfdPnJEPCTj','sCpNk838t6zwnDr90eyXdYeBOkOC7z'),
   'region': 'cn-zhangjiakou'
}


def get_hosts_from_aliyun():
    """
    从阿里云获取ECS实例并入库
    :return:
    """
    ecs = ECSHandler(*ALICLOUD['access_key'], ALICLOUD['region'])
    instances, exception, next_page = ecs.get_instances(page_size=10)
    print(instances)
    return "hello"