# -*- coding:utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from app_nstd.models import asset_nstd_models
from app_nstd.models import asset_manage_models
import json,datetime

def index(request):
	if not request.session.get('u_nstd_id',None):
		return HttpResponseRedirect('/nstd/login_page')
	return render(request, 'nstd/index.html')

def login_page(request):
	return render(request, 'nstd/login.html')

def login(request):
	u_id = request.POST.get('u_id')
	u_passwd = request.POST.get('u_passwd')
	result,u_name,authority_level,dept_name = asset_nstd_models.login(u_id,u_passwd)
	if result:
		request.session['u_nstd_id'] = u_id
		request.session['u_nstd_name'] = u_name
		request.session['dept_name'] = dept_name
		request.session['authority_level'] = authority_level
		if authority_level == 2:	#普通用户权限
			data = asset_manage_models.getAuthority(u_id)
			if data['result']:
				request.session['authority'] = data['user_authority']
		return HttpResponse(json.dumps({'result':True}))
	else:
		return HttpResponse(json.dumps({'result':False,'msg':'用户名或密码错误！'}))

def logout(request):
	try:
		del request.session['u_nstd_id']
		del request.session['u_nstd_name']
	except Exception as e:
		print(e)
	return HttpResponseRedirect('/nstd/login_page')

#用户管理页面
def user_manage(request):
	return render(request, 'nstd/user_manage.html')

#权限修改页面
def authority_page(request):
	return render(request, 'nstd/authority_page.html')

#基本功能
def asset_add_page(request):
	return render(request, 'nstd/basefunc/asset_add_page.html')

#设备出库记账
def asset_out_page(request):
	return render(request, 'nstd/basefunc/asset_out_page.html')

#支给设备
def asset_zj_page(request):
	return render(request, 'nstd/basefunc/asset_zj_page.html')

#支给设备归还
def asset_zj_revert_page(request):
	return render(request, 'nstd/basefunc/asset_zj_revert_page.html')

#借用设备归还
def asset_loan_revert_page(request):
	return render(request, 'nstd/basefunc/asset_loan_revert_page.html')

#设备退库记账
def asset_back_page(request):
	return render(request, 'nstd/basefunc/asset_back_page.html')

#设备销售记账
def asset_sale_page(request):
	return render(request, 'nstd/basefunc/asset_sale_page.html')

#设备报废记账
def asset_scrap_page(request):
	return render(request, 'nstd/basefunc/asset_scrap_page.html')

#在线移动
def asset_online_move_page(request):
	return render(request, 'nstd/basefunc/asset_online_move_page.html')

#库房内部移动
def asset_instorage_move_page(request):
	return render(request, 'nstd/basefunc/asset_instorage_move_page.html')

#-----综合查询-----

#总账信息页面
def total_search(request):
	data = asset_nstd_models.total_search()
	return render(request, 'nstd/general/total_search.html',{'data':data})

#在库信息也面
def in_storage_search(request):
	return render(request, 'nstd/general/in_storage_page.html')

#在线查询页面
def on_line_search(request):
	return render(request, 'nstd/general/on_line_search.html')

#支给归还页面
def zj_revert_page(request):
	return render(request, 'nstd/general/zj_revert_page.html')

#设备出库页面
def out_storage_search(request):
	return render(request, 'nstd/general/out_storage_search.html')

#设备退库页面
def back_storage_search(request):
	return render(request, 'nstd/general/back_storage_search.html')

#借用设备归还
def loan_revert_search(request):
	return render(request, 'nstd/general/loan_revert_search.html')

#设备销售页面
def sale_search(request):
	return render(request, 'nstd/general/sale_search.html')

def scrap_search(request):
	return render(request, 'nstd/general/scrap_search.html')

#获取移动数据
def move_search_page(request):
	return render(request, 'nstd/general/move_search_page.html')

#-----基本信息设置-----

def asset_pos_page(request):
	return render(request, 'nstd/baseinfo/asset_pos_page.html')

#部门管理
def depart_page(request):
	return render(request, 'nstd/baseinfo/depart_page.html')

#资产基本信息修改界面
def asset_update_page(request):
	return render(request, 'nstd/baseinfo/asset_update_page.html')

#手持移动机种界面
def mobile_model_page(request):
	return render(request, 'nstd/baseinfo/mobile_model_page.html')

#修改密码页面
def upd_passwd_page(request):
	return render(request, 'nstd/upd_passwd_page.html')

#修改密码
def upd_passwd(request):
	old_passwd = request.POST.get('old_passwd')
	new_passwd = request.POST.get('new_passwd')
	u_id = request.session.get('u_nstd_id',None)
	if not u_id:
		return HttpResponse(json.dumps({'result':False,'msg':'您未登录或登录已失效，请重新登录'}))
	data = asset_nstd_models.upd_passwd(u_id,old_passwd,new_passwd)
	return HttpResponse(json.dumps(data))

#-----计量信息管理-----

#资产计量确认
def cal_confirm_page(request):
	return render(request,'nstd/calculate/cal_confirm_page.html')

#计量导入界面
def cal_import_page(request):
	return render(request,'nstd/calculate/cal_import_page.html')

#计量查询页面
def cal_search_page(request):
	return render(request,'nstd/calculate/cal_search_page.html')

#计量记录查询界面
def cal_record_page(request):
	return render(request, 'nstd/calculate/cal_record_page.html')

#资产计量修改界面
def cal_update_page(request):
	return render(request, 'nstd/calculate/cal_update_page.html')

#在线盘点页面
def online_ventory(request):
	return render(request, 'nstd/ventory/online_ventory.html')

def instorage_ventory(request):
	return render(request, 'nstd/ventory/instorage_ventory.html')
