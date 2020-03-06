# -*- coding:utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from app_nstd.models import asset_general_models
from config.models import common
from machinemanage.settings import BASE_DIR
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
from urllib import parse
import json,datetime,os,xlwt
import mimetypes

#入库信息查询
def add_search_page(request):
	return render(request, 'nstd/general/add_search_page.html')

#获取添加数据
def get_add_data(request):
	a_cd = request.GET.get('a_cd')
	startDate = request.GET.get('startDate')
	endDate = request.GET.get('endDate')
	if endDate:
		endDate += ' 23:59:59'
	page = int(request.GET.get('page'))
	limit = int(request.GET.get('limit'))

	data = {"code": 0,"msg": "","count": 1,"data": []}
	data['data'],data['count'] = asset_general_models.get_add_data(a_cd,startDate,endDate,page,limit)
	return HttpResponse(json.dumps(data))

#导出入库数据
def add_export(request):
	a_cd = request.GET.get('a_cd')
	startDate = request.GET.get('startDate')
	endDate = request.GET.get('endDate')
	if endDate:
		endDate += ' 23:59:59'
	page = request.GET.get('page')
	limit = request.GET.get('limit')
	u_name = request.session.get('u_nstd_name')
	data = asset_general_models.get_add_export_data(a_cd,startDate,endDate,page,limit)
	f = xlwt.Workbook()
	sheet = f.add_sheet('sheet1',cell_overwrite_ok = True)
	title = ['资产番号','资产编号','资产名称','资产型号','机身号码','单位','单价','币种',
		'出厂时间','购入时间','品牌','供应商','入库位置','入库状态','购入机种','预算号',
		'请示书号','PO号','SAP番号','工程代码','经费类别','记录时间','操作员','备注信息']

	#生成Excel头部信息
	for i in range(0,len(title)):
		sheet.write(0,i,title[i],common.set_style('Times New Roman',220,True))

	#将搜索数据写入Excel文件
	for i in range(0,len(data)):
		sheet.write(i+1,0,data[i]['a_cd'])
		sheet.write(i+1,1,data[i]['a_self_cd'])	
		sheet.write(i+1,2,data[i]['a_name'])
		sheet.write(i+1,3,data[i]['a_type_cd'])
		sheet.write(i+1,4,data[i]['a_fuselage_cd'])
		sheet.write(i+1,5,data[i]['a_amount'])

		if request.session.get('authority_level') == 1 or request.session.get('dept_name') == '设备购买部':		
			sheet.write(i+1,6,data[i]['a_price'])
			sheet.write(i+1,7,data[i]['a_currency'])
		else:
			sheet.write(i+1,6,'***')
			sheet.write(i+1,7,'***')

		sheet.write(i+1,8,data[i]['a_out_time'])
		sheet.write(i+1,9,data[i]['a_purchase_time'])
		sheet.write(i+1,10,data[i]['a_brand'])
		sheet.write(i+1,11,data[i]['a_supplier'])
		sheet.write(i+1,12,data[i]['a_loc_cd'])
		sheet.write(i+1,13,data[i]['a_status'])
		sheet.write(i+1,14,data[i]['a_model'])
		sheet.write(i+1,15,data[i]['a_budget'])
		sheet.write(i+1,16,data[i]['a_referendum'])
		sheet.write(i+1,17,data[i]['a_po_cd'])
		sheet.write(i+1,18,data[i]['a_sap_cd'])
		sheet.write(i+1,19,data[i]['a_project_cd'])
		sheet.write(i+1,20,data[i]['a_funds_type'])
		sheet.write(i+1,21,data[i]['a_record_time'])
		sheet.write(i+1,22,data[i]['a_user_id'])
		sheet.write(i+1,23,data[i]['a_remark'])

	#在服务器端保存Excel文件
	filename = '入库信息导出_{0}.xls'.format(u_name)
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

#支给信息页面
def zj_search_page(request):
	return render(request, 'nstd/general/zj_search_page.html')

#获取支给数据
def get_zj_data(request):
	a_cd = request.GET.get('a_cd')
	startDate = request.GET.get('startDate')
	endDate = request.GET.get('endDate')
	if endDate:
		endDate += ' 23:59:59'
	page = int(request.GET.get('page'))
	limit = int(request.GET.get('limit'))
	data = {"code": 0,"msg": "","count": 0,"data": []}
	data['data'],data['count'] = asset_general_models.get_zj_data(a_cd,startDate,endDate,page,limit)
	return HttpResponse(json.dumps(data))

#支给导出
def zj_export(request):
	a_cd = request.GET.get('a_cd')
	startDate = request.GET.get('startDate')
	endDate = request.GET.get('endDate')
	if endDate:
		endDate += ' 23:59:59'
	u_name = request.session.get('u_nstd_name',None)
	data = asset_general_models.get_zj_export_data(a_cd,startDate,endDate)
	response = general_export(data,'支给信息导出',u_name)
	return response

#获取支给归还数据
def get_zj_revert_data(request):
	beginDate = request.GET.get('beginDate')
	endDate = request.GET.get('endDate')
	if endDate:
		endDate += ' 23:59:59'
	a_cd = request.GET.get('a_cd')
	a_self_cd = request.GET.get('a_self_cd')
	a_type_cd = request.GET.get('a_type_cd')
	a_action_loc = request.GET.get('a_action_loc')
	a_action_state = request.GET.get('a_action_state')
	page = int(request.GET.get('page'))
	limit = int(request.GET.get('limit'))
	data = {
	  "code": 0,
  	  "msg": "",
      "count": 1,
	  "data": []
	}
	data['data'],data['count'] = asset_general_models.get_zj_revert_data(beginDate,endDate,
			a_cd,a_type_cd,a_self_cd,a_action_loc,a_action_state,page,limit)
	return HttpResponse(json.dumps(data))

