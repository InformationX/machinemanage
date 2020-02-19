# -*- coding:utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from app_apple.models import asset_basefunc_models
from app_apple.models import asset_detail_models
import json,datetime

#资产添加
def asset_add(request):
	a_cd = request.POST.get('a_cd')
	a_main_cd = request.POST.get('a_main_cd')
	a_type_cd = request.POST.get('a_type_cd')
	a_main_serial = request.POST.get('a_main_serial')
	a_dept_cd = request.POST.get('a_dept_cd')
	a_loc_cd = request.POST.get('a_loc_cd')
	a_state = request.POST.get('a_state')
	a_remark = request.POST.get('a_remark')

	a_opr_user = request.session.get('u_id')
	a_add_time  = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

	result = asset_basefunc_models.asset_add(a_cd,a_main_cd,a_type_cd,a_main_serial,
				a_dept_cd,a_loc_cd,a_state,a_remark,a_opr_user,a_add_time)

	return HttpResponse(json.dumps({'result':result}))

#资产添加信息查询
def asset_add_search():
	pass

#资产批量添加
def upload_add(request):
	a_opr_user = request.session.get('u_b_name')
	if not a_opr_user:
		return HttpResponse(json.dumps({'result':False,'msg':'您未登陆，请先登录!'}))
	a_add_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	table_data = request.POST.get('table_data')
	if table_data:
		table_data = json.loads(table_data)
		print(table_data[0])
	data = asset_basefunc_models.upload_add(a_opr_user,a_add_time,table_data) 
	return HttpResponse(json.dumps(data))

def get_detail(request):
	assetList = request.GET.get('assetList')
	if assetList:
		assetList = json.loads(assetList)
	data = {"code":0,"msg":"","count":0,'data':[]}
	data['data'] = asset_detail_models.get_detail(assetList)
	return HttpResponse(json.dumps(data))

def upload_zj(request):
	a_opr_user = request.session.get('u_b_name')
	a_add_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	zj_list = request.POST.get('zj_list')
	if zj_list:
		zj_list = json.loads(zj_list)
	data = asset_basefunc_models.upload_zj(zj_list,a_opr_user,a_add_time)
	return HttpResponse(json.dumps(data))

def upload_excel_zj(request):
	a_opr_user = request.session.get('u_b_name')
	a_add_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	zj_list = request.POST.get('table_data')
	if zj_list:
		zj_list = json.loads(zj_list)
	data = asset_basefunc_models.upload_excel_zj(zj_list,a_opr_user,a_add_time)
	return HttpResponse(json.dumps(data))

def upload_excel_zj_revert(request):
	a_opr_user = request.session.get('u_b_name')
	a_add_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	zj_revert_list = request.POST.get('table_data')
	if zj_revert_list:
		zj_revert_list = json.loads(zj_revert_list)
	data = asset_basefunc_models.upload_excel_zj_revert(zj_revert_list,a_opr_user,a_add_time)
	return HttpResponse(json.dumps(data))

def upload_excel_out(request):
	a_opr_user = request.session.get('u_b_name')
	a_add_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	out_list = request.POST.get('table_data')
	if out_list:
		out_list = json.loads(out_list)
	data = asset_basefunc_models.upload_excel_out(out_list,a_opr_user,a_add_time)
	return HttpResponse(json.dumps(data))

'''
def get_out_data(request):
	assetList = request.GET.get('assetList')
	if assetList:
		assetList = json.loads(assetList)
	data = {"code":0,"msg":"","count":0,'data':[]}
	data['data'] = asset_basefunc_models.get_out_data(assetList)
	return HttpResponse(json.dumps(data))
'''

#资产出库
def upload_out(request):
	assetList = request.POST.get('assetList')
	if assetList:
		assetList = json.loads(assetList)
	a_opr_user = request.session.get('u_b_name')
	a_add_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	num = asset_basefunc_models.upload_out(assetList,a_opr_user,a_add_time)
	return HttpResponse(json.dumps({'result':True,'num':num}))

#获取出库资产详情
def asset_out_detail(request):
	a_cd = request.GET.get('a_cd')
	data = asset_basefunc_models.asset_out_detail(a_cd)
	return HttpResponse(json.dumps(data))

#资产单个退库
def asset_out_single(request):
	a_cd = request.POST.get('a_cd')
	a_action_shelf = request.POST.get('a_action_shelf')
	a_action_state = request.POST.get('a_action_state')
	a_back_user = request.POST.get('a_back_user')
	a_confirm_user = request.POST.get('a_confirm_user')
	a_main_cd = request.POST.get('a_main_cd')
	a_main_serial = request.POST.get('a_main_serial')
	a_opr_user = request.session.get('u_b_name')
	a_add_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	result = asset_basefunc_models.asset_out_single(a_cd,a_action_shelf,a_action_state,a_back_user,a_confirm_user,a_main_cd,a_main_serial,a_opr_user,a_add_time)
	return HttpResponse(json.dumps({'result':result}))

#只给归还
def zj_revert_detail(request):
	assetList = request.GET.get('assetList')
	if assetList:
		assetList = json.loads(assetList)
	data = {"code":0,"msg":"","count":0,'data':[]}
	data['data'] = asset_basefunc_models.zj_revert_detail(assetList)
	return HttpResponse(json.dumps(data))

def zj_back(request):
	assetList = request.POST.get('assetList')
	if assetList:
		assetList = json.loads(assetList)
	a_opr_user = request.session.get('u_b_name')
	a_add_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	num = asset_basefunc_models.zj_back(assetList,a_opr_user,a_add_time)
	return HttpResponse(json.dumps({'num':num}))

def upload_out_back(request):
	assetList = request.POST.get('assetList')
	if assetList:
		assetList = json.loads(assetList)
	a_opr_user = request.session.get('u_b_name')
	a_add_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	num = asset_basefunc_models.upload_out_back(assetList,a_opr_user,a_add_time)
	return HttpResponse(json.dumps({'num':num}))

def upload_excel_out_back(request):
	assetList = request.POST.get('table_data')
	if assetList:
		assetList = json.loads(assetList)
	a_opr_user = request.session.get('u_b_name')
	a_add_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	data = asset_basefunc_models.upload_excel_out_back(assetList,a_opr_user,a_add_time)
	return HttpResponse(json.dumps(data))

def upload_edit_loc(request):
	editList = request.POST.get('table_data')
	if editList:
		editList = json.loads(editList)
	data = asset_basefunc_models.upload_edit_loc(editList)
	return HttpResponse(json.dumps(data))
	