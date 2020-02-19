# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from app_nstd.models import asset_basefunc_models
from app_nstd.models import asset_calculate_models
from xlrd import xldate_as_tuple
from datetime import datetime as xldatetime
from config.models import common
from machinemanage.settings import BASE_DIR
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
from urllib import parse
import json,datetime,os,xlrd,xlwt
import mimetypes

#确认计量前查询
def get_is_need_cal(request):
	a_cd = request.GET.get('a_cd')
	data = asset_calculate_models.get_is_need_cal(a_cd)
	return HttpResponse(json.dumps(data))

#资产确认需计量
def confirmToCal(request):
	a_material_id = request.GET.get('a_material_id')
	a_need_cal = request.GET.get('a_need_cal')
	result = asset_calculate_models.confirmToCal(a_material_id,a_need_cal)
	return HttpResponse(json.dumps({'result':result}))

#获取要计量的CSV数据
def get_cal_csv_data(request):
	tmp_file = request.GET.get('tmp_file')
	#读取上传的Excel文件中的数据
	data = {"code":0,"msg":"","count":0,'data':[]}
	if tmp_file:
		workbook = xlrd.open_workbook(tmp_file)
		allsheets = workbook.sheets()
		if allsheets:
			sheet = allsheets[0]
			row_number = sheet.nrows
			for i in range(row_number):
				if i > 1:
					row_dict = {}
					a_cd = str(sheet.cell(i,0).value).split('.')[0]	  	     #资产番号
					row_dict['a_cd'] = a_cd
					row_dict['c_method'] = str(sheet.cell(i,1).value)	  	 #计量方式
					row_dict['c_date'] = get_excel_datetime(sheet,i,2)	     #计量日期
					row_dict['c_end_date'] = get_excel_datetime(sheet,i,3)   #到期日期
					row_dict['c_use_depart'] = str(sheet.cell(i,4).value)	 #使用部门
					row_dict['c_status'] = str(sheet.cell(i,5).value)	 	 #计量状态
					#计量证书号码
					row_dict['c_certificate'] = str(sheet.cell(i,6).value).split('.')[0]
					if a_cd:
						detail = asset_basefunc_models.is_instorage_by_a_cd(a_cd)
						a_need_cal = detail[11]
						if a_need_cal == 0:
							a_need_cal = '未确认'
						elif a_need_cal == 1:
							a_need_cal = '已确认'
						row_dict['a_material_id'] = detail[1]
						row_dict['a_name'] = detail[6]
						row_dict['a_type_cd'] = detail[7]
						row_dict['a_fuselage_cd'] = detail[9]
						row_dict['a_self_cd'] = detail[10]
						row_dict['a_need_cal'] = a_need_cal
					data['data'].append(row_dict)
		if os.path.exists(tmp_file):
			os.remove(tmp_file)
	return HttpResponse(json.dumps(data))

#批量添加计量数据
def cal_upload_add(request):
	table_data = request.POST.get('table_data')
	if table_data:
		table_data = json.loads(table_data)
	c_record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	c_opr_user = request.session.get('u_nstd_name',None)
	num = asset_calculate_models.cal_upload__add(table_data,c_opr_user,c_record_time)
	return HttpResponse(json.dumps({'num':num}))

#查询计量数据
def get_cal_data(request):
	a_cd = request.GET.get('a_cd')
	a_type_cd = request.GET.get('a_type_cd')
	c_date = request.GET.get('c_date')
	c_end_date = request.GET.get('c_end_date')
	c_certificate = request.GET.get('c_certificate')
	data = {
	  "code": 0,
  	  "msg": "",
      "count": 0,
	  "data": []
	}
	data["data"],data['count'] = asset_calculate_models.get_cal_data(a_cd,a_type_cd,c_date,c_end_date,c_certificate)
	return HttpResponse(json.dumps(data))

#计量导出
def cal_export(request):
	f = xlwt.Workbook()
	sheet = f.add_sheet('计量信息',cell_overwrite_ok = True)
	title = ['资产番号','资产型号','资产名称','资产编号','机身号码',
		'计量方式','计量日期','到期日期','使用部门','资产状态','计量证书','记录时间']
	a_cd = request.GET.get('a_cd')
	a_type_cd = request.GET.get('a_type_cd')
	c_date = request.GET.get('c_date')
	c_end_date = request.GET.get('c_end_date')
	c_certificate = request.GET.get('c_certificate')
	u_name = request.session.get('u_nstd_name',None)
	data,count = asset_calculate_models.get_cal_data(a_cd,a_type_cd,c_date,c_end_date,c_certificate)
	#生成Excel头部信息
	for i in range(0,len(title)):
		sheet.write(0,i,title[i],common.set_style('Times New Roman',220,True))

	#将搜索数据写入Excel文件
	for i in range(0,count):
		sheet.write(i+1,0,data[i]['a_cd'])
		sheet.write(i+1,1,data[i]['a_type_cd'])
		sheet.write(i+1,2,data[i]['a_name'])
		sheet.write(i+1,3,data[i]['a_self_cd'])
		sheet.write(i+1,4,data[i]['a_fuselage_cd'])
		sheet.write(i+1,5,data[i]['c_method'])
		sheet.write(i+1,6,data[i]['c_date'])
		sheet.write(i+1,7,data[i]['c_end_date'])
		sheet.write(i+1,8,data[i]['a_action_depart'])
		sheet.write(i+1,9,data[i]['c_status'])
		sheet.write(i+1,10,data[i]['c_certificate'])
		sheet.write(i+1,11,data[i]['c_record_time'])

	#在服务器端保存Excel文件
	filename = '资产计量导出_{0}.xls'.format(u_name)
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

#计量前查询
def get_cal_record(request):
	a_cd = request.GET.get('a_cd')
	data = {
	  "code": 0,
  	  "msg": "",
	  "data": []
	}
	data['data'] = asset_calculate_models.get_cal_record(a_cd)
	return HttpResponse(json.dumps(data))

#计量更改前查询
def cal_update_detail(request):
	a_cd = request.GET.get('a_cd')
	data = asset_calculate_models.cal_update_detail(a_cd)
	return HttpResponse(json.dumps(data))

#添加计量信息
def cal_update(request):
	c_id = request.POST.get('c_id')
	c_method = request.POST.get('c_method')
	c_date = request.POST.get('c_date')
	c_end_date = request.POST.get('c_end_date')
	c_use_depart = request.POST.get('c_use_depart')
	c_status = request.POST.get('c_status')
	c_certificate = request.POST.get('c_certificate')
	a_cd = request.POST.get('a_cd')
	a_fuselage_cd = request.POST.get('a_fuselage_cd')

	result = asset_calculate_models.cal_update(c_id,c_method,c_date,c_end_date,c_use_depart,c_status,c_certificate,a_cd,a_fuselage_cd)
	return HttpResponse(json.dumps({'result':result}))

#Excel日期格式转化
def get_excel_datetime(sheet,i,j):
	ctype = sheet.cell(i,j).ctype 		#表格的数据类型
	cell = sheet.cell_value(i,j)
	if ctype == 2 and cell % 1 == 0:	#整形
		cell = int(cell)
	elif ctype == 3:
		date = xldatetime(*xldate_as_tuple(cell,0))
		cell = date.strftime('%Y-%m-%d')
	elif ctype == 4:
		cell = True if cell == 1 else False
	return cell