#支给归还数据导出
def zj_revert_export(request):
	u_name = request.session.get('u_nstd_name')
	data = asset_general_models.zj_revert_export_data()

	f = xlwt.Workbook()
	sheet = f.add_sheet('sheet1',cell_overwrite_ok = True)
	title = [
		'资产番号','资产编号','资产名称','资产型号','机身号码','单位','单价','币种','出厂时间',
		'购入时间','品牌','供应商','位置代码','状态','机种','预算号','请示书号','PO号',
		'SAP番号','工程代码','经费类别','记录时间','操作员','备注信息'
	]

	#生成Excel头部信息
	for i in range(0,len(title)):
		sheet.write(0,i,title[i],common.set_style('Times New Roman',220,True))

	#将搜索数据写入Excel文件
	for i in range(0,len(data)):
		sheet.write(i+1,0,data[i]['a_cd'])
		sheet.write(i+1,1,data[i]['a_self_cd'])	
		sheet.write(i+1,2,data[i]['a_name'])
		sheet.write(i+1,3,data[i]['a_type_cd'])
		sheet.write(i+1,4,data[i]['a_fuselage_cd'])
		sheet.write(i+1,5,data[i]['a_amount'])

		if request.session.get('authority_level') == 1 or request.session.get('dept_name') == '设备购买部':
			sheet.write(i+1,5,data[i]['a_price'])
			sheet.write(i+1,6,data[i]['a_currency'])
		else:
			sheet.write(i+1,5,'***')
			sheet.write(i+1,6,'***')

		sheet.write(i+1,7,data[i]['a_out_time'])
		sheet.write(i+1,8,data[i]['a_purchase_time'])
		sheet.write(i+1,9,data[i]['a_brand'])
		sheet.write(i+1,10,data[i]['a_supplier'])
		sheet.write(i+1,11,data[i]['a_action_loc'])
		sheet.write(i+1,12,data[i]['a_action_state'])
		sheet.write(i+1,13,data[i]['a_model'])
		sheet.write(i+1,14,data[i]['a_budget'])
		sheet.write(i+1,15,data[i]['a_referendum'])
		sheet.write(i+1,16,data[i]['a_po_cd'])
		sheet.write(i+1,17,data[i]['a_sap_cd'])
		sheet.write(i+1,18,data[i]['a_project_cd'])
		sheet.write(i+1,19,data[i]['a_funds_type'])
		sheet.write(i+1,20,data[i]['a_record_time'])
		sheet.write(i+1,21,data[i]['a_opr_user'])
		sheet.write(i+1,22,data[i]['a_action_remark'])

	#在服务器端保存Excel文件
	filename = '支给归还信息_{0}.xls'.format(u_name)
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


#获取出库数据
def get_out_storage_data(request):
	a_cd = request.GET.get('a_cd')
	a_action_loc = request.GET.get('a_action_loc')
	startDate = request.GET.get('startDate')
	endDate = request.GET.get('endDate')
	if endDate:
		endDate += ' 23:59:59'
	page = int(request.GET.get('page'))
	limit = int(request.GET.get('limit'))
	data = {"code": 0,"msg": "","count": 1,"data": []}
	data['data'],data['count'] = asset_general_models.get_out_storage_data(a_cd,a_action_loc,startDate,endDate,page,limit)
	return HttpResponse(json.dumps(data))

#导出出库数据
def out_export(request):
	a_cd = request.GET.get('a_cd')
	a_action_loc = request.GET.get('a_action_loc')
	startDate = request.GET.get('startDate')
	endDate = request.GET.get('endDate')
	if endDate:
		endDate += ' 23:59:59'

	u_name = request.session.get('u_nstd_name',None)
	data = asset_general_models.get_out_export_data(a_cd,a_action_loc,startDate,endDate)

	f = xlwt.Workbook()
	sheet = f.add_sheet('sheet1',cell_overwrite_ok = True)
	title = ['资产番号','资产编号','资产名称','资产型号','机身号码','单位','单价','币种',
		'出厂时间','购入时间','品牌','供应商','位置代码','状态','机种','领用部门',
		'领用人员','主管确认','预算号','请示书号','PO号','SAP番号','工程代码',
		'经费类别','记录时间','操作员','备注信息']

	#生成Excel头部信息
	for i in range(0,len(title)):
		sheet.write(0,i,title[i],common.set_style('Times New Roman',220,True))

	#将搜索数据写入Excel文件
	for i in range(0,len(data)):
		sheet.write(i+1,0,data[i]['a_cd'])
		sheet.write(i+1,1,data[i]['a_self_cd'])	
		sheet.write(i+1,2,data[i]['a_name'])
		sheet.write(i+1,3,data[i]['a_type_cd'])
		sheet.write(i+1,4,data[i]['a_fuselage_cd'])
		sheet.write(i+1,5,data[i]['a_amount'])

		if request.session.get('authority_level') == 1 or request.session.get('dept_name') == '设备购买部':
			sheet.write(i+1,6,data[i]['a_price'])
			sheet.write(i+1,7,data[i]['a_currency'])
		else:
			sheet.write(i+1,6,'***')
			sheet.write(i+1,7,'***')

		sheet.write(i+1,8,data[i]['a_out_time'])
		sheet.write(i+1,9,data[i]['a_purchase_time'])
		sheet.write(i+1,10,data[i]['a_brand'])
		sheet.write(i+1,11,data[i]['a_supplier'])
		sheet.write(i+1,12,data[i]['a_action_loc'])
		sheet.write(i+1,13,data[i]['a_action_state'])
		sheet.write(i+1,14,data[i]['a_model'])
		sheet.write(i+1,15,data[i]['a_action_depart'])
		sheet.write(i+1,16,data[i]['a_action_user'])
		sheet.write(i+1,17,data[i]['a_action_charge'])
		sheet.write(i+1,18,data[i]['a_budget'])
		sheet.write(i+1,19,data[i]['a_referendum'])
		sheet.write(i+1,20,data[i]['a_po_cd'])
		sheet.write(i+1,21,data[i]['a_sap_cd'])
		sheet.write(i+1,22,data[i]['a_project_cd'])
		sheet.write(i+1,23,data[i]['a_funds_type'])
		sheet.write(i+1,24,data[i]['a_record_time'])
		sheet.write(i+1,25,data[i]['a_opr_user'])
		sheet.write(i+1,26,data[i]['a_action_remark'])

	#在服务器端保存Excel文件
	filename = '{0}_{1}.xls'.format('出库信息导出',u_name)
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

