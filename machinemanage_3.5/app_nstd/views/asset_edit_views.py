# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from app_nstd.models import asset_edit_models
import json,datetime

def get_edit_base(request):
	a_cd = request.GET.get('a_cd')
	data = asset_edit_models.get_edit_base(a_cd)
	return HttpResponse(json.dumps(data))

def edit_base(request):
	a_cd = request.POST.get('a_cd')
	a_status = request.POST.get('a_status')
	a_category = request.POST.get('a_category')
	a_self_cd = request.POST.get('a_self_cd')
	a_type_cd = request.POST.get('a_type_cd')
	a_name = request.POST.get('a_name')
	a_fuselage_cd = request.POST.get('a_fuselage_cd')
	a_funds_type = request.POST.get('a_funds_type')
	a_supplier = request.POST.get('a_supplier')
	a_project_cd = request.POST.get('a_project_cd')
	a_price = request.POST.get('a_price')
	a_currency = request.POST.get('a_currency')
	a_loc_cd = request.POST.get('a_loc_cd')
	a_model = request.POST.get('a_model')
	a_referendum = request.POST.get('a_referendum')
	a_brand = request.POST.get('a_brand')
	a_amount = request.POST.get('a_amount')
	a_remark = request.POST.get('a_remark')
	result = asset_edit_models.edit_base(a_cd,a_status,a_category,a_self_cd,a_type_cd,a_name,a_fuselage_cd,a_funds_type,a_supplier,a_project_cd,a_price,a_currency,a_loc_cd,a_model,a_referendum,a_brand,a_amount,a_remark)
	return HttpResponse(json.dumps({'result':result}))

def get_edit_out(request):
	a_cd = request.GET.get('a_cd')
	data = asset_edit_models.get_edit_out(a_cd)
	return HttpResponse(json.dumps(data))

def edit_out(request):
	a_action_id = request.POST.get('a_action_id')
	a_action_depart = request.POST.get('a_action_depart')
	a_action_user = request.POST.get('a_action_user')
	a_action_loc = request.POST.get('a_action_loc')
	a_action_state = request.POST.get('a_action_state')
	a_action_category = request.POST.get('a_action_category')
	a_action_charge = request.POST.get('a_action_charge')
	a_action_model = request.POST.get('a_action_model')
	a_action_remark = request.POST.get('a_action_remark')
	result = asset_edit_models.edit_out(a_action_id,a_action_depart,a_action_user,a_action_loc,a_action_state,a_action_category,a_action_charge,a_action_model,a_action_remark)
	return HttpResponse(json.dumps({'result':result}))

def get_edit_back(request):
	a_cd = request.GET.get('a_cd')
	data = asset_edit_models.get_edit_back(a_cd)
	return HttpResponse(json.dumps(data))

def edit_back(request):
	a_action_id = request.POST.get('a_action_id')
	a_action_user = request.POST.get('a_action_user')
	a_action_loc = request.POST.get('a_action_loc')
	a_action_state = request.POST.get('a_action_state')
	a_action_charge = request.POST.get('a_action_charge')
	a_action_category = request.POST.get('a_action_category')
	a_action_remark = request.POST.get('a_action_remark')

	result = asset_edit_models.edit_back(a_action_id,a_action_user,a_action_loc,a_action_state,a_action_charge,a_action_category,a_action_remark)
	return HttpResponse(json.dumps({'result':result}))

def get_edit_zj(request):
	a_cd = request.GET.get('a_cd')
	data = asset_edit_models.get_edit_zj(a_cd)
	return HttpResponse(json.dumps(data))

def edit_zj(request):
	a_action_id = request.POST.get('a_action_id')
	a_action_state = request.POST.get('a_action_state')
	a_action_charge = request.POST.get('a_action_charge')
	a_action_supplier = request.POST.get('a_action_supplier')

	result = asset_edit_models.edit_zj(a_action_id,a_action_state,a_action_charge,a_action_supplier)
	return HttpResponse(json.dumps({'result':result}))

def get_edit_zj_back(request):
	a_cd = request.GET.get('a_cd')
	data = asset_edit_models.get_edit_zj_back(a_cd)
	return HttpResponse(json.dumps(data))

def edit_zj_back(request):
	a_action_id = request.POST.get('a_action_id')
	a_action_loc = request.POST.get('a_action_loc')
	a_action_state = request.POST.get('a_action_state')
	a_action_category = request.POST.get('a_action_category')
	a_action_remark = request.POST.get('a_action_remark')
	result = asset_edit_models.edit_zj_back(a_action_id,a_action_loc,a_action_state,a_action_category,a_action_remark)
	return HttpResponse(json.dumps({'result':result}))

def get_edit_loan_back(request):
	a_cd = request.GET.get('a_cd')
	data = asset_edit_models.get_edit_loan_back(a_cd)
	return HttpResponse(json.dumps(data))

