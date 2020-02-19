# -*- coding:utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from app_nstd.models import asset_basefunc_models
from xlrd import xldate_as_tuple
from datetime import datetime as xldatetime
import json,datetime,os,xlrd

#设备入库记账
def asset_add(request):
	a_cd = request.POST.get('a_cd')
	a_self_cd = request.POST.get('a_self_cd')
	a_name = request.POST.get('a_name')
	a_type_cd = request.POST.get('a_type_cd')
	a_fuselage_cd = request.POST.get('a_fuselage_cd')
	a_price = request.POST.get('a_price')
	a_currency = request.POST.get('a_currency')
	a_out_time = request.POST.get('a_out_time')
	a_purchase_time = request.POST.get('a_purchase_time')
	a_amount = request.POST.get('a_amount')
	a_funds_type = request.POST.get('a_funds_type')
	a_project_cd = request.POST.get('a_project_cd')
	a_depart = request.POST.get('a_depart')
	a_budget = request.POST.get('a_budget')
	a_model = request.POST.get('a_model')
	a_po_cd = request.POST.get('a_po_cd')
	a_brand = request.POST.get('a_brand')
	a_supplier = request.POST.get('a_supplier')
	a_sap_cd = request.POST.get('a_sap_cd')
	a_status = request.POST.get('a_status')
	a_category = request.POST.get('a_category')
	a_referendum = request.POST.get('a_referendum')
	a_loc_cd = request.POST.get('a_loc_cd')
	a_need_cal = request.POST.get('a_need_cal')
	a_b_nstd = request.POST.get('a_b_nstd')
	a_remark = request.POST.get('a_remark')
	a_record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	a_user_id = request.session.get('u_nstd_id',None)
	if not a_user_id:
		return HttpResponse(json.dumps({'result':False,'msg':'您未登录或登录信息失效，请先登录!'}))
	else:
		data = asset_basefunc_models.asset_add(a_cd,a_self_cd,a_name,a_type_cd,a_fuselage_cd,a_amount,
			a_price,a_currency,a_out_time,a_purchase_time,a_funds_type,a_project_cd,a_depart,a_budget,
			a_model,a_po_cd,a_brand,a_supplier,a_sap_cd,a_status,a_category,a_referendum,a_loc_cd,
			a_need_cal,a_b_nstd,a_remark,a_user_id,a_record_time)
		return HttpResponse(json.dumps(data))

#支给设备 -> 通过资产番号搜索全局信息
def before_zj_detail(request):
	a_cd = request.GET.get('a_cd')
	data = asset_basefunc_models.before_zj_detail(a_cd)
	return HttpResponse(json.dumps(data))

#支给前验证
def before_action_vde(request):
	a_material_id = request.GET.get('a_material_id')
	data = asset_basefunc_models.before_action_vde(a_material_id)
	return HttpResponse(json.dumps(data))

#支给归还 -> 通过资产番号搜索全局信息
def get_zj_detail(request):
	a_cd = request.GET.get('a_cd')
	data = asset_basefunc_models.get_zj_detail(a_cd)
	return HttpResponse(json.dumps(data))

#确认支给
def action_zj(request):
	a_cd = request.GET.get('a_cd')
	a_action_supplier = request.GET.get('a_action_supplier')
	a_material_id = request.GET.get('a_material_id')
	a_action_loc = request.GET.get('a_action_loc')
	a_action_state = request.GET.get('a_action_state')
	a_opr_user = request.session.get('u_nstd_name',None)
	a_record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	a_action_type = 1
	if not a_opr_user:
		return HttpResponse(json.dumps({'result':False,'msg':'您未登录或登录信息失效，请先登录!'}))
	else:
		result = asset_basefunc_models.action_zj(a_cd,a_action_type,a_record_time,
			a_action_supplier,a_opr_user,a_material_id,a_action_loc,a_action_state)
		return HttpResponse(json.dumps({'result':result}))

#支给归还
def revert_zj(request):
	a_cd = request.GET.get('a_cd')
	a_action_loc = request.GET.get('a_action_loc')
	a_fuselage_cd = request.GET.get('a_fuselage_cd')
	a_action_state = request.GET.get('a_action_state')
	a_action_remark = request.GET.get('a_action_remark')
	a_opr_user = request.session.get('u_nstd_name',None)
	a_record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	a_action_type = 2
	if not a_opr_user:
		return HttpResponse(json.dumps({'result':False,'msg':'您未登录或登录信息失效，请先登录!'}))
	else:
		result = asset_basefunc_models.revert_zj(a_cd,a_action_loc,a_fuselage_cd,a_action_state,
			a_action_remark,a_opr_user,a_record_time,a_action_type)
		return HttpResponse(json.dumps({'result':result}))

#设备出库记账前查询
def get_out_detail(request):
	a_cd = request.GET.get('a_cd')
	data = asset_basefunc_models.get_out_detail(a_cd)
	return HttpResponse(json.dumps(data))

#设备退库记账前查询
def get_back_detail(request):
	a_cd = request.GET.get('a_cd')
	data = asset_basefunc_models.get_back_detail(a_cd)
	return HttpResponse(json.dumps(data))

#资产出库前验证
def before_out_vde(request):
	a_material_id = request.GET.get('a_material_id')
	data = asset_basefunc_models.before_out_vde(a_material_id)
	return HttpResponse(json.dumps(data))

#资产出库
def asset_out(request):
	a_material_id = request.POST.get('a_material_id')
	a_action_depart = request.POST.get('a_action_depart')
	a_action_user = request.POST.get('a_action_user')
	a_action_charge = request.POST.get('a_action_charge')
	a_action_loc = request.POST.get('a_action_loc')
	a_action_model = request.POST.get('a_action_model')
	a_action_state = request.POST.get('a_action_state')
	a_action_remark = request.POST.get('a_action_remark')
	a_action_type = 5
	a_record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	a_opr_user = request.session.get('u_nstd_name',None)
	if not a_opr_user:
		return HttpResponse(json.dumps({'result':False,'msg':'您未登录或登录信息失效，请先登录'}))
	else:
		result = asset_basefunc_models.asset_out(a_material_id,a_record_time,a_action_depart,
			a_action_user,a_action_charge,a_action_loc,a_action_state,a_action_remark,
			a_action_type,a_opr_user,a_action_model)
		return HttpResponse(json.dumps({'result':result}))

