# -*- coding:utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from app_nstd.models import asset_baseinfo_models
from app_nstd.models import asset_basefunc_models
import json,datetime,xlrd,os

#读取资产位置数据（分页情况）
def get_pos_data(request):
	page = request.GET.get('page')
	limit = request.GET.get('limit')
	page = int(page)
	limit = int(limit)
	data = {"code": 0,"msg": "","count": 1000,"data": []}
	pos_data,count = asset_baseinfo_models.get_pos_data(page,limit)
	data['count'] = count
	data['data'] = pos_data
	return HttpResponse(json.dumps(data))

#获取所有资产位置数据（不分页）
def get_all_pos_data(request):
	data = {
	  "code": 0,
	  "msg": "",
	  "count": 1000,
	  "data": []
	}
	data['data'] = asset_baseinfo_models.get_all_pos_data()
	return HttpResponse(json.dumps(data))

#添加资产位置
def add_pos(request):
	p_building = request.GET.get('p_building')
	p_floor = request.GET.get('p_floor')
	p_area = request.GET.get('p_area')
	p_column = request.GET.get('p_column')
	p_position = request.GET.get('p_position')
	p_code = request.GET.get('p_code')
	result = asset_baseinfo_models.add_pos(p_building,p_floor,p_area,p_column,p_position,p_code)
	return HttpResponse(json.dumps({'result':result}))

#删除资产位置
def asset_pos_del(request):
	p_id = request.GET.get('p_id')
	result = asset_baseinfo_models.asset_pos_del(p_id)
	return HttpResponse(json.dumps({'result':result}))

#添加部门
def add_depart(request):
	d_id = request.GET.get('d_id')
	d_name = request.GET.get('d_name')
	result = asset_baseinfo_models.add_depart(d_id,d_name)
	return HttpResponse(json.dumps({'result':result}))

#搜索部门
def search_depart(request):
	depart_list = asset_baseinfo_models.search_depart()
	return HttpResponse(json.dumps({'depart_list':depart_list,'data_list':depart_list}))

#编辑部门
def edit_depart(request):
	d_id = request.GET.get('d_id')
	d_name = request.GET.get('d_name')
	result = asset_baseinfo_models.edit_depart(d_id,d_name)
	return HttpResponse(json.dumps({'result':result}))

#删除部门
def del_depart(request):
	del_dept_list = request.GET.get('del_dept_list')
	if del_dept_list:
		del_dept_list = json.loads(del_dept_list)
	result = asset_baseinfo_models.del_depart(del_dept_list)
	return HttpResponse(json.dumps({'result':result}))

#编辑位置
def edit_pos(request):
	p_id = request.POST.get('p_id')
	edit_p_building = request.POST.get('edit_p_building')
	edit_p_floor = request.POST.get('edit_p_floor')
	edit_p_area = request.POST.get('edit_p_area')
	edit_p_column = request.POST.get('edit_p_column')
	edit_p_position = request.POST.get('edit_p_position')
	edit_p_code = request.POST.get('edit_p_code')

	result = asset_baseinfo_models.edit_pos(p_id,edit_p_building,edit_p_floor,edit_p_area,
		edit_p_column,edit_p_position,edit_p_code)
	return HttpResponse(json.dumps({'result':result}))

#添加供应商
def add_supplier(request):
	a_supplier = request.GET.get('a_supplier')
	result = asset_baseinfo_models.add_supplier(a_supplier)
	return HttpResponse(json.dumps({'result':result}))

#搜索供应商
def search_supplier(request):
	data_list = asset_baseinfo_models.search_supplier()
	return HttpResponse(json.dumps({'data_list':data_list}))

#添加资产类别
def add_category(request):
	a_category = request.GET.get('a_category')
	result = asset_baseinfo_models.add_category(a_category)
	return HttpResponse(json.dumps({'result':result}))

#搜索资产类别
def search_category(request):
	data_list = asset_baseinfo_models.search_category()
	return HttpResponse(json.dumps({'data_list':data_list}))