def edit_loan_back(request):
	a_action_id = request.POST.get('a_action_id')
	a_action_state = request.POST.get('a_action_state')
	a_action_remark = request.POST.get('a_action_remark')
	result = asset_edit_models.edit_loan_back(a_action_id,a_action_state,a_action_remark)
	return HttpResponse(json.dumps({'result':result}))

def get_edit_storage_move(request):
	a_cd = request.GET.get('a_cd')
	data = asset_edit_models.get_edit_storage_move(a_cd)
	return HttpResponse(json.dumps(data))

def edit_storage_move(request):
	a_action_id = request.POST.get('a_action_id')
	a_action_loc = request.POST.get('a_action_loc')
	a_action_remark = request.POST.get('a_action_remark')
	result = asset_edit_models.edit_storage_move(a_action_id,a_action_loc,a_action_remark)
	return HttpResponse(json.dumps({'result':result}))
	
def get_edit_online_move(request):
	a_cd = request.GET.get('a_cd')
	data = asset_edit_models.get_edit_online_move(a_cd)
	return HttpResponse(json.dumps(data))

def edit_online_move(request):
	a_action_depart = request.POST.get('a_action_depart')
	a_action_loc = request.POST.get('a_action_loc')
	a_action_user = request.POST.get('a_action_user')
	a_action_charge = request.POST.get('a_action_charge')
	a_action_model = request.POST.get('a_action_model')
	a_action_remark = request.POST.get('a_action_remark')
	a_action_id = request.POST.get('a_action_id')
	result = asset_edit_models.edit_online_move(a_action_id,a_action_depart,a_action_loc,a_action_user,a_action_charge,a_action_model,a_action_remark)
	return HttpResponse(json.dumps({'result':result}))

def get_edit_loc(request):
	a_cd = request.GET.get('a_cd')
	data = asset_edit_models.get_edit_loc(a_cd)
	return HttpResponse(json.dumps(data))

def edit_loc(request):
	a_cd = request.POST.get('a_cd')
	a_material_id = request.POST.get('a_material_id')
	a_action_id = request.POST.get('a_action_id')
	a_origin_loc = request.POST.get('a_origin_loc')
	a_action_loc = request.POST.get('a_action_loc')
	a_opr_user = request.session.get('u_nstd_name')
	a_record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	a_action_type = 11
	result = asset_edit_models.edit_loc(a_cd,a_material_id,a_action_id,a_origin_loc,a_action_loc,a_opr_user,a_record_time,a_action_type)
	return HttpResponse(json.dumps({'result':result}))

def get_edit_state(request):
	a_cd = request.GET.get('a_cd')
	data = asset_edit_models.get_edit_state(a_cd)
	return HttpResponse(json.dumps(data))

def edit_state(request):
	a_cd = request.POST.get('a_cd')
	a_material_id = request.POST.get('a_material_id')
	a_action_id = request.POST.get('a_action_id')
	a_origin_state = request.POST.get('a_origin_state')
	a_action_state = request.POST.get('a_action_state')
	a_opr_user = request.session.get('u_nstd_name')
	a_record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	a_action_type = 12
	result = asset_edit_models.edit_state(a_cd,a_material_id,a_action_id,a_origin_state,a_action_state,a_opr_user,a_record_time,a_action_type)
	return HttpResponse(json.dumps({'result':result}))
	
def get_edit_category(request):
	a_cd = request.GET.get('a_cd')
	data = asset_edit_models.get_edit_category(a_cd)
	return HttpResponse(json.dumps(data))

def edit_category(request):
	a_cd = request.POST.get('a_cd')
	a_material_id = request.POST.get('a_material_id')
	a_action_id = request.POST.get('a_action_id')
	a_origin_category = request.POST.get('a_origin_category')
	a_action_category = request.POST.get('a_action_category')
	a_opr_user = request.session.get('u_nstd_name')
	a_record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	a_action_type = 13
	result = asset_edit_models.edit_category(a_cd,a_material_id,a_action_id,a_origin_category,a_action_category,a_opr_user,a_record_time,a_action_type)
	return HttpResponse(json.dumps({'result':result}))

def get_edit_depart(request):
	a_cd = request.GET.get('a_cd')
	data = asset_edit_models.get_edit_depart(a_cd)
	return HttpResponse(json.dumps(data))

def edit_depart(request):
	a_cd = request.POST.get('a_cd')
	a_material_id = request.POST.get('a_material_id')
	a_action_id = request.POST.get('a_action_id')
	a_origin_depart = request.POST.get('a_origin_depart')
	a_action_depart = request.POST.get('a_action_depart')
	a_opr_user = request.session.get('u_nstd_name')
	a_record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	a_action_type = 14
	result = asset_edit_models.edit_depart(a_cd,a_material_id,a_action_id,a_origin_depart,a_action_depart,a_opr_user,a_record_time,a_action_type)
	return HttpResponse(json.dumps({'result':result}))