#资产退库前验证
def before_back_vde(request):
	a_material_id = request.GET.get('a_material_id')
	data = asset_basefunc_models.before_back_vde(a_material_id)
	return HttpResponse(json.dumps(data))

#资产退库
def asset_back(request):
	a_cd = request.GET.get('a_cd')
	a_material_id = request.GET.get('a_material_id')
	a_action_user = request.GET.get('a_action_user')
	a_action_state = request.GET.get('a_action_state')
	a_action_charge = request.GET.get('a_action_charge')
	a_action_loc = request.GET.get('a_action_loc')
	a_action_category = request.GET.get('a_action_category')
	a_action_remark = request.GET.get('a_action_remark')
	a_action_type = 4
	a_record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	a_opr_user = request.session.get('u_nstd_name',None)
	if not a_opr_user:
		return HttpResponse(json.dumps({'result':False,'msg':'您未登录或登录信息失效，请先登录'}))
	result = asset_basefunc_models.asset_back(a_cd,a_material_id,a_action_user,
		a_action_state,a_action_charge,a_action_loc,a_action_remark,
		a_action_type,a_record_time,a_opr_user,a_action_category)
	return HttpResponse(json.dumps({'result':result}))

#借用归还前查询
def loan_revert_detail(request):
	a_cd = request.GET.get('a_cd')
	data = asset_basefunc_models.loan_revert_detail(a_cd)
	return HttpResponse(json.dumps(data))

#借用设备归还
def loan_revert(request):
	a_cd = request.GET.get('a_cd')
	a_action_state = request.GET.get('a_action_state')
	a_material_id = request.GET.get('a_material_id')
	a_action_type = 3
	a_record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	a_opr_user = request.session.get('u_nstd_name',None)
	if not a_opr_user:
		return HttpResponse(json.dumps({'result':False,'msg':'您未登录或登录信息失效，请先登录'}))
	else: 
		result = asset_basefunc_models.loan_revert(a_cd,a_action_state,a_material_id,a_action_type,a_record_time,a_opr_user)
	return HttpResponse(json.dumps({'result':result}))

#销售记账详情查询
def get_sale_detail(request):
	a_cd = request.GET.get('a_cd')
	data = asset_basefunc_models.get_sale_detail(a_cd)
	return HttpResponse(json.dumps(data))

#设备销售记账
def asset_sale(request):
	a_cd = request.GET.get('a_cd')
	a_action_supplier = request.GET.get('a_action_supplier')
	a_material_id = request.GET.get('a_material_id')
	a_action_remark = request.GET.get('a_action_remark')
	a_record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	a_action_type = 6
	a_opr_user = request.session.get('u_nstd_name',None)
	if not a_opr_user:
		return HttpResponse(json.dumps({'result':False,'msg':'您未登录或登录信息失效，请先登录'}))

	result = asset_basefunc_models.asset_sale(a_cd,a_action_supplier,a_material_id,a_action_remark,a_record_time,a_action_type,a_opr_user)
	return HttpResponse(json.dumps({'result':result}))

#资产报废记账
def asset_scrap(request):
	a_cd = request.GET.get('a_cd')
	a_material_id = request.GET.get('a_material_id')
	a_action_remark = request.GET.get('a_action_remark')
	a_record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	a_action_type = 7
	a_opr_user = request.session.get('u_nstd_name',None)
	if not a_opr_user:
		return HttpResponse(json.dumps({'result':False,'msg':'您未登录或登录信息失效，请先登录'}))

	result = asset_basefunc_models.asset_scrap(a_cd,a_material_id,
				a_action_remark,a_record_time,a_action_type,a_opr_user)
	return HttpResponse(json.dumps({'result':result}))

#资产移动前搜索详情
def asset_move_detail(request):
	a_cd = request.GET.get('a_cd')
	data = asset_basefunc_models.asset_move_detail(a_cd)
	return HttpResponse(json.dumps(data))

#资产移动
def asset_move(request):
	asset_list = request.GET.get('asset_list')
	a_action_user = request.GET.get('a_action_user')
	a_action_charge = request.GET.get('a_action_charge')
	a_opr_user = request.session.get('u_nstd_name',None)
	a_record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	a_action_type = request.GET.get('a_action_type')
	if a_action_type:
		a_action_type = int(a_action_type)

	if asset_list:
		asset_list = json.loads(asset_list)
	if not a_opr_user:
		return HttpResponse(json.dumps({'result':False,'msg':'您未登录或登录信息失效，请先登录'}))
	result = asset_basefunc_models.asset_move(asset_list,a_action_user,a_action_charge,
		a_opr_user,a_record_time,a_action_type)
	return HttpResponse(json.dumps({'result':result}))