#添加领用人员
def add_action_user(request):
	u_name = request.GET.get('u_name')
	result = asset_baseinfo_models.add_action_user(u_name)
	return HttpResponse(json.dumps({'result':result}))

#搜索领用人员
def search_action_user(request):
	data_list = asset_baseinfo_models.search_action_user()
	return HttpResponse(json.dumps({'data_list':data_list}))

#添加主管人员
def add_action_charge(request):
	c_name = request.GET.get('c_name')
	result = asset_baseinfo_models.add_action_charge(c_name)
	return HttpResponse(json.dumps({'result':result}))

#搜索主管人员
def search_action_charge(request):
	data_list = asset_baseinfo_models.search_action_charge()
	return HttpResponse(json.dumps({'data_list':data_list}))

#搜索销售客户
def search_client(request):
	data_list = asset_baseinfo_models.search_client()
	return HttpResponse(json.dumps({'data_list':data_list}))

#索索位置信息
def search_pos(request):
	pos_type = request.GET.get('pos_type')
	data_list = asset_baseinfo_models.search_pos(pos_type)
	return HttpResponse(json.dumps({'data_list':data_list}))

#添加销售客户
def add_client(request):
	c_name = request.GET.get('c_name')
	result = asset_baseinfo_models.add_client(c_name)
	return HttpResponse(json.dumps({'result':result}))

#资产转换页面
def asset_convert_page(request):
	return render(request,'nstd/baseinfo/asset_convert_page.html')

def edit_base_page(request):
	return render(request,'nstd/edit/edit_base_page.html')

def edit_out_page(request):
	return render(request,'nstd/edit/edit_out_page.html')

def edit_back_page(request):
	return render(request,'nstd/edit/edit_back_page.html')

def edit_zj_page(request):
	return render(request,'nstd/edit/edit_zj_page.html')

def edit_zj_back_page(request):
	return render(request,'nstd/edit/edit_zj_back_page.html')

def edit_loan_back_page(request):
	return render(request,'nstd/edit/edit_loan_back_page.html')

def edit_storage_move_page(request):
	return render(request,'nstd/edit/edit_storage_move_page.html')

def edit_online_move_page(request):
	return render(request,'nstd/edit/edit_online_move_page.html')

def edit_pos_page(request):
	return render(request,'nstd/edit/edit_pos_page.html')

def edit_state_page(request):
	return render(request,'nstd/edit/edit_state_page.html')

def edit_category_page(request):
	return render(request,'nstd/edit/edit_category_page.html')

def edit_depart_page(request):
	return render(request,'nstd/edit/edit_depart_page.html')

#资产转换前详情查询
def before_convert_detail(request):
	a_origin_cd = request.GET.get('a_origin_cd')
	data = asset_baseinfo_models.before_convert_detail(a_origin_cd)
	return HttpResponse(json.dumps(data))

#验证资产番号是否重复
def is_a_cd_repeat(request):
	a_cd = request.GET.get('a_cd')
	result = asset_baseinfo_models.is_a_cd_repeat(a_cd)
	return HttpResponse(json.dumps({'result':result}))

#资产转换
def asset_convert(request):
	#a_action_id = request.GET.get('a_action_id')
	a_material_id = request.GET.get('a_material_id')
	a_origin_cd = request.GET.get('a_origin_cd')
	a_cd = request.GET.get('a_cd')
	a_opr_user = request.session.get('u_nstd_name')
	a_record_time =datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	#result = asset_baseinfo_models.asset_convert(a_action_id,a_material_id,a_origin_cd,a_cd,a_opr_user,a_record_time)
	result = asset_baseinfo_models.asset_convert(a_material_id,a_origin_cd,a_cd,a_opr_user,a_record_time)
	return HttpResponse(json.dumps({'result':result}))

#查询资产详情
def get_asset_detail(request):
	a_cd = request.GET.get('a_cd')
	data = asset_baseinfo_models.get_asset_detail(a_cd)
	return HttpResponse(json.dumps(data))

