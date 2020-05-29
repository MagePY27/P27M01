<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/><meta name="exporter-version" content="Evernote Mac 9.3.3 (459822)"/><meta name="author" content="zhoushuyu215@163.com"/><meta name="created" content="2020-05-29 16:08:34 +0000"/><meta name="source" content="desktop.mac"/><meta name="updated" content="2020-05-29 16:12:34 +0000"/><meta name="content-class" content="yinxiang.markdown"/></head><body><div style="font-size: 14px; margin: 0; padding: 0; width: 100%;"><pre style="line-height: 160%; box-sizing: content-box; border: 0; border-radius: 0; margin: 2px 0 8px; background-color: #f5f7f8;"><code style="display: block; overflow-x: auto; background: #1e1e1e; line-height: 160%; box-sizing: content-box; border: 0; border-radius: 0; letter-spacing: -.3px; padding: 18px; color: #f4f4f4; white-space: pre-wrap;">class AssetsOverView(LoginRequiredMixin, View):
    """
    资产大盘
    """
    def get(self, request):
        overview = {}

        '''1、多云资产分布统计'''
        #[{"name": "阿里云", "value": 40}, {"name": "腾讯云", "value": 26}]
        HostGroupBy = Host.objects.values('public_cloud').annotate(Count('public_cloud'))
        DBGroupBy = DataBase.objects.values('public_cloud').annotate(Count('public_cloud'))
        HostGroupByList=[]
        for i in HostGroupBy:
            for j in DBGroupBy:
                if i.get('public_cloud') == j.get('public_cloud'):
                    counts = i.get('public_cloud__count') + j.get('public_cloud__count')
                    HostGroupByList.append({"name":i.get('public_cloud'), "value": counts})
            #HostGroupByList.append({"name":i.get('public_cloud'),"value":i.get('public_cloud__count')})
        overview['clouds_asset_count']=HostGroupByList

        '''2、不同类型资产占比'''
        HostAll = Host.objects.count()
        DataBaseAll = DataBase.objects.count()
        overview['each_type_assets_count'] = [{'name': '服务器','value':HostAll},{'name':'数据库','value':DataBaseAll}]
        #[{'name': '服务器', 'value': 54}, {'name': 'RDS', 'value': 5}, {'name': 'NAS', 'value': 7}]


        '''3、业务线资产占比，这个不会用ORM写，自己实现的感觉太复杂'''
        #[{'name': '未分配', 'value': 41}, {'name': '商城', 'value': 3}]
        #overview.business_line_host_nums
        BusinessLineHostByList = []
        cursor=connection.cursor()
        cursor.execute("select a.name_cn, count(a.name_cn) from cmdb_tag a,cmdb_host_tags b, cmdb_host c where b.tag_id = a.id and b.host_id = c.id GROUP BY(a.name_cn)")
        CursorAll = cursor.fetchall()
        print(CursorAll)  #(('拓扑管理服务器', 1), ('身份管理服务器', 2))
        #得到所有的HOST服务器，进行统计
        YHost_Count = Host.objects.all().count()
        #得到没有分配标签的服务器数量
        TagHostNum = 0
        for x in CursorAll:
            TagHostNum = TagHostNum + x[1]
            BusinessLineHostByList.append({'name': x[0],'value': x[1]})
        UnTagHostNum = YHost_Count - TagHostNum
        BusinessLineHostByList.append({'name':'未分配','value':UnTagHostNum})
        overview['business_line_host_nums'] = BusinessLineHostByList


        '''标签云'''
        #var word_list = [{'text': '数据库', 'weight': 2, 'link': '/assets/hosts/?tag=db'}]
        TagCloudList = []
        AllTags = Tag.objects.all()
        for i in AllTags:
            if i.host_set.all():
                TagCloudList.append({'text':i.name, 'weight':i.host_set.all().count(),'link':'/cmdb/hosts/?tag='+i.name})
                #print('标签云',i.name,i.host_set.all().count())
        # print(TagCloudList)
        overview['tag_cloud'] = TagCloudList
        # print(overview)
        context = {
            'overview': overview,
        }
        return render(request, 'cmdb/assets_overview.html', context=context)
</code></pre>
<p style="line-height: 160%; box-sizing: content-box; margin: 10px 0; color: #333;">效果图：</p>
<p style="line-height: 160%; box-sizing: content-box; margin: 10px 0; color: #333;"><img src="day%2010.resources/32CF93FF-AC7E-4C5B-9F9B-67766F12BFDD.png" height="954" width="1728"/></p>
</div></body></html>