#添加资产模板下载
def download_template(request):
    param = request.GET.get('param')
    if param == 'add':
        param = '录入模板'
    elif param == 'out':
        param = '出库模板'
    elif param == 'back':
        param = '退库模板'
    elif param == 'zj':
        param = '支给模板'
    elif param == 'zj_revert':
        param = '支给归还'
    elif param == 'loan_revert':
        param = '借用归还'
    elif param == 'sale':
        param = '销售模板'
    elif param == 'scrap':
        param = '报废模板'
    elif param == 'instorage_move':
        param = '库房移动模板'
    elif param == 'online_move':
        param = '在线移动模板'
    elif param == 'add_out':
        param = '在线设备导入模板'
    elif param == 'calculate_add':
        param = '计量录入模板'
    elif param == 'asset_modify':
    	param = '资产修改模板'
    elif param == 'asset_convert':
    	param = '资产转换模板'
    elif param == 'asset_modify_1':
    	param = '当前部门_资产位置_使用机种_备注_修改模板'
    elif param == 'asset_modify_2':
    	param = '资产冲消模板'
    elif param == 'asset_modify_3':
    	param = '价格_币种_修改模板'
    elif param == 'asset_modify_4':
    	param = '资产状态_折旧类别_修改模板'
    elif param == 'print':
    	param = 'CLodop打印插件.zip'

    import mimetypes
    from django.http import StreamingHttpResponse
    from wsgiref.util import FileWrapper
    from urllib import parse

    if param == 'CLodop打印插件.zip':
    	the_file = 'app_nstd/templatefolder/{0}'.format(param)
    else:
    	the_file = 'app_nstd/templatefolder/{0}.xls'.format(param)
    chunk_size = 8192
    response = StreamingHttpResponse(FileWrapper(open(the_file, 'rb'), chunk_size),
            content_type=mimetypes.guess_type(the_file)[0])
    response['Content-Length'] = os.path.getsize(the_file)
    if param == 'CLodop打印插件.zip':
    	response['Content-Disposition'] = "attachment; filename="+parse.quote(param)
    else:
    	response['Content-Disposition'] = "attachment; filename="+parse.quote(param)+".xls"
    return response

#文件上传保存
def upload_file(request):
	from machinemanage.settings import MEDIA_ROOT
	from django.core.files.base import ContentFile
	from django.core.files.storage import default_storage
	result = False
	try:
		file = request.FILES.get('file')
		file_path = os.path.join(MEDIA_ROOT,file.name).replace('\\','/')
		path = default_storage.save(file_path, ContentFile(file.read()))
		tmp_file = os.path.join(MEDIA_ROOT, path)	#存储临时文件目录及文件名
		result = True
	except Exception as e:
		print(e)
	return HttpResponse(json.dumps({'result':result,'tmp_file':tmp_file}))

#跳转加载上传数据表格页面
def upload_table_page(request):
	flag = request.GET.get('flag')
	tmp_file = request.GET.get('tmp_file')
	if flag == 'add':
		return render(request,'nstd/uploadtable/upload_add.html',{'tmp_file':tmp_file})
	elif flag == 'out':
		return render(request,'nstd/uploadtable/upload_out.html',{'tmp_file':tmp_file})
	elif flag == 'back':
		return render(request,'nstd/uploadtable/upload_back.html',{'tmp_file':tmp_file})
	elif flag == 'zj':
		return render(request, 'nstd/uploadtable/upload_zj.html',{'tmp_file':tmp_file})
	elif flag == 'zj_revert':
		return render(request, 'nstd/uploadtable/upload_zj_revert.html',{'tmp_file':tmp_file})
	elif flag == 'loan_revert':
		return render(request, 'nstd/uploadtable/upload_loan_revert.html',{'tmp_file':tmp_file})
	elif flag == 'sale':
		return render(request, 'nstd/uploadtable/upload_sale.html',{'tmp_file':tmp_file})
	elif flag == 'scrap':
		return render(request, 'nstd/uploadtable/upload_scrap.html',{'tmp_file':tmp_file})
	elif flag == 'instorage_move':
		return render(request, 'nstd/uploadtable/upload_instorage_move.html',{'tmp_file':tmp_file})
	elif flag == 'online_move':
		return render(request, 'nstd/uploadtable/upload_online_move.html',{'tmp_file':tmp_file})
	elif flag == 'add_out':
		return render(request, 'nstd/uploadtable/upload_add_out.html',{'tmp_file':tmp_file})
	elif flag == 'add_instorage':
		return render(request, 'nstd/uploadtable/upload_add_instorage.html',{'tmp_file':tmp_file})
	elif flag == 'calculate_add':
		return render(request, 'nstd/uploadtable/upload_calculate_add.html',{'tmp_file':tmp_file})
	elif flag == 'upload_convert':
		return render(request, 'nstd/uploadtable/upload_convert.html',{'tmp_file':tmp_file})
	elif flag == 'upload_modify_1':
		return render(request, 'nstd/uploadtable/upload_modify_1.html',{'tmp_file':tmp_file})
	elif flag == 'upload_modify_2':
		return render(request, 'nstd/uploadtable/upload_modify_2.html',{'tmp_file':tmp_file})
	elif flag == 'upload_modify_3':
		return render(request, 'nstd/uploadtable/upload_modify_3.html',{'tmp_file':tmp_file})
	elif flag == 'upload_modify_4':
		return render(request, 'nstd/uploadtable/upload_modify_4.html',{'tmp_file':tmp_file})

