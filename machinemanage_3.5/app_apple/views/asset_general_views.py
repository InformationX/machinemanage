# -*- coding:utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
from urllib import parse
from app_apple.models import asset_general_models
from config.models import common
from machinemanage.settings import BASE_DIR
import os,json,datetime,xlwt
import mimetypes

#获取在库数据
def get_storage_data(request):
	beginDate = request.GET.get('beginDate')
	endDate = request.GET.get('endDate')
	if endDate:
		endDate += ' 23:59:59'

	page = request.GET.get('page')
	limit = request.GET.get('limit')
	assetList,count = asset_general_models.get_storage_data(beginDate,endDate,int(page),int(limit))
	data = {"code": 0,"msg": "","count": count,"data": assetList}
	return HttpResponse(json.dumps(data))

#获取支给归还数据
def get_zj_back(request):
	beginDate = request.GET.get('beginDate')
	endDate = request.GET.get('endDate')
	if endDate:
		endDate += ' 23:59:59'
	page = request.GET.get('page')
	limit = request.GET.get('limit')
	data = {"code": 0,"msg": "","count": 1}
	data['data'],data['count'] = asset_general_models.get_zj_back(beginDate,endDate,int(page),int(limit))
	return HttpResponse(json.dumps(data))

#获取添加数据
def get_add_data(request):
	beginDate = request.GET.get('beginDate')
	endDate = request.GET.get('endDate')
	data = {
	  "code": 0,
  	  "msg": "",
      "count": 2,
	  "data": [
	  	{
	  		'a_cd':'N10595','a_type_cd':'CA-CN3L','a_fuselage_cd':'P16172-02','a_main_cd':'L1266914',
	  		'a_serial_cd':'L1266914','a_location_cd':'设备库房','a_status':'NG','a_shelf_cd':'GK-G16-01',
	  		'a_operate_time':'2018-05-31','a_mark':'','a_operator':'zw'
	  	},
	  	{
	  		'a_cd':'N10742','a_type_cd':'LWM-100','a_fuselage_cd':'P17028-03','a_main_cd':'L1266913',
	  		'a_serial_cd':'L1266913','a_location_cd':'设备库房','a_status':'OK','a_shelf_cd':'GK-G16-01',
	  		'a_operate_time':'2018-12-28','a_mark':'','a_operator':'zw'
	  	}
	  ]
	}
	asset_general_models.get_add_data(beginDate,endDate)
	return HttpResponse(json.dumps(data))

#获取支给数据
def get_zj_data(request):
	beginDate = request.GET.get('beginDate')
	endDate = request.GET.get('endDate')
	if endDate:
		endDate += ' 23:59:59'
	page = request.GET.get('page')
	limit = request.GET.get('limit')

	data = {"code": 0,"msg": "","count": 0,"data": []}
	data["data"],data['count'] = asset_general_models.get_zj_data(beginDate,endDate,int(page),int(limit))
	return HttpResponse(json.dumps(data))

#获取在线数据
def get_online_data(request):
	data = {"code": 0,"msg": "","count": 2,"data": []}
	data['data'] = asset_general_models.get_online_data()
	return HttpResponse(json.dumps(data))

#获取出库数据
def get_out_data(request):
	beginDate = request.GET.get('beginDate')
	endDate = request.GET.get('endDate')
	if endDate:
		endDate += ' 23:59:59'
	page = request.GET.get('page')
	limit = request.GET.get('limit')
	data = {"code": 0,"msg": "","count": 1}
	data['data'],data['count'] = asset_general_models.get_out_data(beginDate,endDate,int(page),int(limit))
	return HttpResponse(json.dumps(data))

#获取退库数据
def get_back_data(request):
	beginDate = request.GET.get('beginDate')
	endDate = request.GET.get('endDate')
	if endDate:
		endDate += ' 23:59:59'
	page = request.GET.get('page')
	limit = request.GET.get('limit')
	data = {"code": 0,"msg": "","count": 1}
	data['data'],data['count'] = asset_general_models.get_back_data(beginDate,endDate,int(page),int(limit))
	return HttpResponse(json.dumps(data))