#获取退库数据
def get_back_storage_data(request):
	a_cd = request.GET.get('a_cd')
	a_action_loc = request.GET.get('a_action_loc')
	startDate = request.GET.get('startDate')
	endDate = request.GET.get('endDate')
	if endDate:
		endDate += ' 23:59:59'
	page = int(request.GET.get('page'))
	limit = int(request.GET.get('limit'))

	data = {"code": 0,"msg": "","count": 1,"data": []}
	data['data'],data['count'] = asset_general_models.get_back_storage_data(a_cd,a_action_loc,startDate,endDate,page,limit)
	return HttpResponse(json.dumps(data))

#导出退库数据
def back_export(request):
	a_cd = request.GET.get('a_cd')
	a_action_loc = request.GET.get('a_action_loc')
	startDate = request.GET.get('startDate')
	endDate = request.GET.get('endDate')
	if endDate:
		endDate += ' 23:59:59'

	u_name = request.session.get('u_nstd_name',None)
	data = asset_general_models.get_back_export_data(a_cd,a_action_loc,startDate,endDate)
	f = xlwt.Workbook()
	sheet = f.add_sheet('sheet1',cell_overwrite_ok = True)
	title = ['资产番号','资产编号','资产名称','资产型号','机身号码','单位','单价','币种',
		'出厂时间','购入时间','品牌','供应商','位置代码','状态','机种','退库人员',
		'主管确认','预算号','请示书号','PO号','SAP番号','工程代码','经费类别',
		'记录时间','操作员','备注信息']

	#生成Excel头部信息
	for i in range(0,len(title)):
		sheet.write(0,i,title[i],common.set_style('Times New Roman',220,True))

	#将搜索数据写入Excel文件
	for i in range(0,len(data)):
		sheet.write(i+1,0,data[i]['a_cd'])
		sheet.write(i+1,1,data[i]['a_self_cd'])	
		sheet.write(i+1,2,data[i]['a_name'])
		sheet.write(i+1,3,data[i]['a_type_cd'])
		sheet.write(i+1,4,data[i]['a_fuselage_cd'])
		sheet.write(i+1,5,data[i]['a_amount'])

		if request.session.get('authority_level') == 1 or request.session.get('dept_name') == '设备购买部':
			sheet.write(i+1,6,data[i]['a_price'])
			sheet.write(i+1,7,data[i]['a_currency'])
		else:
			sheet.write(i+1,6,'***')
			sheet.write(i+1,7,'***')

		sheet.write(i+1,8,data[i]['a_out_time'])
		sheet.write(i+1,9,data[i]['a_purchase_time'])
		sheet.write(i+1,10,data[i]['a_brand'])
		sheet.write(i+1,11,data[i]['a_supplier'])
		sheet.write(i+1,12,data[i]['a_action_loc'])
		sheet.write(i+1,13,data[i]['a_action_state'])
		sheet.write(i+1,14,data[i]['a_model'])
		sheet.write(i+1,15,data[i]['a_action_user'])
		sheet.write(i+1,16,data[i]['a_action_charge'])
		sheet.write(i+1,17,data[i]['a_budget'])
		sheet.write(i+1,18,data[i]['a_referendum'])
		sheet.write(i+1,19,data[i]['a_po_cd'])
		sheet.write(i+1,20,data[i]['a_sap_cd'])
		sheet.write(i+1,21,data[i]['a_project_cd'])
		sheet.write(i+1,22,data[i]['a_funds_type'])
		sheet.write(i+1,23,data[i]['a_record_time'])
		sheet.write(i+1,24,data[i]['a_opr_user'])
		sheet.write(i+1,25,data[i]['a_action_remark'])

	#在服务器端保存Excel文件
	filename = '{0}_{1}.xls'.format('退库信息导出',u_name)
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

#借用归还数据查询
def get_loan_revert_data(request):
	a_cd = request.GET.get('a_cd')
	startDate = request.GET.get('startDate')
	endDate = request.GET.get('endDate')
	if endDate:
		endDate += ' 23:59:59'
	page = request.GET.get('page')
	limit = request.GET.get('limit')
	data = {"code": 0,"msg": "","count": 1,"data": []}
	data['data'],data['count'] = asset_general_models.get_loan_revert_data(a_cd,startDate,endDate,page,limit)
	return HttpResponse(json.dumps(data))

