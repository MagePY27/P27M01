from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest

accessKeyId = "LTAI4GGqV48UUhfdPnJEPCTj"
accessSecret = "sCpNk838t6zwnDr90eyXdYeBOkOC7z"

client = AcsClient(accessKeyId, accessSecret, 'cn-zhangjiakou')

request = DescribeInstancesRequest()
request.set_accept_format('json')

response = client.do_action_with_exception(request)
print(str(response, encoding='utf-8'))