#在库数据导出
def storage_export(request):
	beginDate = request.GET.get('beginDate')
	endDate = request.GET.get('endDate')
	b_name = request.session.get('u_b_name')
	data = asset_general_models.get_storage_export(beginDate,endDate)
	f = xlwt.Workbook()
	sheet = f.add_sheet('sheet1',cell_overwrite_ok = True)
	title = ['资产番号','型号','主体资产番号','主体序列号','机身号码','位置编号','状态','备注信息']

	#生成Excel头部信息
	for i in range(0,len(title)):
		sheet.write(0,i,title[i],common.set_style('Times New Roman',220,True))

	#将搜索数据写入Excel文件
	for i in range(0,len(data)):
		sheet.write(i+1,0,data[i]['a_cd'])
		sheet.write(i+1,1,data[i]['a_type_cd'])	
		sheet.write(i+1,2,data[i]['a_main_cd'])
		sheet.write(i+1,3,data[i]['a_main_serial'])
		sheet.write(i+1,4,data[i]['a_fuselage_cd'])
		sheet.write(i+1,5,data[i]['a_action_loc'])
		sheet.write(i+1,6,data[i]['a_action_state'])
		sheet.write(i+1,7,data[i]['a_action_remark'])

	#在服务器端保存Excel文件
	filename = '入库信息导出_{0}.xls'.format(b_name)
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

#支给数据导出
def zj_export(request):
	beginDate = request.GET.get('beginDate')
	endDate = request.GET.get('endDate')
	b_name = request.session.get('u_b_name')
	data = asset_general_models.get_zj_export(beginDate,endDate)
	f = xlwt.Workbook()
	sheet = f.add_sheet('sheet1',cell_overwrite_ok = True)
	title = ['序号','资产番号','型号','机身号码','主体资产番号','主体序列号','资产状态','被支给方','备注信息','操作员','操作时间']

	#生成Excel头部信息
	for i in range(0,len(title)):
		sheet.write(0,i,title[i],common.set_style('Times New Roman',220,True))

	#将搜索数据写入Excel文件
	for i in range(0,len(data)):
		sheet.write(i+1,0,i + 1)
		sheet.write(i+1,1,data[i]['a_cd'])
		sheet.write(i+1,2,data[i]['a_type_cd'])	
		sheet.write(i+1,3,data[i]['a_fuselage_cd'])
		sheet.write(i+1,4,data[i]['a_main_cd'])
		sheet.write(i+1,5,data[i]['a_main_serial'])
		sheet.write(i+1,6,data[i]['a_action_state'])
		sheet.write(i+1,7,data[i]['a_zj_object'])
		sheet.write(i+1,8,data[i]['a_action_remark'])
		sheet.write(i+1,9,data[i]['a_opr_user'])
		sheet.write(i+1,10,data[i]['a_add_time'])

	#在服务器端保存Excel文件
	filename = '支给数据导出_{0}.xls'.format(b_name)
	path = os.path.join(os.path.join(BASE_DIR,'media'),'tmp_folder')
	the_file = os.path.join(path,filename)
	f.save(the_file)
	
	#下载Excel文件
	chunk_size = 8192
	response = StreamingHttpResponse(FileWrapper(open(the_file, 'rb'), chunk_size),
			content_type=mimetypes.guess_type(the_file)[0])
	response['Content-Length'] = os.path.getsize(the_file)
	response['Content-Disposition'] = "attachment; filename="+parse.quote(filename)
	return response