#获取添加资产的CSV文件数据
def get_add_csv_data(request):
	tmp_file = request.GET.get('tmp_file')
	#读取上传的Excel文件中的数据
	data = {"code":0,"msg":"","count":0,'data':[]}
	if tmp_file:
		workbook = xlrd.open_workbook(tmp_file)
		allsheets = workbook.sheets()
		if allsheets:
			uploadsheet = allsheets[0]
			row_number = uploadsheet.nrows
			for i in range(row_number):
				if i > 1:
					row_dict = {}
					row_dict['index'] = i - 1
					row_dict['a_cd'] = str(uploadsheet.cell(i,0).value).split('.')[0]
					row_dict['a_self_cd'] = str(uploadsheet.cell(i,1).value).split('.')[0]
					row_dict['a_name'] = str(uploadsheet.cell(i,2).value)
					row_dict['a_type_cd'] = str(uploadsheet.cell(i,3).value)
					row_dict['a_fuselage_cd'] = str(uploadsheet.cell(i,4).value).split('.')[0]
					row_dict['a_amount'] = str(uploadsheet.cell(i,5).value)
					row_dict['a_price'] = str(uploadsheet.cell(i,6).value)
					row_dict['a_currency'] = str(uploadsheet.cell(i,7).value)
					row_dict['a_out_time'] = get_excel_datetime(uploadsheet,i,8)
					row_dict['a_purchase_time'] = get_excel_datetime(uploadsheet,i,9)
					row_dict['a_project_cd'] = str(uploadsheet.cell(i,10).value).split('.')[0]
					row_dict['a_depart'] = str(uploadsheet.cell(i,11).value)
					row_dict['a_brand'] = str(uploadsheet.cell(i,12).value)
					row_dict['a_supplier'] = str(uploadsheet.cell(i,13).value)
					row_dict['a_loc_cd'] = str(uploadsheet.cell(i,14).value)
					row_dict['a_status'] = str(uploadsheet.cell(i,15).value)
					row_dict['a_category'] = str(uploadsheet.cell(i,16).value)
					row_dict['a_model'] = str(uploadsheet.cell(i,17).value)
					row_dict['a_funds_type'] = str(uploadsheet.cell(i,18).value)
					row_dict['a_budget'] = str(uploadsheet.cell(i,19).value)
					row_dict['a_referendum'] = str(uploadsheet.cell(i,20).value)
					row_dict['a_po_cd'] = str(uploadsheet.cell(i,21).value)
					row_dict['a_sap_cd'] = str(uploadsheet.cell(i,22).value)
					row_dict['a_b_nstd'] = str(uploadsheet.cell(i,23).value)
					row_dict['a_need_cal'] = str(uploadsheet.cell(i,24).value)
					row_dict['a_remark'] = str(uploadsheet.cell(i,25).value)
					data['data'].append(row_dict)
		if os.path.exists(tmp_file):
			os.remove(tmp_file)
	return HttpResponse(json.dumps(data))

def get_add_out_csv_data(request):
	tmp_file = request.GET.get('tmp_file')
	#读取上传的Excel文件中的数据
	data = {"code":0,"msg":"","count":0,'data':[]}
	if tmp_file:
		workbook = xlrd.open_workbook(tmp_file)
		allsheets = workbook.sheets()
		if allsheets:
			uploadsheet = allsheets[0]
			row_number = uploadsheet.nrows
			for i in range(row_number):
				if i > 0:
					row_dict = {}
					row_dict['index'] = i
					row_dict['a_cd'] = str(uploadsheet.cell(i,0).value).split('.')[0]
					row_dict['a_self_cd'] = str(uploadsheet.cell(i,1).value).split('.')[0]
					row_dict['a_name'] = str(uploadsheet.cell(i,2).value)
					row_dict['a_type_cd'] = str(uploadsheet.cell(i,3).value)
					row_dict['a_fuselage_cd'] = str(uploadsheet.cell(i,4).value)
					row_dict['a_amount'] = str(uploadsheet.cell(i,5).value)
					row_dict['a_price'] = str(uploadsheet.cell(i,6).value)
					row_dict['a_currency'] = str(uploadsheet.cell(i,7).value)
					row_dict['a_out_time'] = get_excel_datetime(uploadsheet,i,8)
					row_dict['a_purchase_time'] = get_excel_datetime(uploadsheet,i,9)
					row_dict['a_brand'] = str(uploadsheet.cell(i,10).value)
					row_dict['a_supplier'] = str(uploadsheet.cell(i,11).value)
					row_dict['a_po_cd'] = str(uploadsheet.cell(i,12).value)
					row_dict['a_status'] = str(uploadsheet.cell(i,13).value)
					row_dict['a_category'] = str(uploadsheet.cell(i,14).value)
					row_dict['a_model'] = str(uploadsheet.cell(i,15).value)
					row_dict['a_project_cd'] = str(uploadsheet.cell(i,16).value)
					row_dict['a_funds_type'] = str(uploadsheet.cell(i,17).value)
					row_dict['a_b_nstd'] = str(uploadsheet.cell(i,18).value)		#资产分类(b社、nstd)

					row_dict['a_action_depart'] = str(uploadsheet.cell(i,19).value) #领用部门
					row_dict['a_action_user'] = str(uploadsheet.cell(i,20).value)	#领用人员
					row_dict['a_action_charge'] = str(uploadsheet.cell(i,21).value)	#主管确认
					row_dict['a_action_model'] = str(uploadsheet.cell(i,22).value)	#使用机种
					row_dict['a_action_loc'] = str(uploadsheet.cell(i,23).value)	#使用位置
					row_dict['a_action_remark'] = str(uploadsheet.cell(i,24).value)	#出库备注
					row_dict['a_record_time'] = str(uploadsheet.cell(i,25).value)
					row_dict['a_opr_user'] = str(uploadsheet.cell(i,26).value)

					row_dict['c_adjust'] = str(uploadsheet.cell(i,27).value)		#校正
					row_dict['c_method'] = str(uploadsheet.cell(i,28).value)		#计量方式
					row_dict['c_date'] = str(uploadsheet.cell(i,29).value)			#计量日期
					row_dict['c_end_date'] = str(uploadsheet.cell(i,30).value)		#到期日期
					data['data'].append(row_dict)
		if os.path.exists(tmp_file):
			os.remove(tmp_file)
	return HttpResponse(json.dumps(data))