#借用归还数据导出
def loan_revert_export(request):
	a_cd = request.GET.get('a_cd')
	startDate = request.GET.get('startDate')
	endDate = request.GET.get('endDate')
	u_name = request.session.get('u_nstd_name')
	data = asset_general_models.loan_revert_export_data(a_cd,startDate,endDate)
	f = xlwt.Workbook()
	sheet = f.add_sheet('sheet1',cell_overwrite_ok = True)
	title = [
		'资产番号','编号','资产名称','资产型号','机身号码','单位','单价','币种','出厂时间',
		'购入时间','品牌','供应商','位置代码','状态','机种','预算号','请示书号',
		'PO号','SAP番号','工程代码','经费类别','记录时间','操作员','备注信息'
	]

	#生成Excel头部信息
	for i in range(0,len(title)):
		sheet.write(0,i,title[i],common.set_style('Times New Roman',220,True))

	#将搜索数据写入Excel文件
	for i in range(0,len(data)):
		sheet.write(i+1,0,data[i]['a_cd'])
		sheet.write(i+1,1,data[i]['a_self_cd'])	
		sheet.write(i+1,2,data[i]['a_name'])
		sheet.write(i+1,3,data[i]['a_type_cd'])
		sheet.write(i+1,4,data[i]['a_fuselage_cd'])
		sheet.write(i+1,5,data[i]['a_amount'])

		if request.session.get('authority_level') == 1 or request.session.get('dept_name') == '设备购买部':
			sheet.write(i+1,6,data[i]['a_price'])
			sheet.write(i+1,7,data[i]['a_currency'])
		else:
			sheet.write(i+1,6,'***')
			sheet.write(i+1,7,'***')

		sheet.write(i+1,8,data[i]['a_out_time'])
		sheet.write(i+1,9,data[i]['a_purchase_time'])
		sheet.write(i+1,10,data[i]['a_brand'])
		sheet.write(i+1,11,data[i]['a_supplier'])
		sheet.write(i+1,12,data[i]['a_action_loc'])
		sheet.write(i+1,13,data[i]['a_action_state'])
		sheet.write(i+1,14,data[i]['a_model'])
		sheet.write(i+1,15,data[i]['a_budget'])
		sheet.write(i+1,16,data[i]['a_referendum'])
		sheet.write(i+1,17,data[i]['a_po_cd'])
		sheet.write(i+1,18,data[i]['a_sap_cd'])
		sheet.write(i+1,19,data[i]['a_project_cd'])
		sheet.write(i+1,20,data[i]['a_funds_type'])
		sheet.write(i+1,21,data[i]['a_record_time'])
		sheet.write(i+1,22,data[i]['a_opr_user'])
		sheet.write(i+1,23,data[i]['a_action_remark'])

	#在服务器端保存Excel文件
	filename = '借用归还信息_{0}.xls'.format(u_name)
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

#获取销售数据
def get_sale_data(request):
	a_cd = request.GET.get('a_cd')
	startDate = request.GET.get('startDate')
	endDate = request.GET.get('endDate')
	page = request.GET.get('page')
	limit = request.GET.get('limit')
	if endDate:
		endDate += ' 23:59:59'
	a_cd = request.GET.get('a_cd')
	startDate = request.GET.get('startDate')
	endDate = request.GET.get('endDate')
	data = {"code": 0,"msg": "","count": 1,"data": []}
	data['data'], data['count'] = asset_general_models.get_sale_data(a_cd,startDate,endDate,page,limit)
	return HttpResponse(json.dumps(data))

#导出销售数据
def sale_export(request):
	a_cd = request.GET.get('a_cd')
	startDate = request.GET.get('startDate')
	endDate = request.GET.get('endDate')
	if endDate:
		endDate += ' 23:59:59'
	u_name = request.session.get('u_nstd_name')
	data = asset_general_models.get_sale_export_data(a_cd,startDate,endDate)
	response = general_export(data,'销售信息导出',u_name)
	return response

#获取报废数据
def get_scrap_data(request):
	a_cd = request.GET.get('a_cd')
	startDate = request.GET.get('startDate')
	endDate = request.GET.get('endDate')
	if endDate:
		endDate += ' 23:59:59'
	page = int(request.GET.get('page'))
	limit = int(request.GET.get('limit'))

	data = {"code": 0,"msg": "","count": 1,"data": []}
	data['data'],data['count'] = asset_general_models.get_scrap_data(a_cd, startDate, endDate, page, limit)
	return HttpResponse(json.dumps(data))

#导出报废数据
def scrap_export(request):
	a_cd = request.GET.get('a_cd')
	startDate = request.GET.get('startDate')
	endDate = request.GET.get('endDate')
	if endDate:
		endDate += ' 23:59:59'
	u_name = request.session.get('u_nstd_name')
	data = asset_general_models.get_scrap_export_data(a_cd,startDate,endDate)
	f = xlwt.Workbook()
	sheet = f.add_sheet('sheet1',cell_overwrite_ok = True)
	title = ['资产番号','资产编号','资产名称','资产型号','机身号码','单位','币种','出厂时间','购入时间','品牌',
		'供应商','位置代码','状态','机种','预算号','请示书号','PO号','SAP番号','工程代码','经费类别','记录时间',
		'操作员','备注信息']

	#生成Excel头部信息
	for i in range(0,len(title)):
		sheet.write(0,i,title[i],common.set_style('Times New Roman',220,True))

	#将搜索数据写入Excel文件
	for i in range(0,len(data)):
		sheet.write(i+1,0,data[i]['a_cd'])
		sheet.write(i+1,1,data[i]['a_self_cd'])	
		sheet.write(i+1,2,data[i]['a_name'])
		sheet.write(i+1,3,data[i]['a_type_cd'])
		sheet.write(i+1,4,data[i]['a_fuselage_cd'])
		sheet.write(i+1,5,data[i]['a_amount'])
		sheet.write(i+1,6,data[i]['a_currency'])
		sheet.write(i+1,7,data[i]['a_out_time'])
		sheet.write(i+1,8,data[i]['a_purchase_time'])
		sheet.write(i+1,9,data[i]['a_brand'])
		sheet.write(i+1,10,data[i]['a_supplier'])
		sheet.write(i+1,11,data[i]['a_action_loc'])
		sheet.write(i+1,12,data[i]['a_action_state'])
		sheet.write(i+1,13,data[i]['a_model'])
		sheet.write(i+1,14,data[i]['a_budget'])
		sheet.write(i+1,15,data[i]['a_referendum'])
		sheet.write(i+1,16,data[i]['a_po_cd'])
		sheet.write(i+1,17,data[i]['a_sap_cd'])
		sheet.write(i+1,18,data[i]['a_project_cd'])
		sheet.write(i+1,19,data[i]['a_funds_type'])
		sheet.write(i+1,20,data[i]['a_record_time'])
		sheet.write(i+1,21,data[i]['a_user_id'])
		sheet.write(i+1,22,data[i]['a_remark'])

	#在服务器端保存Excel文件
	filename = '资产报废导出_{0}.xls'.format(u_name)
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