#资产更新
def asset_update(request):
	a_material_id = request.POST.get('a_material_id')
	a_action_id = request.POST.get('a_action_id')
	a_type_cd = request.POST.get('a_type_cd')
	a_name = request.POST.get('a_name')
	a_self_cd = request.POST.get('a_self_cd')
	a_fuselage_cd = request.POST.get('a_fuselage_cd')
	a_project_cd = request.POST.get('a_project_cd')
	a_action_category = request.POST.get('a_action_category')
	a_action_state = request.POST.get('a_action_state')
	a_action_loc = request.POST.get('a_action_loc')
	a_po_cd = request.POST.get('a_po_cd')
	a_referendum = request.POST.get('a_referendum')
	a_funds_type = request.POST.get('a_funds_type')
	a_model = request.POST.get('a_model')
	a_supplier = request.POST.get('a_supplier')
	a_action_depart = request.POST.get('a_action_depart')
	a_action_remark = request.POST.get('a_action_remark')
	result = asset_baseinfo_models.asset_update(a_material_id,a_action_id,a_type_cd,a_name,
		a_self_cd,a_fuselage_cd,a_project_cd,a_action_category,a_action_state,a_action_loc,
		a_po_cd,a_referendum,a_funds_type,a_model,a_supplier,a_action_depart,a_action_remark)
	return HttpResponse(json.dumps({'result':result}))

#批量修改前查询(暂时不用了)
def get_modify_csv_data(request):
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
					a_cd = str(sheet.cell(i,0).value).split('.')[0]			    #资产番号
					row_dict['a_cd'] = a_cd
					row_dict['a_category'] = str(sheet.cell(i,1).value)			#资产分类
					row_dict['a_action_state'] = str(sheet.cell(i,2).value)		#资产状态
					row_dict['a_action_loc'] = str(sheet.cell(i,3).value)		#资产位置
					if a_cd:
						detail = asset_basefunc_models.is_instorage_by_a_cd(a_cd)
						row_dict['a_action_type'] = detail[0]
						row_dict['a_action_id'] = detail[12]
						row_dict['a_name'] = detail[6]
						row_dict['a_type_cd'] = detail[7]
					data['data'].append(row_dict)
		if os.path.exists(tmp_file):
			os.remove(tmp_file)
	return HttpResponse(json.dumps(data))

#批量修改资产位置前查询
def get_modify_1_csv_data(request):
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
					a_cd = str(sheet.cell(i,0).value).split('.')[0]			    #资产番号
					row_dict['a_cd'] = a_cd
					row_dict['a_action_depart'] = str(sheet.cell(i,1).value)	#当前部门
					row_dict['a_action_loc'] = str(sheet.cell(i,2).value)		#资产位置
					row_dict['a_action_model'] = str(sheet.cell(i,3).value)		#使用机种
					row_dict['a_action_remark'] = str(sheet.cell(i,4).value)	#备注信息
					if a_cd:
						detail = asset_basefunc_models.is_instorage_by_a_cd(a_cd)
						row_dict['a_action_type'] = detail[0]
						row_dict['a_action_id'] = detail[12]
						row_dict['a_name'] = detail[6]
						row_dict['a_type_cd'] = detail[7]
					data['data'].append(row_dict)
		if os.path.exists(tmp_file):
			os.remove(tmp_file)
	return HttpResponse(json.dumps(data))

#资产冲销前读取资产番号
def get_modify_2_csv_data(request):
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
					a_cd = str(sheet.cell(i,0).value).split('.')[0]			    #资产番号
					row_dict['a_cd'] = a_cd
					if a_cd:
						detail = asset_basefunc_models.is_instorage_by_a_cd(a_cd)
						row_dict['a_action_type'] = detail[0]
						row_dict['a_action_id'] = detail[12]
						row_dict['a_name'] = detail[6]
						row_dict['a_type_cd'] = detail[7]
					data['data'].append(row_dict)
		if os.path.exists(tmp_file):
			os.remove(tmp_file)
	return HttpResponse(json.dumps(data))