#支给归还导出
def zj_back_export(request):
	beginDate = request.GET.get('beginDate')
	endDate = request.GET.get('endDate')
	if endDate:
		endDate += ' 23:59:59'
	b_name = request.session.get('u_b_name')
	data = asset_general_models.zj_back_data(beginDate,endDate)
	f = xlwt.Workbook()
	sheet = f.add_sheet('支给归还导出',cell_overwrite_ok = True)
	title = ['序号','资产番号','型号','机身号码','主体资产番号','主体序列号','资产状态','当前位置','备注信息','操作员','操作时间']

	#生成Excel头部信息
	for i in range(0,len(title)):
		sheet.write(0,i,title[i],common.set_style('Times New Roman',220,True))

	#将搜索数据写入Excel文件
	for i in range(0,len(data)):
		sheet.write(i+1,0,i + 1)
		sheet.write(i+1,1,data[i]['a_cd'])
		sheet.write(i+1,2,data[i]['a_type_cd'])	
		sheet.write(i+1,3,data[i]['a_fuselage_cd'])
		sheet.write(i+1,4,data[i]['a_main_cd'])
		sheet.write(i+1,5,data[i]['a_main_serial'])
		sheet.write(i+1,6,data[i]['a_action_state'])
		sheet.write(i+1,7,data[i]['a_action_loc'])
		sheet.write(i+1,8,data[i]['a_action_remark'])
		sheet.write(i+1,9,data[i]['a_opr_user'])
		sheet.write(i+1,10,data[i]['a_add_time'])

	#在服务器端保存Excel文件
	filename = '支给归还导出_{0}.xls'.format(b_name)
	path = os.path.join(os.path.join(BASE_DIR,'media'),'tmp_folder')
	the_file = os.path.join(path,filename)
	f.save(the_file)
	
	#下载Excel文件
	chunk_size = 8192
	response = StreamingHttpResponse(FileWrapper(open(the_file, 'rb'), chunk_size),
			content_type=mimetypes.guess_type(the_file)[0])
	response['Content-Length'] = os.path.getsize(the_file)
	response['Content-Disposition'] = "attachment; filename="+parse.quote(filename)
	return response

#出库信息导出
def out_export(request):
	beginDate = request.GET.get('beginDate')
	endDate = request.GET.get('endDate')
	if endDate:
		endDate += ' 23:59:59'
	b_name = request.session.get('u_b_name')
	data = asset_general_models.out_export(beginDate,endDate)
	f = xlwt.Workbook()
	sheet = f.add_sheet('支给归还导出',cell_overwrite_ok = True)
	title = ['序号','资产番号','型号','机身号码','主体资产番号','主体序列号','领用线别','领用人','使用位置','资产状态','主管确认','备注信息','操作员','操作时间']

	#生成Excel头部信息
	for i in range(0,len(title)):
		sheet.write(0,i,title[i],common.set_style('Times New Roman',220,True))

	#将搜索数据写入Excel文件
	for i in range(0,len(data)):
		sheet.write(i+1,0,i + 1)
		sheet.write(i+1,1,data[i]['a_cd'])
		sheet.write(i+1,2,data[i]['a_type_cd'])	
		sheet.write(i+1,3,data[i]['a_fuselage_cd'])
		sheet.write(i+1,4,data[i]['a_main_cd'])
		sheet.write(i+1,5,data[i]['a_main_serial'])
		sheet.write(i+1,6,data[i]['a_take_line'])
		sheet.write(i+1,7,data[i]['a_take_user'])
		sheet.write(i+1,8,data[i]['a_action_loc'])
		sheet.write(i+1,9,data[i]['a_action_state'])
		sheet.write(i+1,10,data[i]['a_confirm_user'])
		sheet.write(i+1,11,data[i]['a_action_remark'])
		sheet.write(i+1,12,data[i]['a_opr_user'])
		sheet.write(i+1,13,data[i]['a_add_time'])

	#在服务器端保存Excel文件
	filename = '出库信息导出_{0}.xls'.format(b_name)
	path = os.path.join(os.path.join(BASE_DIR,'media'),'tmp_folder')
	the_file = os.path.join(path,filename)
	f.save(the_file)
	
	#下载Excel文件
	chunk_size = 8192
	response = StreamingHttpResponse(FileWrapper(open(the_file, 'rb'), chunk_size),
			content_type=mimetypes.guess_type(the_file)[0])
	response['Content-Length'] = os.path.getsize(the_file)
	response['Content-Disposition'] = "attachment; filename="+parse.quote(filename)
	return response

