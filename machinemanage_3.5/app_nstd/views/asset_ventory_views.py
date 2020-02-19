# -*- coding:utf-8 -*-
from django.http import HttpResponse
from app_nstd.models import asset_ventory_models
from config.models import common
from machinemanage.settings import BASE_DIR
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
from urllib import parse
import mimetypes
import json,datetime,xlwt,os

#在线盘点批次查询
def getVenBat(request):
	b_inven_type = request.GET.get('b_inven_type')
	daterange = request.GET.get('daterange')
	if daterange:
		beginDate,endDate = daterange.split(' - ')
		endDate += ' 23:59:59'
	else:
		beginDate,endDate = '',''
	data = {"code":0,"msg":"","count":0,'data':[]}
	data['data'] = asset_ventory_models.getVenBat(beginDate,endDate,b_inven_type)
	return HttpResponse(json.dumps(data))

#导出在线盘点数据
def VenExport(request):
	datetimestyle = xlwt.XFStyle()
	datetimestyle.num_format_str = 'yyyy-mm-dd hh:mm:ss'

	f = xlwt.Workbook()
	sheet = f.add_sheet('盘点详情',cell_overwrite_ok = True)
	title = ['位置代码','资产番号','资产名称','资产型号','操作员','盘点时间','盘点状态']
	b_id = request.GET.get('b_id')
	u_name = request.session.get('u_nstd_name',None)
	data = asset_ventory_models.VenExport(b_id)

	#生成Excel头部信息
	for i in range(0,len(title)):
		sheet.write(0,i,title[i],common.set_style('Times New Roman',220,True))

	#将搜索数据写入Excel文件
	for i in range(0,len(data)):
		sheet.write(i+1,0,data[i]['b_location'])
		sheet.write(i+1,1,data[i]['i_cd'])
		sheet.write(i+1,2,data[i]['a_name'])
		sheet.write(i+1,3,data[i]['a_type_cd'])
		sheet.write(i+1,4,data[i]['b_user_name'])
		sheet.write(i+1,5,data[i]['b_datetime'],datetimestyle)
		sheet.write(i+1,6,data[i]['i_status'])

	#在服务器端保存Excel文件
	filename = '资产盘点详情_{0}.xls'.format(u_name)
	path = os.path.join(BASE_DIR,'media')
	the_file = os.path.join(path,filename)
	f.save(the_file)
	
	#下载Excel文件
	chunk_size = 8192
	response = StreamingHttpResponse(FileWrapper(open(the_file, 'rb'), chunk_size),
			content_type=mimetypes.guess_type(the_file)[0])
	response['Content-Length'] = os.path.getsize(the_file)
	response['Content-Disposition'] = "attachment; filename="+parse.quote(filename)
	return response

#删除盘点数据
def delVen(request):
	b_id = request.GET.get('b_id')
	result = asset_ventory_models.delVen(b_id)
	return HttpResponse(json.dumps({'result':result}))