#读取在库CSV文件数据信息
def get_add_instorage_csv_data(request):
	tmp_file = request.GET.get('tmp_file')
	#读取上传的Excel文件中的数据
	data = {"code":0,"msg":"","count":0,'data':[]}
	if tmp_file:
		workbook = xlrd.open_workbook(tmp_file)
		allsheets = workbook.sheets()
		if allsheets:
			uploadsheet = allsheets[1]
			row_number = uploadsheet.nrows
			for i in range(row_number):
				if i > 0:
					row_dict = {}
					row_dict['a_cd'] = str(uploadsheet.cell(i,0).value).split('.')[0]
					row_dict['a_self_cd'] = str(uploadsheet.cell(i,1).value).split('.')[0]
					row_dict['a_name'] = str(uploadsheet.cell(i,2).value)
					row_dict['a_type_cd'] = str(uploadsheet.cell(i,3).value)
					row_dict['a_fuselage_cd'] = str(uploadsheet.cell(i,4).value)
					row_dict['a_amount'] = str(uploadsheet.cell(i,5).value)
					row_dict['a_price'] = str(uploadsheet.cell(i,6).value)
					row_dict['a_currency'] = str(uploadsheet.cell(i,7).value)
					row_dict['a_out_time'] = get_excel_datetime(uploadsheet,i,8)
					row_dict['a_purchase_time'] = get_excel_datetime(uploadsheet,i,9)
					row_dict['a_depart'] = str(uploadsheet.cell(i,10).value)
					row_dict['a_loc_cd'] = str(uploadsheet.cell(i,13).value)
					row_dict['a_brand'] = str(uploadsheet.cell(i,15).value)
					row_dict['a_supplier'] = str(uploadsheet.cell(i,16).value)
					row_dict['a_po_cd'] = str(uploadsheet.cell(i,17).value)
					row_dict['a_status'] = str(uploadsheet.cell(i,18).value)
					row_dict['a_category'] = str(uploadsheet.cell(i,19).value)
					row_dict['a_model'] = str(uploadsheet.cell(i,21).value)
					row_dict['a_project_cd'] = str(uploadsheet.cell(i,22).value)
					row_dict['a_funds_type'] = str(uploadsheet.cell(i,23).value)
					row_dict['a_b_nstd'] = str(uploadsheet.cell(i,24).value)		#资产分类(b社、nstd)
					data['data'].append(row_dict)
		if os.path.exists(tmp_file):
			os.remove(tmp_file)
	return HttpResponse(json.dumps(data))

def upload_add_instorage(request):
	table_data = request.POST.get('table_data')
	if table_data:
		table_data = json.loads(table_data)
	a_record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	data = asset_basefunc_models.upload_add_instorage(table_data,a_record_time)
	return HttpResponse(json.dumps(data))

#在线设备导入
def upload_add_out(request):
	table_data = request.POST.get('table_data')
	if table_data:
		table_data = json.loads(table_data)
	a_record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	a_opr_user = request.session.get('u_nstd_name',None)
	a_action_type = 5
	if not a_opr_user:
		return HttpResponse(json.dumps({'result':False,'msg':'您未登录或登录信息失效，请先登录'}))
	else:
		data = asset_basefunc_models.upload_add_out(a_record_time,a_action_type,a_opr_user,table_data)
		print(data)
		return HttpResponse(json.dumps(data))

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

#批量上传资产添加数据
def upload_add(request):
	table_data = request.POST.get('table_data')
	a_record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	a_opr_user = request.session.get('u_nstd_name',None)
	if table_data:
		table_data = json.loads(table_data)
	data = asset_basefunc_models.upload_add(table_data,a_opr_user,a_record_time)
	return HttpResponse(json.dumps(data))

#获取资产出库的CSV文件数据.
def get_out_csv_data(request):
	tmp_file = request.GET.get('tmp_file')
	#读取上传的Excel文件中的数据
	tmp_list = []
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
					row_dict['index'] = i - 1
					a_cd = str(sheet.cell(i,0).value).split('.')[0]			    #资产番号

					if a_cd in tmp_list:	#资产重复出库提醒
						data['code'] = 1
						data['msg'] = '资产号{0}重复,请检查Excel数据!'.format(a_cd)
						break

					row_dict['a_cd'] = a_cd
					row_dict['a_action_depart'] = str(sheet.cell(i,1).value)	#领用部门
					row_dict['a_action_user'] = str(sheet.cell(i,2).value)		#领用人员
					row_dict['a_action_loc'] = str(sheet.cell(i,3).value)		#使用位置
					row_dict['a_action_model'] = str(sheet.cell(i,4).value)		#使用机种
					row_dict['a_action_charge'] = str(sheet.cell(i,5).value)	#主管确认
					row_dict['a_action_remark'] = str(sheet.cell(i,6).value)	#备注信息
					if a_cd:
						detail = asset_basefunc_models.is_instorage_by_a_cd(a_cd)
						row_dict['a_action_type'] = detail[0]
						row_dict['a_material_id'] = detail[1]
						row_dict['a_action_state'] = detail[2]
						row_dict['a_origin_loc'] = detail[3]
						row_dict['a_action_category'] = detail[13]
						row_dict['a_name'] = detail[6]
						row_dict['a_type_cd'] = detail[7]
					data['data'].append(row_dict)
					tmp_list.append(a_cd)
		if os.path.exists(tmp_file):
			os.remove(tmp_file)
	return HttpResponse(json.dumps(data))

#获取资产退库的CSV文件中的数据
def get_back_csv_data(request):
	tmp_file = request.GET.get('tmp_file')
	#读取上传的Excel文件中的数据
	data = {"code":0,"msg":"","count":0,'data':[]}
	tmp_list = []
	if tmp_file:
		workbook = xlrd.open_workbook(tmp_file)
		allsheets = workbook.sheets()
		if allsheets:
			uploadsheet = allsheets[0]
			row_number = uploadsheet.nrows
			for i in range(row_number):
				if i > 1:
					row_dict = {}
					a_cd = str(uploadsheet.cell(i,0).value).split('.')[0]

					if a_cd in tmp_list:	#资产号出现重复提醒
						data['code'] = 1
						data['msg'] = '资产号{0}出现重复，请检查Excel数据'.format(a_cd)
						break

					row_dict['a_cd'] = a_cd                                          #资产番号
					row_dict['a_action_user'] = str(uploadsheet.cell(i,1).value)	 #退库人员
					row_dict['a_action_loc'] = str(uploadsheet.cell(i,2).value)		 #退库位置
					row_dict['a_action_charge'] = str(uploadsheet.cell(i,3).value)	 #主管确认
					row_dict['a_action_state'] = str(uploadsheet.cell(i,4).value)	 #资产状态
					row_dict['a_action_category'] = str(uploadsheet.cell(i,5).value) #折旧类别 
					row_dict['a_action_remark'] = str(uploadsheet.cell(i,6).value)	 #备注信息
					if a_cd:
						detail = asset_basefunc_models.is_instorage_by_a_cd(a_cd)
						row_dict['a_action_type'] = detail[0]
						row_dict['a_material_id'] = detail[1]
						row_dict['a_origin_loc'] = detail[3]
						row_dict['a_name'] = detail[6]
						row_dict['a_type_cd'] = detail[7]
					data['data'].append(row_dict)
					tmp_list.append(a_cd)
		if os.path.exists(tmp_file):
			os.remove(tmp_file)
	return HttpResponse(json.dumps(data))

