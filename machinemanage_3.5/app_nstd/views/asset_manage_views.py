# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from app_nstd.models import asset_manage_models
import json,datetime

#获取所有用户信息
def getUser(request):
	data = {
	  "code": 0,
  	  "msg": "",
      "count": 0,
	  "data": []
	}
	data['data'] = asset_manage_models.getUser()
	return HttpResponse(json.dumps(data))

#删除用户
def userDelete(request):
	user_num = request.GET.get('user_num')
	result = asset_manage_models.userDelete(user_num)
	return HttpResponse(json.dumps({'result':result}))

#更新用户
def userUpdate(request):
	user_num = request.POST.get('user_num')
	user_name = request.POST.get('user_name')
	user_depart = request.POST.get('user_depart')
	user_phone = request.POST.get('user_phone')
	user_email = request.POST.get('user_email')
	user_title = request.POST.get('user_title')

	result = asset_manage_models.userUpdate(user_num,user_name,user_depart,user_phone,user_email,user_title)
	return HttpResponse(json.dumps({'result':result}))

#添加用户
def userAdd(request):
	user_num = request.POST.get('user_num')
	user_name = request.POST.get('user_name')
	user_depart = request.POST.get('user_depart')
	user_phone = request.POST.get('user_phone')
	user_email = request.POST.get('user_email')
	user_title = request.POST.get('user_title')
	opr_user = request.session.get('u_nstd_id',None)
	add_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	result = asset_manage_models.userAdd(user_num,user_name,
		user_depart,user_phone,user_email,user_title,opr_user,add_time)
	return HttpResponse(json.dumps({'result':result}))

#修改用户访问权限
def updateAuthority(request):
	data = request.POST.get('data')
	user_num = request.POST.get('user_num')
	result = asset_manage_models.updateAuthority(user_num,data.replace('\'','\"'))
	return HttpResponse(json.dumps({'result':result}))

#查询权限
def getAuthority(request):
	user_num = request.GET.get('user_num')
	data = asset_manage_models.getAuthority(user_num)
	return HttpResponse(json.dumps(data))