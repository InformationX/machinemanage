# -*- coding:utf-8 -*-
from __future__ import unicode_literals
import os,json,xlwt
from django.db import connections
from machinemanage.settings import BASE_DIR

def get_config(key):
	file_path = os.getcwd() + '/config/dbconfig.json'
	fp = open(file_path)
	json_data = json.load(fp)
	fp.close()
	return json_data[key]

#设置导出的Excel文件样式
def set_style(name,height,bold=False):
	style = xlwt.XFStyle()	#初始化样式
	font = xlwt.Font()
	font.name = name
	font.bold = bold
	font.color_index = 4
	font.height = height
	style.font = font
	return style

#清除media目录下所有的导出Excel文件
def clear_media_dir():
	path = os.path.join(os.path.join(BASE_DIR,'media'),'tmp_folder')
	files = os.listdir(path)
	for file in files:
		f = os.path.join(path,file)
		if os.path.exists(f):
			os.remove(f)

#返回资产行为类型
def get_action_type(a_type):
	if a_type == 0 or a_type == 2 or a_type == 4 or a_type == 9:
		return '在库'
	elif a_type == 1:
		return '已支给'
	elif a_type == 3:
		return '已归还供应商'
	elif a_type == 5 or a_type == 8:
		return '已出库'
	elif a_type == 6:
		return '已销售'
	elif a_type == 7:
		return '已报废'
	elif a_type == 10:
		return '资产转换'
	elif a_type == 11:
		return '修改位置'

def getAppleActionType(a_action_type):
	if a_action_type == 0 or a_action_type == 2 or a_action_type == 4:
		a_action_type = '在库'
	elif a_action_type == 1:
		a_action_type = '出库'
	elif a_action_type == 3:
		a_action_type = '支给'
	return a_action_type 