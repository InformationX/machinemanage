# -*- coding:utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from app_apple.models import asset_baseinfo_models
import json,datetime

#查询基础信息
def get_base_detail(request):
	a_cd = request.GET.get('a_cd')
	data = asset_baseinfo_models.get_base_detail(a_cd)
	return HttpResponse(json.dumps(data))

#编辑基础信息
def edit_base(request):
	a_cd = request.POST.get('a_cd')
	a_type_cd = request.POST.get('a_type_cd')
	a_fuselage_cd = request.POST.get('a_fuselage_cd')
	a_main_cd = request.POST.get('a_main_cd')
	a_main_serial = request.POST.get('a_main_serial')
	a_action_loc = request.POST.get('a_action_loc')
	a_action_state = request.POST.get('a_action_state')
	a_dept_cd = request.POST.get('a_dept_cd')
	a_action_remark = request.POST.get('a_action_remark')
	result = asset_baseinfo_models.edit_base(a_cd,a_type_cd,a_fuselage_cd,a_main_cd,a_main_serial,a_action_loc,a_action_state,a_dept_cd,a_action_remark)
	return HttpResponse(json.dumps({'result':result}))

#查询出库详情
def get_out_detail(request):
	a_cd = request.GET.get('a_cd')
	data = asset_baseinfo_models.get_out_detail(a_cd) 
	return HttpResponse(json.dumps(data))

#编辑出库信息
def edit_out(request):
	a_main_cd = request.POST.get('a_main_cd')
	a_main_serial = request.POST.get('a_main_serial')
	a_take_line = request.POST.get('a_take_line')
	a_take_user = request.POST.get('a_take_user')
	a_action_loc = request.POST.get('a_action_loc')
	a_action_state = request.POST.get('a_action_state')
	a_confirm_user = request.POST.get('a_confirm_user')
	a_action_remark = request.POST.get('a_action_remark')
	id = request.POST.get('id')
	result = asset_baseinfo_models.edit_out(a_main_cd,a_main_serial,a_take_line,a_take_user,a_action_loc,a_action_state,a_confirm_user,a_action_remark,id)
	return HttpResponse(json.dumps({'result':result}))

#查询退库详情
def get_out_back(request):
	a_cd = request.GET.get('a_cd')
	data = asset_baseinfo_models.get_out_back(a_cd)
	return HttpResponse(json.dumps(data))

#编辑退库信息
def edit_out_back(request):
	a_main_cd = request.POST.get('a_main_cd')
	a_main_serial = request.POST.get('a_main_serial')
	a_back_user = request.POST.get('a_back_user')
	a_action_loc = request.POST.get('a_action_loc')
	a_action_state = request.POST.get('a_action_state')
	a_confirm_user = request.POST.get('a_confirm_user')
	a_action_remark = request.POST.get('a_action_remark')
	id = request.POST.get('id')
	result = asset_baseinfo_models.edit_out_back(a_main_cd,a_main_serial,a_back_user,a_action_loc,a_action_state,a_confirm_user,a_action_remark,id)
	return HttpResponse(json.dumps({'result':result}))

#查询支给详情
def get_zj_detail(request):
	a_cd = request.GET.get('a_cd')
	data = asset_baseinfo_models.get_zj_detail(a_cd)
	return HttpResponse(json.dumps(data))

#查询支给详情
def edit_zj(request):
	a_main_cd = request.POST.get('a_main_cd')
	a_main_serial = request.POST.get('a_main_serial')
	a_zj_object = request.POST.get('a_zj_object')
	a_action_state = request.POST.get('a_action_state')
	a_action_remark = request.POST.get('a_action_remark')
	id = request.POST.get('id')
	result = asset_baseinfo_models.edit_zj(a_main_cd,a_main_serial,a_zj_object,a_action_state,a_action_remark,id)
	return HttpResponse(json.dumps({'result':result}))

#查询支给归还
def get_zj_back(request):
	a_cd = request.GET.get('a_cd')
	data = asset_baseinfo_models.get_zj_back(a_cd)
	return HttpResponse(json.dumps(data))

#编辑支给归还
def edit_zj_back(request):
	a_main_cd = request.POST.get('a_main_cd')
	a_main_serial = request.POST.get('a_main_serial')
	a_action_loc = request.POST.get('a_action_loc')
	a_action_state = request.POST.get('a_action_state')
	a_action_remark = request.POST.get('a_action_remark')
	id = request.POST.get('id')
	result = asset_baseinfo_models.edit_zj_back(a_main_cd,a_main_serial,a_action_loc,a_action_state,a_action_remark,id)
	return HttpResponse(json.dumps({'result':result}))

#根据主题资产号查询主题序列号
def get_serial_by_cd(request):
	pass