#获取移动数据
def get_move_data(request):
	a_cd = request.GET.get('a_cd')
	startDate = request.GET.get('startDate')
	endDate = request.GET.get('endDate')
	if endDate:
		endDate += ' 23:59:59'
	page = request.GET.get('page')
	limit = request.GET.get('limit')
	data = {"code": 0,"msg": "","count": 1,"data": []}
	data['data'],data['count'] = asset_general_models.get_move_data(a_cd,startDate,endDate,page,limit)
	return HttpResponse(json.dumps(data))

#资产移动信息导出
def move_export(request):
	a_cd = request.GET.get('a_cd')
	startDate = request.GET.get('startDate')
	endDate = request.GET.get('endDate')
	if endDate:
		endDate += ' 23:59:59'
	u_nstd_name = request.session.get('u_nstd_name',None)
	data = asset_general_models.get_move_export_data(a_cd,startDate,endDate)
	f = xlwt.Workbook()
	sheet = f.add_sheet('sheet1',cell_overwrite_ok = True)
	title = [
		'资产番号','资产编号','资产名称','资产型号','机身号码','单位','单价','币种','出厂时间','购入时间','品牌',
		'供应商','原位置','新位置','状态','机种','领用人员','记录时间','操作员','预算号','请示书号','PO号',
		'SAP番号','工程代码','经费类别','主管确认','备注信息'
	]

	#生成Excel头部信息
	for i in range(0,len(title)):
		sheet.write(0,i,title[i],common.set_style('Times New Roman',220,True))

	#将搜索数据写入Excel文件
	for i in range(0,len(data)):
		sheet.write(i+1,0,data[i]['a_cd'])
		sheet.write(i+1,1,data[i]['a_self_cd'])
		sheet.write(i+1,2,data[i]['a_name'])
		sheet.write(i+1,3,data[i]['a_type_cd'])
		sheet.write(i+1,4,data[i]['a_fuselage_cd'])
		sheet.write(i+1,5,data[i]['a_amount'])

		if request.session.get('authority_level') == 1 or request.session.get('dept_name') == '设备购买部':
			sheet.write(i+1,6,data[i]['a_price'])
			sheet.write(i+1,7,data[i]['a_currency'])
		else:
			sheet.write(i+1,6,'***')
			sheet.write(i+1,7,'***')

		sheet.write(i+1,8,data[i]['a_out_time'])
		sheet.write(i+1,9,data[i]['a_purchase_time'])
		sheet.write(i+1,10,data[i]['a_brand'])
		sheet.write(i+1,11,data[i]['a_supplier'])
		sheet.write(i+1,12,data[i]['a_origin_loc'])
		sheet.write(i+1,13,data[i]['a_action_loc'])
		sheet.write(i+1,14,data[i]['a_action_state'])
		sheet.write(i+1,15,data[i]['a_model'])
		sheet.write(i+1,16,data[i]['a_action_user'])

		a_record_time = data[i]['a_record_time']
		if a_record_time and len(a_record_time) > 10:
			a_record_time = a_record_time[:10]

		sheet.write(i+1,17,a_record_time)
		sheet.write(i+1,18,data[i]['a_opr_user'])
		sheet.write(i+1,19,data[i]['a_budget'])
		sheet.write(i+1,20,data[i]['a_referendum'])
		sheet.write(i+1,21,data[i]['a_po_cd'])
		sheet.write(i+1,22,data[i]['a_sap_cd'])
		sheet.write(i+1,23,data[i]['a_project_cd'])
		sheet.write(i+1,24,data[i]['a_funds_type'])
		sheet.write(i+1,25,data[i]['a_action_charge'])
		sheet.write(i+1,26,data[i]['a_action_remark'])

	#在服务器端保存Excel文件
	filename = '资产在线移动信息导出_{0}.xls'.format(u_nstd_name)
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


#获取在库数据
def get_in_storage_data(request):
	a_cd = request.GET.get('a_cd')
	a_action_loc = request.GET.get('a_action_loc')
	startDate = request.GET.get('startDate')
	endDate = request.GET.get('endDate')
	if endDate:
		endDate += ' 23:59:59'
	page = int(request.GET.get('page'))
	limit = int(request.GET.get('limit'))
	data = {"code": 0,"msg": "","count": 0,"data": []}
	data['data'],data['count'] = asset_general_models.get_in_storage_data(a_cd,a_action_loc,startDate,endDate,page,limit)
	return HttpResponse(json.dumps(data))