#获取资产转换的CSV文件中的数据
def get_convert_csv_data(request):
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
					a_origin_cd = str(sheet.cell(i,0).value).split('.')[0]
					row_dict['a_origin_cd'] = a_origin_cd        				 #资产番号
					row_dict['a_cd'] = str(sheet.cell(i,1).value).split('.')[0]	 #新资产番号
					if a_origin_cd:
						detail = asset_basefunc_models.is_instorage_by_a_cd(a_origin_cd)
						row_dict['a_action_type'] = detail[0]
						row_dict['a_material_id'] = detail[1]
						row_dict['a_name'] = detail[6]
						row_dict['a_type_cd'] = detail[7]
					data['data'].append(row_dict)
		if os.path.exists(tmp_file):
			os.remove(tmp_file)
	return HttpResponse(json.dumps(data))

#资产批量出库
def upload_out(request): 
	a_action_type = 5
	a_record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	table_data = request.POST.get('table_data')
	if table_data:
		table_data = json.loads(table_data)
	a_opr_user = request.session.get('u_nstd_name',None)
	if not a_opr_user:
		return HttpResponse(json.dumps({'result':False,'msg':'您未登录或登录信息失效，请先登录'}))
	else:
		num = asset_basefunc_models.upload_out(a_action_type,a_record_time,a_opr_user,table_data)
		return HttpResponse(json.dumps({'result':True,'num':num}))

#资产批量归还
def upload_back(request):
	a_action_type = 4
	a_record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	table_data = request.POST.get('table_data')
	if table_data:
		table_data = json.loads(table_data)
	a_opr_user = request.session.get('u_nstd_name',None)
	if not a_opr_user:
		return HttpResponse(json.dumps({'result':False,'msg':'您未登录或登录信息失效，请先登录'}))
	else:
		num = asset_basefunc_models.upload_back(a_action_type,a_record_time,a_opr_user,table_data)
		return HttpResponse(json.dumps({'result':True,'num':num}))

#上传支给设备数据
def upload_zj(request):
	a_action_type = 1
	a_record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	table_data = request.POST.get('table_data')
	if table_data:
		table_data = json.loads(table_data)
	a_opr_user = request.session.get('u_nstd_name',None)
	if not a_opr_user:
		return HttpResponse(json.dumps({'result':False,'msg':'您未登录或登录信息失效，请先登录'}))
	else:
		num = asset_basefunc_models.upload_zj(a_action_type,a_record_time,a_opr_user,table_data)
		return HttpResponse(json.dumps({'result':True,'num':num}))

#上传支给归还设备数据
def upload_zj_revert(request):
	a_action_type = 2
	a_record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	table_data = request.POST.get('table_data')
	if table_data:
		table_data = json.loads(table_data)
	a_opr_user = request.session.get('u_nstd_name',None)
	if not a_opr_user:
		return HttpResponse(json.dumps({'result':False,'msg':'您未登录或登录信息失效，请先登录'}))
	else:
		num = asset_basefunc_models.upload_zj_revert(a_action_type,a_record_time,a_opr_user,table_data)
	return HttpResponse(json.dumps({'result':True,'num':num}))

#上传借用归还设备数据
def upload_loan_revert(request):
	a_action_type = 3
	a_record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	table_data = request.POST.get('table_data')
	if table_data:
		table_data = json.loads(table_data)
	a_opr_user = request.session.get('u_nstd_name',None)
	if not a_opr_user:
		return HttpResponse(json.dumps({'result':False,'msg':'您未登录或登录信息失效，请先登录'}))
	else:
		num = asset_basefunc_models.upload_loan_revert(a_action_type,a_record_time,a_opr_user,table_data)
	return HttpResponse(json.dumps({'result':True,'num':num}))

#上传销售设备数据
def upload_sale(request):
	a_action_type = 6
	a_record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	a_opr_user = request.session.get('u_nstd_name',None)
	table_data = request.POST.get('table_data')
	if table_data:
		table_data = json.loads(table_data)
	if not a_opr_user:
		return HttpResponse(json.dumps({'result':False,'msg':'您未登录或登录信息失效，请先登录'}))
	else:
		num = asset_basefunc_models.upload_sale(a_action_type,a_record_time,a_opr_user,table_data)
	return HttpResponse(json.dumps({'result':True,'num':num}))

#上传报废设备数据
def upload_scrap(request):
	a_action_type = 7
	a_record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	a_opr_user = request.session.get('u_nstd_name',None)
	table_data = request.POST.get('table_data')
	if table_data:
		table_data = json.loads(table_data)
	if not a_opr_user:
		return HttpResponse(json.dumps({'result':False,'msg':'您未登录或登录信息失效，请先登录'}))
	else:
		num = asset_basefunc_models.upload_scrap(a_action_type,a_record_time,a_opr_user,table_data)
	return HttpResponse(json.dumps({'result':True,'num':num}))

#库房设备批量移动
def upload_instorage_move(request):
	a_action_type = 9
	a_record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	a_opr_user = request.session.get('u_nstd_name',None)
	table_data = request.POST.get('table_data')
	if table_data:
		table_data = json.loads(table_data)
	if not a_opr_user:
		return HttpResponse(json.dumps({'result':False,'msg':'您未登录或登录信息失效，请先登录'}))
	else:
		num = asset_basefunc_models.upload_instorage_move(a_action_type,a_record_time,a_opr_user,table_data)
	return HttpResponse(json.dumps({'result':True,'num':num}))

