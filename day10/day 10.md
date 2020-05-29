<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/><meta name="exporter-version" content="Evernote Mac 9.3.3 (459822)"/><meta name="author" content="zhoushuyu215@163.com"/><meta name="created" content="2020-05-29 16:08:34 +0000"/><meta name="source" content="desktop.mac"/><meta name="updated" content="2020-05-29 16:12:34 +0000"/><meta name="content-class" content="yinxiang.markdown"/><title>day 10</title></head><body><div style="font-size: 14px; margin: 0; padding: 0; width: 100%;"><pre style="line-height: 160%; box-sizing: content-box; border: 0; border-radius: 0; margin: 2px 0 8px; background-color: #f5f7f8;"><code style="display: block; overflow-x: auto; background: #1e1e1e; line-height: 160%; box-sizing: content-box; border: 0; border-radius: 0; letter-spacing: -.3px; padding: 18px; color: #f4f4f4; white-space: pre-wrap;">class AssetsOverView(LoginRequiredMixin, View):
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
</div><center style="display:none !important;visibility:collapse !important;height:0 !important;white-space:nowrap;width:100%;overflow:hidden">%0A%60%60%60%0Aclass%20AssetsOverView(LoginRequiredMixin%2C%20View)%3A%0A%20%20%20%20%22%22%22%0A%20%20%20%20%E8%B5%84%E4%BA%A7%E5%A4%A7%E7%9B%98%0A%20%20%20%20%22%22%22%0A%20%20%20%20def%20get(self%2C%20request)%3A%0A%20%20%20%20%20%20%20%20overview%20%3D%20%7B%7D%0A%0A%20%20%20%20%20%20%20%20'''1%E3%80%81%E5%A4%9A%E4%BA%91%E8%B5%84%E4%BA%A7%E5%88%86%E5%B8%83%E7%BB%9F%E8%AE%A1'''%0A%20%20%20%20%20%20%20%20%23%5B%7B%22name%22%3A%20%22%E9%98%BF%E9%87%8C%E4%BA%91%22%2C%20%22value%22%3A%2040%7D%2C%20%7B%22name%22%3A%20%22%E8%85%BE%E8%AE%AF%E4%BA%91%22%2C%20%22value%22%3A%2026%7D%5D%0A%20%20%20%20%20%20%20%20HostGroupBy%20%3D%20Host.objects.values('public_cloud').annotate(Count('public_cloud'))%0A%20%20%20%20%20%20%20%20DBGroupBy%20%3D%20DataBase.objects.values('public_cloud').annotate(Count('public_cloud'))%0A%20%20%20%20%20%20%20%20HostGroupByList%3D%5B%5D%0A%20%20%20%20%20%20%20%20for%20i%20in%20HostGroupBy%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20for%20j%20in%20DBGroupBy%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20if%20i.get('public_cloud')%20%3D%3D%20j.get('public_cloud')%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20counts%20%3D%20i.get('public_cloud__count')%20%2B%20j.get('public_cloud__count')%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20HostGroupByList.append(%7B%22name%22%3Ai.get('public_cloud')%2C%20%22value%22%3A%20counts%7D)%0A%20%20%20%20%20%20%20%20%20%20%20%20%23HostGroupByList.append(%7B%22name%22%3Ai.get('public_cloud')%2C%22value%22%3Ai.get('public_cloud__count')%7D)%0A%20%20%20%20%20%20%20%20overview%5B'clouds_asset_count'%5D%3DHostGroupByList%0A%0A%20%20%20%20%20%20%20%20'''2%E3%80%81%E4%B8%8D%E5%90%8C%E7%B1%BB%E5%9E%8B%E8%B5%84%E4%BA%A7%E5%8D%A0%E6%AF%94'''%0A%20%20%20%20%20%20%20%20HostAll%20%3D%20Host.objects.count()%0A%20%20%20%20%20%20%20%20DataBaseAll%20%3D%20DataBase.objects.count()%0A%20%20%20%20%20%20%20%20overview%5B'each_type_assets_count'%5D%20%3D%20%5B%7B'name'%3A%20'%E6%9C%8D%E5%8A%A1%E5%99%A8'%2C'value'%3AHostAll%7D%2C%7B'name'%3A'%E6%95%B0%E6%8D%AE%E5%BA%93'%2C'value'%3ADataBaseAll%7D%5D%0A%20%20%20%20%20%20%20%20%23%5B%7B'name'%3A%20'%E6%9C%8D%E5%8A%A1%E5%99%A8'%2C%20'value'%3A%2054%7D%2C%20%7B'name'%3A%20'RDS'%2C%20'value'%3A%205%7D%2C%20%7B'name'%3A%20'NAS'%2C%20'value'%3A%207%7D%5D%0A%0A%0A%20%20%20%20%20%20%20%20'''3%E3%80%81%E4%B8%9A%E5%8A%A1%E7%BA%BF%E8%B5%84%E4%BA%A7%E5%8D%A0%E6%AF%94%EF%BC%8C%E8%BF%99%E4%B8%AA%E4%B8%8D%E4%BC%9A%E7%94%A8ORM%E5%86%99%EF%BC%8C%E8%87%AA%E5%B7%B1%E5%AE%9E%E7%8E%B0%E7%9A%84%E6%84%9F%E8%A7%89%E5%A4%AA%E5%A4%8D%E6%9D%82'''%0A%20%20%20%20%20%20%20%20%23%5B%7B'name'%3A%20'%E6%9C%AA%E5%88%86%E9%85%8D'%2C%20'value'%3A%2041%7D%2C%20%7B'name'%3A%20'%E5%95%86%E5%9F%8E'%2C%20'value'%3A%203%7D%5D%0A%20%20%20%20%20%20%20%20%23overview.business_line_host_nums%0A%20%20%20%20%20%20%20%20BusinessLineHostByList%20%3D%20%5B%5D%0A%20%20%20%20%20%20%20%20cursor%3Dconnection.cursor()%0A%20%20%20%20%20%20%20%20cursor.execute(%22select%20a.name_cn%2C%20count(a.name_cn)%20from%20cmdb_tag%20a%2Ccmdb_host_tags%20b%2C%20cmdb_host%20c%20where%20b.tag_id%20%3D%20a.id%20and%20b.host_id%20%3D%20c.id%20GROUP%20BY(a.name_cn)%22)%0A%20%20%20%20%20%20%20%20CursorAll%20%3D%20cursor.fetchall()%0A%20%20%20%20%20%20%20%20print(CursorAll)%20%20%23(('%E6%8B%93%E6%89%91%E7%AE%A1%E7%90%86%E6%9C%8D%E5%8A%A1%E5%99%A8'%2C%201)%2C%20('%E8%BA%AB%E4%BB%BD%E7%AE%A1%E7%90%86%E6%9C%8D%E5%8A%A1%E5%99%A8'%2C%202))%0A%20%20%20%20%20%20%20%20%23%E5%BE%97%E5%88%B0%E6%89%80%E6%9C%89%E7%9A%84HOST%E6%9C%8D%E5%8A%A1%E5%99%A8%EF%BC%8C%E8%BF%9B%E8%A1%8C%E7%BB%9F%E8%AE%A1%0A%20%20%20%20%20%20%20%20YHost_Count%20%3D%20Host.objects.all().count()%0A%20%20%20%20%20%20%20%20%23%E5%BE%97%E5%88%B0%E6%B2%A1%E6%9C%89%E5%88%86%E9%85%8D%E6%A0%87%E7%AD%BE%E7%9A%84%E6%9C%8D%E5%8A%A1%E5%99%A8%E6%95%B0%E9%87%8F%0A%20%20%20%20%20%20%20%20TagHostNum%20%3D%200%0A%20%20%20%20%20%20%20%20for%20x%20in%20CursorAll%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20TagHostNum%20%3D%20TagHostNum%20%2B%20x%5B1%5D%0A%20%20%20%20%20%20%20%20%20%20%20%20BusinessLineHostByList.append(%7B'name'%3A%20x%5B0%5D%2C'value'%3A%20x%5B1%5D%7D)%0A%20%20%20%20%20%20%20%20UnTagHostNum%20%3D%20YHost_Count%20-%20TagHostNum%0A%20%20%20%20%20%20%20%20BusinessLineHostByList.append(%7B'name'%3A'%E6%9C%AA%E5%88%86%E9%85%8D'%2C'value'%3AUnTagHostNum%7D)%0A%20%20%20%20%20%20%20%20overview%5B'business_line_host_nums'%5D%20%3D%20BusinessLineHostByList%0A%0A%0A%20%20%20%20%20%20%20%20'''%E6%A0%87%E7%AD%BE%E4%BA%91'''%0A%20%20%20%20%20%20%20%20%23var%20word_list%20%3D%20%5B%7B'text'%3A%20'%E6%95%B0%E6%8D%AE%E5%BA%93'%2C%20'weight'%3A%202%2C%20'link'%3A%20'%2Fassets%2Fhosts%2F%3Ftag%3Ddb'%7D%5D%0A%20%20%20%20%20%20%20%20TagCloudList%20%3D%20%5B%5D%0A%20%20%20%20%20%20%20%20AllTags%20%3D%20Tag.objects.all()%0A%20%20%20%20%20%20%20%20for%20i%20in%20AllTags%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20if%20i.host_set.all()%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20TagCloudList.append(%7B'text'%3Ai.name%2C%20'weight'%3Ai.host_set.all().count()%2C'link'%3A'%2Fcmdb%2Fhosts%2F%3Ftag%3D'%2Bi.name%7D)%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%23print('%E6%A0%87%E7%AD%BE%E4%BA%91'%2Ci.name%2Ci.host_set.all().count())%0A%20%20%20%20%20%20%20%20%23%20print(TagCloudList)%0A%20%20%20%20%20%20%20%20overview%5B'tag_cloud'%5D%20%3D%20TagCloudList%0A%20%20%20%20%20%20%20%20%23%20print(overview)%0A%20%20%20%20%20%20%20%20context%20%3D%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20'overview'%3A%20overview%2C%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20return%20render(request%2C%20'cmdb%2Fassets_overview.html'%2C%20context%3Dcontext)%0A%60%60%60%0A%0A%E6%95%88%E6%9E%9C%E5%9B%BE%EF%BC%9A%0A%0A!%5Bf8b7095f03fd98623e6875f63273238a.png%5D(evernotecid%3A%2F%2FBA30DB65-67D6-4761-A907-0CB104C2E14B%2Fappyinxiangcom%2F18707421%2FENResource%2Fp811)%0A</center></body></html>