#导出在库数据
def instorage_export(request):
	a_cd = request.GET.get('a_cd')
	a_action_loc = request.GET.get('a_action_loc')
	startDate = request.GET.get('startDate')
	endDate = request.GET.get('endDate')
	if endDate:
		endDate += ' 23:59:59'
	u_name = request.session.get('u_nstd_name',None)
	data = asset_general_models.get_in_storage_export_data(a_cd,a_action_loc,startDate,endDate)
	f = xlwt.Workbook()
	sheet = f.add_sheet('sheet1',cell_overwrite_ok = True)
	title = ['资产番号','资产编号','资产名称','资产型号','机身号码','单位','价格','币种','出厂时间',
		'购入时间','品牌','供应商','当前部门','位置代码','状态','机种','预算号','请示书号',
		'PO号','SAP番号','工程代码','经费类别','记录时间','操作员','备注信息']

	#生成Excel头部信息
	for i in range(0,len(title)):
		sheet.write(0,i,title[i],common.set_style('Times New Roman',220,True))

	#将搜索数据写入Excel文件
	for i in range(0,len(data)):
		sheet.write(i+1,0,data[i]['a_cd'])
		sheet.write(i+1,1,data[i]['a_self_cd'])	
		sheet.write(i+1,2,data[i]['a_name'])
		sheet.write(i+1,3,data[i]['a_type_cd'])
		sheet.write(i+1,4,data[i]['a_fuselage_cd'])
		sheet.write(i+1,5,data[i]['a_amount'])

		if request.session.get('authority_level') == 1 or request.session.get('dept_name') == '设备购买部':
			sheet.write(i+1,6,data[i]['a_price'])
			sheet.write(i+1,7,data[i]['a_currency'])
		else:
			sheet.write(i+1,6,'***')
			sheet.write(i+1,7,'***')

		sheet.write(i+1,8,data[i]['a_out_time'])
		sheet.write(i+1,9,data[i]['a_purchase_time'])
		sheet.write(i+1,10,data[i]['a_brand'])
		sheet.write(i+1,11,data[i]['a_supplier'])
		sheet.write(i+1,12,'IDLE')
		sheet.write(i+1,13,data[i]['a_action_loc'])
		sheet.write(i+1,14,data[i]['a_action_state'])
		sheet.write(i+1,15,data[i]['a_model'])
		sheet.write(i+1,16,data[i]['a_budget'])
		sheet.write(i+1,17,data[i]['a_referendum'])
		sheet.write(i+1,18,data[i]['a_po_cd'])
		sheet.write(i+1,19,data[i]['a_sap_cd'])
		sheet.write(i+1,20,data[i]['a_project_cd'])
		sheet.write(i+1,21,data[i]['a_funds_type'])
		sheet.write(i+1,22,data[i]['a_record_time'])
		sheet.write(i+1,23,data[i]['a_user_id'])
		sheet.write(i+1,24,data[i]['a_remark'])

	#在服务器端保存Excel文件
	filename = '在库信息导出_{0}.xls'.format(u_name)
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

#获取在线数据
def get_online_data(request):
	a_cd = request.GET.get('a_cd')
	a_action_loc = request.GET.get('a_action_loc')
	startDate = request.GET.get('startDate')
	endDate = request.GET.get('endDate')
	if endDate:
		endDate += ' 23:59:59'
	page = int(request.GET.get('page'))
	limit = int(request.GET.get('limit'))
	data = {"code": 0,"msg": "","count": 0,"data": []}
	data['data'],data['count'] = asset_general_models.get_online_data(a_cd,a_action_loc,startDate,endDate,page,limit)
	return HttpResponse(json.dumps(data))

#导出在线数据
def online_export(request):
	a_cd = request.GET.get('a_cd')
	a_action_loc = request.GET.get('a_action_loc')
	startDate = request.GET.get('startDate')
	endDate = request.GET.get('endDate')
	if endDate:
		endDate += ' 23:59:59'
	u_nstd_name = request.session.get('u_nstd_name',None)
	data = asset_general_models.get_online_export_data(a_cd,a_action_loc,startDate,endDate)

	f = xlwt.Workbook()
	sheet = f.add_sheet('sheet1',cell_overwrite_ok = True)
	title = [
		'资产番号','资产编号','资产名称','资产型号','机身号码','单位','单价','币种',
		'出厂时间','购入时间','品牌','供应商','状态','当前部门','位置代码','使用机种',
		'工程代码','经费类别','记录时间','操作员','备注信息'
	]

	#生成Excel头部信息
	for i in range(0,len(title)):
		sheet.write(0,i,title[i],common.set_style('Times New Roman',220,True))

	#将搜索数据写入Excel文件
	for i in range(0,len(data)):
		sheet.write(i+1,0,data[i]['a_cd'])
		sheet.write(i+1,1,data[i]['a_self_cd'])	
		sheet.write(i+1,2,data[i]['a_name'])
		sheet.write(i+1,3,data[i]['a_type_cd'])
		sheet.write(i+1,4,data[i]['a_fuselage_cd'])
		sheet.write(i+1,5,data[i]['a_amount'])

		if request.session.get('authority_level') == 1 or request.session.get('dept_name') == '设备购买部':
			sheet.write(i+1,6,data[i]['a_price'])
			sheet.write(i+1,7,data[i]['a_currency'])
			sheet.write(i+1,11,data[i]['a_supplier'])
		else:
			sheet.write(i+1,6,'***')
			sheet.write(i+1,7,'***')
			sheet.write(i+1,11,'***')

		sheet.write(i+1,8,data[i]['a_out_time'])
		sheet.write(i+1,9,data[i]['a_purchase_time'])
		sheet.write(i+1,10,data[i]['a_brand'])
		sheet.write(i+1,12,data[i]['a_action_state'])
		sheet.write(i+1,13,data[i]['a_action_depart'])
		sheet.write(i+1,14,data[i]['a_action_loc'])
		sheet.write(i+1,15,data[i]['a_action_model'])
		sheet.write(i+1,16,data[i]['a_project_cd'])
		sheet.write(i+1,17,data[i]['a_funds_type'])
		sheet.write(i+1,18,data[i]['a_record_time'])
		sheet.write(i+1,19,data[i]['a_opr_user'])
		sheet.write(i+1,20,data[i]['a_action_remark'])

	#在服务器端保存Excel文件
	filename = '在线信息导出_{0}.xls'.format(u_nstd_name)
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