#上传设备移动数据
def upload_online_move(request):
	a_action_type = 8
	a_record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	a_opr_user = request.session.get('u_nstd_name',None)
	table_data = request.POST.get('table_data')
	if table_data:
		table_data = json.loads(table_data)
	if not a_opr_user:
		return HttpResponse(json.dumps({'result':False,'msg':'您未登录或登录信息失效，请先登录'}))
	else:
		num = asset_basefunc_models.upload_online_move(a_action_type,a_record_time,a_opr_user,table_data)
	return HttpResponse(json.dumps({'result':True,'num':num}))

#获取要支给的CSV数据
def get_zj_csv_data(request):
	tmp_file = request.GET.get('tmp_file')
	#读取上传的Excel文件中的数据
	data = {"code":0,"msg":"","count":0,'data':[]}
	if tmp_file:
		workbook = xlrd.open_workbook(tmp_file)
		allsheets = workbook.sheets()
		if allsheets:
			uploadsheet = allsheets[0]
			row_number = uploadsheet.nrows
			for i in range(row_number):
				if i > 1:
					row_dict = {}
					row_dict['index'] = i - 1
					a_cd = str(uploadsheet.cell(i,0).value).split('.')[0]			 #资产番号
					row_dict['a_cd'] = a_cd
					row_dict['a_action_depart'] = str(uploadsheet.cell(i,1).value)   #当前部门
					row_dict['a_action_state'] = str(uploadsheet.cell(i,2).value)	 #资产状态
					row_dict['a_action_charge'] = str(uploadsheet.cell(i,3).value)	 #供应商确认
					row_dict['a_action_remark'] = str(uploadsheet.cell(i,4).value)	 #备注信息
					if a_cd:
						detail = asset_basefunc_models.is_instorage_by_a_cd(a_cd)
						row_dict['a_action_type'] = detail[0]
						row_dict['a_material_id'] = detail[1]
						row_dict['a_action_loc'] = detail[3]
						row_dict['a_name'] = detail[6]
						row_dict['a_type_cd'] = detail[7]
						row_dict['a_action_category'] = detail[13]
					data['data'].append(row_dict)
		if os.path.exists(tmp_file):
			os.remove(tmp_file)
	return HttpResponse(json.dumps(data))

#获取支给归还CSV文件数据
def get_zj_revert_csv_data(request):
	tmp_file = request.GET.get('tmp_file')
	#读取上传的Excel文件中的数据
	data = {"code":0,"msg":"","count":0,'data':[]}
	if tmp_file:
		workbook = xlrd.open_workbook(tmp_file)
		allsheets = workbook.sheets()
		if allsheets:
			uploadsheet = allsheets[0]
			row_number = uploadsheet.nrows
			for i in range(row_number):
				if i > 1:
					row_dict = {}
					row_dict['index'] = i - 1
					a_cd = str(uploadsheet.cell(i,0).value).split('.')[0]			 #资产番号
					row_dict['a_cd'] = a_cd
					row_dict['a_action_loc'] = str(uploadsheet.cell(i,1).value) 	 #还入位置
					row_dict['a_action_state'] = str(uploadsheet.cell(i,2).value)	 #资产状态
					row_dict['a_action_category'] = str(uploadsheet.cell(i,3).value) #折旧分类
					row_dict['a_action_remark'] = str(uploadsheet.cell(i,4).value)	 #备注信息
					if a_cd:
						detail = asset_basefunc_models.is_instorage_by_a_cd(a_cd)
						row_dict['a_action_type'] = detail[0]
						row_dict['a_material_id'] = detail[1]
						row_dict['a_name'] = detail[6]
						row_dict['a_type_cd'] = detail[7]
						row_dict['a_action_supplier'] = detail[14]
					data['data'].append(row_dict)
		if os.path.exists(tmp_file):
			os.remove(tmp_file)
	return HttpResponse(json.dumps(data))

#获取借用归还CSV文件数据
def get_loan_revert_csv_data(request):
	tmp_file = request.GET.get('tmp_file')
	#读取上传的Excel文件中的数据
	data = {"code":0,"msg":"","count":0,'data':[]}
	if tmp_file:
		workbook = xlrd.open_workbook(tmp_file)
		allsheets = workbook.sheets()
		if allsheets:
			uploadsheet = allsheets[0]
			row_number = uploadsheet.nrows
			for i in range(row_number):
				if i > 1:
					row_dict = {}
					a_cd = str(uploadsheet.cell(i,0).value).split('.')[0]		  #资产番号
					row_dict['a_cd'] = a_cd,
					row_dict['a_action_state'] = str(uploadsheet.cell(i,1).value) #资产状态
					row_dict['a_action_remark'] = str(uploadsheet.cell(i,2).value)#备注信息
					if a_cd:
						detail = asset_basefunc_models.is_instorage_by_a_cd(a_cd)
						row_dict['a_action_type'] = detail[0]
						row_dict['a_material_id'] = detail[1]
						row_dict['a_action_loc'] = detail[3]
						row_dict['a_price'] = detail[4]
						row_dict['a_supplier'] = detail[5]
						row_dict['a_name'] = detail[6]
						row_dict['a_type_cd'] = detail[7]
					data['data'].append(row_dict)
		if os.path.exists(tmp_file):
			os.remove(tmp_file)
	return HttpResponse(json.dumps(data))