#退库信息导出
def out_back_export(request):
	beginDate = request.GET.get('beginDate')
	endDate = request.GET.get('endDate')
	if endDate:
		endDate += ' 23:59:59'
	b_name = request.session.get('u_b_name')
	data = asset_general_models.out_back_export(beginDate,endDate)
	f = xlwt.Workbook()
	sheet = f.add_sheet('退库导出',cell_overwrite_ok = True)
	title = ['序号','资产番号','型号','机身号码','主体资产番号','主体序列号','退库位置','资产状态','退库人员','主管确认','备注信息','操作员','操作时间']

	#生成Excel头部信息
	for i in range(0,len(title)):
		sheet.write(0,i,title[i],common.set_style('Times New Roman',220,True))

	#将搜索数据写入Excel文件
	for i in range(0,len(data)):
		sheet.write(i+1,0,i + 1)
		sheet.write(i+1,1,data[i]['a_cd'])
		sheet.write(i+1,2,data[i]['a_type_cd'])	
		sheet.write(i+1,3,data[i]['a_fuselage_cd'])
		sheet.write(i+1,4,data[i]['a_main_cd'])
		sheet.write(i+1,5,data[i]['a_main_serial'])
		sheet.write(i+1,6,data[i]['a_action_loc'])
		sheet.write(i+1,7,data[i]['a_action_state'])
		sheet.write(i+1,8,data[i]['a_back_user'])
		sheet.write(i+1,9,data[i]['a_confirm_user'])
		sheet.write(i+1,10,data[i]['a_action_remark'])
		sheet.write(i+1,11,data[i]['a_opr_user'])
		sheet.write(i+1,12,data[i]['a_add_time'])

	#在服务器端保存Excel文件
	filename = '退库信息导出_{0}.xls'.format(b_name)
	path = os.path.join(os.path.join(BASE_DIR,'media'),'tmp_folder')
	the_file = os.path.join(path,filename)
	f.save(the_file)
	
	#下载Excel文件
	chunk_size = 8192
	response = StreamingHttpResponse(FileWrapper(open(the_file, 'rb'), chunk_size),
			content_type=mimetypes.guess_type(the_file)[0])
	response['Content-Length'] = os.path.getsize(the_file)
	response['Content-Disposition'] = "attachment; filename="+parse.quote(filename)
	return response

#总账导出
def total_export(request):
	b_name = request.session.get('u_b_name')
	startDate = request.GET.get('startDate')
	endDate = request.GET.get('endDate')
	if endDate:
		endTime = endDate + ' 23:59:59'
	else:
		endTime = endDate

	data = asset_general_models.get_total_data(startDate,endTime)
	f = xlwt.Workbook()
	sheet = f.add_sheet('sheet1',cell_overwrite_ok = True)
	title = ['资产番号','资产型号','机身号','主体资产番号','主体序列号','当前部门','使用机种','资产位置','资产状态','操作时间','备注信息','行为类型','操作员']
	#生成Excel头部信息
	for i in range(0,len(title)):
		sheet.write(0,i,title[i],common.set_style('Times New Roman',220,True))

	#将搜索数据写入Excel文件
	for i in range(0,len(data)):
		sheet.write(i+1,0,data[i]['a_cd'])
		sheet.write(i+1,1,data[i]['a_type_cd'])
		sheet.write(i+1,2,data[i]['a_fuselage_cd'])
		sheet.write(i+1,3,data[i]['a_main_cd'])
		sheet.write(i+1,4,data[i]['a_main_serial'])
		sheet.write(i+1,5,data[i]['a_action_dept'])
		sheet.write(i+1,6,data[i]['a_action_model'])
		sheet.write(i+1,7,data[i]['a_action_loc'])
		sheet.write(i+1,8,data[i]['a_action_state'])
		sheet.write(i+1,9,data[i]['a_add_time'])
		sheet.write(i+1,10,data[i]['a_action_remark'])
		sheet.write(i+1,11,data[i]['a_action_type'])

	#在服务器端保存Excel文件
	filename = '总账信息导出_{0}.xls'.format(b_name)
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

def get_history_data(request):
	a_cd = request.GET.get('a_cd')
	data = {"code": 0,"msg": "","count": 2}
	data['data'] = asset_general_models.get_history_data(a_cd)
	data['count'] = len(data['data'])
	return HttpResponse(json.dumps(data))