#公共导出Excel方法
def general_export(data,name,u_id):
	f = xlwt.Workbook()
	sheet = f.add_sheet('sheet1',cell_overwrite_ok = True)
	if name == '销售信息导出':
		a_action_supplier = '销售客户'
	elif name == '支给信息导出':
		a_action_supplier = '支给客户'
	title = ['资产番号','资产编号','资产名称','资产型号','机身号码','单位','币种','出厂时间','购入时间','品牌',
		'供应商',a_action_supplier,'位置代码','状态','机种','预算号','请示书号','PO号','SAP番号','工程代码','经费类别','记录时间',
		'操作员','备注信息']

	#生成Excel头部信息
	for i in range(0,len(title)):
		sheet.write(0,i,title[i],common.set_style('Times New Roman',220,True))

	#将搜索数据写入Excel文件
	for i in range(0,len(data)):
		sheet.write(i+1,0,data[i]['a_cd'])
		sheet.write(i+1,1,data[i]['a_self_cd'])	
		sheet.write(i+1,2,data[i]['a_name'])
		sheet.write(i+1,3,data[i]['a_type_cd'])
		sheet.write(i+1,4,data[i]['a_fuselage_cd'])
		sheet.write(i+1,5,data[i]['a_amount'])
		sheet.write(i+1,6,data[i]['a_currency'])
		sheet.write(i+1,7,data[i]['a_out_time'])
		sheet.write(i+1,8,data[i]['a_purchase_time'])
		sheet.write(i+1,9,data[i]['a_brand'])
		sheet.write(i+1,10,data[i]['a_supplier'])
		sheet.write(i+1,11,data[i]['a_action_supplier'])
		sheet.write(i+1,12,data[i]['a_action_loc'])
		sheet.write(i+1,13,data[i]['a_action_state'])
		sheet.write(i+1,14,data[i]['a_model'])
		sheet.write(i+1,15,data[i]['a_budget'])
		sheet.write(i+1,16,data[i]['a_referendum'])
		sheet.write(i+1,17,data[i]['a_po_cd'])
		sheet.write(i+1,18,data[i]['a_sap_cd'])
		sheet.write(i+1,19,data[i]['a_project_cd'])
		sheet.write(i+1,20,data[i]['a_funds_type'])
		sheet.write(i+1,21,data[i]['a_record_time'])
		sheet.write(i+1,22,data[i]['a_opr_user'])
		sheet.write(i+1,23,data[i]['a_action_remark'])

	#在服务器端保存Excel文件
	filename = '{0}_{1}.xls'.format(name,u_id)
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

#资产总账信息导出
def total_export(request):
	datestyle = xlwt.XFStyle()
	datetimestyle = xlwt.XFStyle()
	datestyle.num_format_str = 'yyyy-mm-dd'
	datetimestyle.num_format_str = 'yyyy-mm-dd hh:mm:ss'

	f = xlwt.Workbook()
	sheet = f.add_sheet('总账信息',cell_overwrite_ok = True)
	title = ['资产番号','资产编号','资产名称','资产型号','机身号码','单位','单价','币种','出厂时间',
		'购入时间','品牌','供应商','当前部门','位置代码','折旧类别','状态','购入机种','预算号','请示书号','PO号',
		'SAP番号','工程代码','经费类别','使用机种','操作日期','操作员','备注1','备注2','库存状态','是否计量']

	u_name = request.session.get('u_nstd_name',None)
	startDate = request.GET.get('startDate')
	endDate = request.GET.get('endDate')
	if endDate:
		endDate += ' 23:59:59'
	data = asset_general_models.total_export_data(startDate,endDate)

	#生成Excel头部信息
	for i in range(0,len(title)):
		sheet.write(0,i,title[i],common.set_style('Times New Roman',220,True))

	#将搜索数据写入Excel文件
	for i in range(0,len(data)):
		sheet.write(i+1,0,data[i]['a_cd'])
		sheet.write(i+1,1,data[i]['a_self_cd'])
		sheet.write(i+1,2,data[i]['a_name'])
		sheet.write(i+1,3,data[i]['a_type_cd'])
		sheet.write(i+1,4,data[i]['a_fuselage_cd'])
		sheet.write(i+1,5,data[i]['a_amount'])
		sheet.write(i+1,6,data[i]['a_price'])
		sheet.write(i+1,7,data[i]['a_currency'])

		if data[i]['a_out_time']:
			sheet.write(i+1,8,data[i]['a_out_time'],datestyle)
		else:
			sheet.write(i+1,8,data[i]['a_out_time'])

		if data[i]['a_purchase_time']:
			sheet.write(i+1,9,data[i]['a_purchase_time'],datestyle)
		else:
			sheet.write(i+1,9,data[i]['a_purchase_time'])

		sheet.write(i+1,10,data[i]['a_brand'])
		sheet.write(i+1,11,data[i]['a_supplier'])
		sheet.write(i+1,12,data[i]['a_action_depart'])
		
		if data[i]['a_action_type'] == '支给':
			sheet.write(i+1,13,data[i]['a_action_supplier'])
		else:
			sheet.write(i+1,13,data[i]['a_action_loc'])

		sheet.write(i+1,14,data[i]['a_action_category'])	#折旧类别
		sheet.write(i+1,15,data[i]['a_action_state'])
		sheet.write(i+1,16,data[i]['a_model'])
		sheet.write(i+1,17,data[i]['a_budget'])
		sheet.write(i+1,18,data[i]['a_referendum'])
		sheet.write(i+1,19,data[i]['a_po_cd'])
		sheet.write(i+1,20,data[i]['a_sap_cd'])
		sheet.write(i+1,21,data[i]['a_project_cd'])
		sheet.write(i+1,22,data[i]['a_funds_type'])
		sheet.write(i+1,23,data[i]['a_action_model'])

		if data[i]['a_record_time']:
			sheet.write(i+1,24,str(data[i]['a_record_time'])[:10],datetimestyle)
		else:
			sheet.write(i+1,24,data[i]['a_record_time'])

		sheet.write(i+1,25,data[i]['a_opr_user'])
		sheet.write(i+1,26,data[i]['a_remark'])
		sheet.write(i+1,27,data[i]['a_action_remark'])
		sheet.write(i+1,28,data[i]['a_action_type'])
		sheet.write(i+1,29,data[i]['a_need_cal'])
	#在服务器端保存Excel文件
	filename = '资产总账信息导出_{0}.xls'.format(u_name)
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