#获取批量销售CSV数据
def get_sale_csv_data(request):
	tmp_file = request.GET.get('tmp_file')
	#读取上传的Excel文件中的数据
	data = {"code":0,"msg":"","count":0,'data':[]}
	if tmp_file:
		workbook = xlrd.open_workbook(tmp_file)
		allsheets = workbook.sheets()
		if allsheets:
			uploadsheet = allsheets[0]
			row_number = uploadsheet.nrows
			for i in range(row_number):
				if i > 1:
					row_dict = {}
					row_dict['index'] = i - 1
					#资产番号
					a_cd = str(uploadsheet.cell(i,0).value).split('.')[0]			 #资产番号
					row_dict['a_cd'] = a_cd
					row_dict['a_action_supplier'] = str(uploadsheet.cell(i,1).value) #客户名称
					row_dict['a_action_remark'] = str(uploadsheet.cell(i,2).value)   #备注信息
					if a_cd:
						detail = asset_basefunc_models.is_instorage_by_a_cd(a_cd)
						row_dict['a_action_type'] = detail[0]
						row_dict['a_material_id'] = detail[1]
						row_dict['a_action_state'] = detail[2]
						row_dict['a_action_loc'] = detail[3]
						row_dict['a_name'] = detail[6]
						row_dict['a_type_cd'] = detail[7]
					data['data'].append(row_dict)
		if os.path.exists(tmp_file):
			os.remove(tmp_file)
	return HttpResponse(json.dumps(data))

#获取批量报废CSV数据
def get_scrap_csv_data(request):
	tmp_file = request.GET.get('tmp_file')
	#读取上传的Excel文件中的数据
	data = {"code":0,"msg":"","count":0,'data':[]}
	if tmp_file:
		workbook = xlrd.open_workbook(tmp_file)
		allsheets = workbook.sheets()
		if allsheets:
			uploadsheet = allsheets[0]
			row_number = uploadsheet.nrows
			for i in range(row_number):
				if i > 1:
					row_dict = {}
					row_dict['index'] = i - 1
					#资产番号
					a_cd = str(uploadsheet.cell(i,0).value).split('.')[0]			 #资产番号
					row_dict['a_cd'] = a_cd
					row_dict['a_action_remark'] = str(uploadsheet.cell(i,1).value)   #备注信息
					if a_cd:
						detail = asset_basefunc_models.is_instorage_by_a_cd(a_cd)
						row_dict['a_action_type'] = detail[0]
						row_dict['a_material_id'] = detail[1]
						row_dict['a_name'] = detail[6]
						row_dict['a_type_cd'] = detail[7]
					data['data'].append(row_dict)
		if os.path.exists(tmp_file):
			os.remove(tmp_file)
	return HttpResponse(json.dumps(data))

#读取库房移动的CSV文件数据
def get_instorage_move_data(request):
	tmp_file = request.GET.get('tmp_file')
	data = {"code":0,"msg":"","count":0,'data':[]}
	if tmp_file:
		workbook = xlrd.open_workbook(tmp_file)
		allsheets = workbook.sheets()
		if allsheets:
			uploadsheet = allsheets[0]
			row_number = uploadsheet.nrows
			for i in range(row_number):
				if i > 1:
					row_dict = {}
					a_cd = str(uploadsheet.cell(i,0).value).split('.')[0]			 #资产番号
					row_dict['a_cd'] = a_cd
					row_dict['a_action_loc'] = str(uploadsheet.cell(i,1).value)		 #移动位置
					row_dict['a_action_depart'] = 'IDLE'							 #移动部门
					if a_cd:
						detail = asset_basefunc_models.is_instorage_by_a_cd(a_cd)
						row_dict['a_action_type'] = detail[0]
						row_dict['a_material_id'] = detail[1]
						row_dict['a_action_state'] = detail[2]
						row_dict['a_origin_loc'] = detail[3]
						row_dict['a_name'] = detail[6]
						row_dict['a_type_cd'] = detail[7]
					data['data'].append(row_dict)
		if os.path.exists(tmp_file):
			os.remove(tmp_file)
	return HttpResponse(json.dumps(data))

#读取在线移动的Excel文件中的数据
def get_online_move_data(request):
	tmp_file = request.GET.get('tmp_file')
	data = {"code":0,"msg":"","count":0,'data':[]}
	if tmp_file:
		workbook = xlrd.open_workbook(tmp_file)
		allsheets = workbook.sheets()
		if allsheets:
			uploadsheet = allsheets[0]
			row_number = uploadsheet.nrows
			for i in range(row_number):
				if i > 1:
					row_dict = {}
					a_cd = str(uploadsheet.cell(i,0).value).split('.')[0]			 #资产番号
					row_dict['a_cd'] = a_cd
					row_dict['a_action_depart'] = str(uploadsheet.cell(i,1).value)   #移动部门
					row_dict['a_action_loc'] = str(uploadsheet.cell(i,2).value)		 #移动位置
					row_dict['a_action_user'] = str(uploadsheet.cell(i,3).value)	 #领用人员
					row_dict['a_action_charge'] = str(uploadsheet.cell(i,4).value)	 #主管确认
					row_dict['a_action_model'] = str(uploadsheet.cell(i,5).value)	 #领用人员
					row_dict['a_action_remark'] = str(uploadsheet.cell(i,6).value)	 #领用人员
					if a_cd:
						detail = asset_basefunc_models.is_instorage_by_a_cd(a_cd)
						row_dict['a_action_type'] = detail[0]
						row_dict['a_material_id'] = detail[1]
						row_dict['a_action_state'] = detail[2]
						row_dict['a_origin_loc'] = detail[3]
						row_dict['a_name'] = detail[6]
						row_dict['a_type_cd'] = detail[7]
						row_dict['a_origin_depart'] = detail[8]
						row_dict['a_action_category'] = detail[13]
					data['data'].append(row_dict)
		if os.path.exists(tmp_file):
			os.remove(tmp_file)
	return HttpResponse(json.dumps(data))

#资产库房内部移动
def asset_instorage_move(request):
	a_opr_user = request.session.get('u_nstd_name',None)
	a_action_type = request.POST.get('a_action_type')
	asset_list = request.POST.get('asset_list')
	if asset_list:
		asset_list = json.loads(asset_list)
	a_record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	num = asset_basefunc_models.asset_instorage_move(a_opr_user,a_action_type,a_record_time,asset_list)
	return HttpResponse(json.dumps({'num':num}))