#批量修改资产单价、币种
def get_modify_3_csv_data(request):
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
					a_cd = str(sheet.cell(i,0).value).split('.')[0]			    #资产番号
					row_dict['a_cd'] = a_cd
					row_dict['a_price'] = str(sheet.cell(i,1).value).split('.')[0]
					row_dict['a_currency'] = str(sheet.cell(i,2).value).split('.')[0]
					if a_cd:
						detail = asset_basefunc_models.is_instorage_by_a_cd(a_cd)
						row_dict['a_action_type'] = detail[0]
						row_dict['a_name'] = detail[6]
						row_dict['a_type_cd'] = detail[7]
					data['data'].append(row_dict)
		if os.path.exists(tmp_file):
			os.remove(tmp_file)
	return HttpResponse(json.dumps(data))

#批量修改资产资产状态、资产类别
def get_modify_4_csv_data(request):
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
					a_cd = str(sheet.cell(i,0).value).split('.')[0]			    #资产番号
					row_dict['a_cd'] = a_cd
					row_dict['a_action_state'] = str(sheet.cell(i,1).value).split('.')[0]
					row_dict['a_action_category'] = str(sheet.cell(i,2).value).split('.')[0]
					if a_cd:
						detail = asset_basefunc_models.is_instorage_by_a_cd(a_cd)
						row_dict['a_action_type'] = detail[0]
						row_dict['a_name'] = detail[6]
						row_dict['a_type_cd'] = detail[7]
					data['data'].append(row_dict)
		if os.path.exists(tmp_file):
			os.remove(tmp_file)
	return HttpResponse(json.dumps(data))

#批量更新
def upload_modify(request):
	table_data = request.POST.get('table_data')
	if table_data:
		table_data = json.loads(table_data)
	num = asset_baseinfo_models.upload_modify(table_data)
	return HttpResponse(json.dumps({'num':num}))

#批量修改资产位置
def upload_modify_1(request):
	table_data = request.POST.get('table_data')
	if table_data:
		table_data = json.loads(table_data)
	num = asset_baseinfo_models.upload_modify_1(table_data)
	return HttpResponse(json.dumps({'num':num}))

#资产批量冲消
def upload_modify_2(request):
	table_data = request.POST.get('table_data')
	if table_data:
		table_data = json.loads(table_data)
	num = asset_baseinfo_models.upload_modify_2(table_data)
	return HttpResponse(json.dumps({'num':num}))

#资产批量价格、币种
def upload_modify_3(request):
	table_data = request.POST.get('table_data')
	if table_data:
		table_data = json.loads(table_data)
	num = asset_baseinfo_models.upload_modify_3(table_data)
	return HttpResponse(json.dumps({'num':num}))

#资产批量价格、币种
def upload_modify_4(request):
	table_data = request.POST.get('table_data')
	if table_data:
		table_data = json.loads(table_data)
	num = asset_baseinfo_models.upload_modify_4(table_data)
	return HttpResponse(json.dumps({'num':num}))

#批量转换资产(修改资产番号)
def upload_convert(request):
	a_action_type = 10
	a_opr_user = request.session.get('u_nstd_name')
	a_record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	table_data = request.POST.get('table_data')
	if table_data:
		table_data = json.loads(table_data)
	num = asset_baseinfo_models.upload_convert(table_data,a_action_type,a_opr_user,a_record_time)
	return HttpResponse(json.dumps({'num':num}))

#获取所有使用机种
def get_mobile_model(request):
	data = {"code":0,"msg":"","count":0,'data':[]}
	data['data'] = asset_baseinfo_models.get_mobile_model()
	return HttpResponse(json.dumps(data))

#添加使用机种
def add_action_model(request):
	a_action_model = request.GET.get('a_action_model')
	opr_user = request.session.get('u_nstd_name')
	add_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	if opr_user:
		result = asset_baseinfo_models.add_action_model(a_action_model,opr_user,add_time)
		return HttpResponse(json.dumps({'result':result}))
	else:
		return HttpResponse(json.dumps({'result':False, 'msg':'您未登陆，请先登陆!'}))

#删除使用机种
def action_model_del(request):
	m_id = request.GET.get('m_id')
	result = asset_baseinfo_models.action_model_del(m_id)
	return HttpResponse(json.dumps({'result':result}))