#操作记录查询页
def opr_his_search(request):
	return render(request,'nstd/general/opr_his_search.html')

#根据资产番号查询操作历史记录
def get_history_data(request):
	a_cd = request.GET.get('a_cd')
	data = {"code": 0,"msg": "","count": 1,"data": []}
	data["data"] = asset_general_models.get_history_data(a_cd)
	return HttpResponse(json.dumps(data))

#操作历史记录信息导出
def history_export(request):
	f = xlwt.Workbook()
	sheet = f.add_sheet('历史记录信息',cell_overwrite_ok = True)
	title = ['资产番号','编号','名称','型号','机身号码','单位','币种','价格','经费类别','出厂时间',
			'购入时间','品牌','供应商','PO号','SAP番号','工程代码','机种','预算号','请示书号',
			'记录时间','状态','所属部门','领用人员','退库人员','支给客户','销售客户','领用部门',
			'移动部门','原位置代码','新位置代码','主管确认','操作员','备注信息','操作类型']
	a_cd = request.GET.get('a_cd')
	u_name = request.session.get('u_nstd_name',None)
	data = asset_general_models.get_history_data(a_cd)

	#生成Excel头部信息
	for i in range(0,len(title)):
		sheet.write(0,i,title[i],common.set_style('Times New Roman',220,True))

	#将搜索数据写入Excel文件
	for i in range(0,len(data)):
		sheet.write(i+1,0,data[i]['a_cd'])
		sheet.write(i+1,1,data[i]['a_self_cd'])
		sheet.write(i+1,2,data[i]['a_name'])
		sheet.write(i+1,3,data[i]['a_type_cd'])
		sheet.write(i+1,4,data[i]['a_fuselage_cd'])
		sheet.write(i+1,5,data[i]['a_amount'])
		sheet.write(i+1,6,data[i]['a_currency'])
		sheet.write(i+1,7,data[i]['a_price'])
		sheet.write(i+1,8,data[i]['a_funds_type'])
		sheet.write(i+1,9,data[i]['a_out_time'])
		sheet.write(i+1,10,data[i]['a_purchase_time'])
		sheet.write(i+1,11,data[i]['a_brand'])
		sheet.write(i+1,12,data[i]['a_supplier'])
		sheet.write(i+1,13,data[i]['a_po_cd'])
		sheet.write(i+1,14,data[i]['a_sap_cd'])
		sheet.write(i+1,15,data[i]['a_project_cd'])
		sheet.write(i+1,16,data[i]['a_model'])
		sheet.write(i+1,17,data[i]['a_budget'])
		sheet.write(i+1,18,data[i]['a_referendum'])
		sheet.write(i+1,19,data[i]['a_record_time'])
		sheet.write(i+1,20,data[i]['a_action_state'])
		sheet.write(i+1,21,data[i]['a_depart'])
		if data[i]['a_action_type'] == '出库':
			sheet.write(i+1,22,data[i]['a_take_user'])		#领用人员
			sheet.write(i+1,26,data[i]['a_take_depart'])	#领用部门
		if data[i]['a_action_type'] == '退库':
			sheet.write(i+1,23,data[i]['a_back_user'])		#退库人员
		if data[i]['a_action_type'] == '支给':
			sheet.write(i+1,24,data[i]['a_zj_supplier'])	#支给客户
		if data[i]['a_action_type'] == '销售':
			sheet.write(i+1,25,data[i]['a_sale_supplier'])	#销售客户
		if data[i]['a_action_type'] == '移动':
			sheet.write(i+1,27,data[i]['a_move_depart'])	#移动部门
			sheet.write(i+1,28,data[i]['a_origin_loc'])		#原位置代码
		sheet.write(i+1,29,data[i]['a_action_loc'])			#新位置代码
		if data[i]['a_action_type'] != '入库':
			sheet.write(i+1,30,data[i]['a_action_charge'])
		sheet.write(i+1,31,data[i]['a_opr_user'])
		sheet.write(i+1,32,data[i]['a_action_remark'])
		sheet.write(i+1,33,data[i]['a_action_type'])

	#在服务器端保存Excel文件
	filename = '资产操作记录_{0}.xls'.format(u_name)
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