# -*- coding:utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from app_apple.models import asset_apple_models
import json,datetime

def index(request):
	if not request.session.get('u_b_id',None):
		return HttpResponseRedirect('/b/login_page')
	return render(request, 'apple/index.html')

def main(request):
	return render(request, 'apple/main.html')

def login_page(request):
	return render(request, 'apple/login.html')

def login(request):
	u_id = request.POST.get('u_id')
	u_passwd = request.POST.get('u_passwd')
	result,u_name = asset_apple_models.login(u_id,u_passwd)
	if result:
		request.session['u_b_id'] = u_id
		request.session['u_b_name'] = u_name
		return HttpResponse(json.dumps({'result':True}))
	else:
		return HttpResponse(json.dumps({'result':False,'msg':'用户名或密码错误！'}))

def basic(request):
	return render(request, 'basic.html')

def logout(request):
	try:
		del request.session['u_id']
		del request.session['u_name']
	except Exception as e:
		print(e)
	return HttpResponseRedirect('/b/login_page')

#基本功能页面
def asset_add_page(request):
	return render(request, 'apple/basefunc/asset_add_page.html')

def asset_zj_page(request):
	return render(request, 'apple/basefunc/asset_zj_page.html')

def zj_revert_page(request):
	return render(request, 'apple/basefunc/zj_revert_page.html')

def asset_out_page(request):
	return render(request, 'apple/basefunc/asset_out_page.html')

def asset_back_page(request):
	return render(request, 'apple/basefunc/asset_back_page.html')

def asset_loan_page(request):
	return render(request, 'apple/basefunc/asset_loan_page.html')

def asset_revert_page(request):
	return render(request, 'apple/basefunc/asset_revert_page.html')

def asset_scrap_page(request):
	return render(request, 'apple/basefunc/asset_scrap_page.html')

#综合查询页面
def total_search(request):
	data = asset_apple_models.get_total_data()
	return render(request, 'apple/general/total_search.html',data)

def in_storage_search(request):
	return render(request, 'apple/general/in_storage_search.html')

def zj_search(request):
	return render(request, 'apple/general/zj_search.html')

def out_storage_search(request):
	return render(request, 'apple/general/out_storage_search.html')

def back_search(request):
	return render(request, 'apple/general/back_search.html')

def zj_back_search(request):
	return render(request, 'apple/general/zj_back_search.html')

def add_search(request):
	return render(request, 'apple/general/add_search.html')

def online_search(request):
	return render(request, 'apple/general/online_search.html')

def revert_search(request):
	return render(request, 'apple/general/revert_search.html')

	'''————————————————————————————————'''
	'''——————————基本信息设置———————————'''
	'''————————————————————————————————'''

#部门管理
def department(request):
	return render(request, 'apple/baseinfo/department.html')

#添加部门
def add_depart(request):
	d_id = request.GET.get('d_id')
	d_name = request.GET.get('d_name')
	result = asset_apple_models.add_depart(d_id,d_name)
	return HttpResponse(json.dumps({'result':result}))

#搜索部门
def search_depart(request):
	depart_list = asset_apple_models.search_depart()
	return HttpResponse(json.dumps({'depart_list':depart_list}))

#编辑部门
def edit_depart(request):
	d_id = request.GET.get('d_id')
	d_name = request.GET.get('d_name')
	result = asset_apple_models.edit_depart(d_id,d_name)
	return HttpResponse(json.dumps({'result':result}))

#删除部门
def del_depart(request):
	del_dept_list = request.GET.get('del_dept_list')
	if del_dept_list:
		del_dept_list = json.loads(del_dept_list)
	result = asset_apple_models.del_depart(del_dept_list)
	return HttpResponse(json.dumps({'result':result}))

#资产存放位置页面
def asset_pos_page(request):
	return render(request, 'apple/baseinfo/asset_pos_page.html')

#获取所有资产存放位置数据
def get_all_pos_data(request):
	data = {"code": 0,"msg": "","count": 2,"data": []}
	data['data'] = asset_apple_models.get_all_pos_data()
	return HttpResponse(json.dumps(data))

def asset_edit_page(request):
	return render(request, 'apple/baseinfo/asset_edit_page.html')

#添加资产存放位置
def add_pos(request):
	p_name = request.GET.get('p_name')
	result = asset_apple_models.add_pos(p_name)
	return HttpResponse(json.dumps({'result':result}))

#删除资产存放位置
def del_pos(request):
	p_id = request.GET.get('p_id')
	result = asset_apple_models.del_pos(p_id)
	return HttpResponse(json.dumps({'result':result}))

#修改资产存储位置
def update_pos(request):
	p_id = request.GET.get('p_id')
	p_name = request.GET.get('p_name')
	result = asset_apple_models.update_pos(p_id,p_name)
	return HttpResponse(json.dumps({'result':result}))

def edit_detail(request):
	opr_type = request.GET.get('opr_type')
	if opr_type == 'base':
		return render(request, 'apple/baseinfo/edit_base.html')
	elif opr_type == 'out':
		return render(request, 'apple/baseinfo/edit_out.html')
	elif opr_type == 'out_back':
		return render(request, 'apple/baseinfo/edit_out_back.html')
	elif opr_type == 'zj':
		return render(request, 'apple/baseinfo/edit_zj.html')
	elif opr_type == 'zj_back':
		return render(request, 'apple/baseinfo/edit_zj_back.html')

def history_search(request):
	return render(request, 'apple/general/history_search.html')
	