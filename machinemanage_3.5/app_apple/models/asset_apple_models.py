# -*- coding:utf-8 -*-
from django.db import connections
import datetime

global MODEL
MODEL = 'asset_b'

#用户登录
def login(u_id,u_passwd):
	sql = 'select u_passwd,u_name from users where u_id = \'{0}\''.format(u_id)
	result = False
	u_name = ''
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		row = cur.fetchone()
		if row and u_passwd == row[0]:
			u_name = row[1]
			result = True
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	return result,u_name

'''
	——————————综合查询——————————
'''

#添加部门
def add_depart(d_id,d_name):
	sql = 'insert into depart(d_pid,d_name) values(\'{0}\',\'{1}\')'.format(d_id,d_name)
	result = False
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		result = True
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	return result

#搜索部门
def search_depart():
	sql = 'select d_id,d_pid,d_name from depart order by d_id'
	depart_list = []
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for row in rows:
			d_id,d_pid,d_name = row
			depart_list.append({'id':d_id,'pid':d_pid,'d_name':d_name})
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	return depart_list

#编辑修改部门
def edit_depart(d_id,d_name):
	sql = 'update depart set d_name = \'{1}\' where d_id = \'{0}\''.format(d_id,d_name)
	result = False
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		result = True
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	return result

#删除部门节点及其子节点
def del_depart(del_dept_list):
	str = ''
	for index,d_id in enumerate(del_dept_list):
		if index < len(del_dept_list) - 1:
			str += '\'{0}\','.format(d_id)
		else:
			str += '\'{0}\''.format(d_id)
	sql = 'delete from depart where d_id in ({0})'.format(str)
	result = False
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		result = True
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	return result

#获取所有资产存放位置数据
def get_all_pos_data():
	sql = 'select p_id,p_name from asset_pos order by p_id desc'
	data = []
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for index,row in enumerate(rows):
			p_id,p_name = row
			data.append({'index':index + 1,'p_id':p_id,'p_name':p_name})
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	return data
	
#添加资产存放位置
def add_pos(p_name):
	sql = 'insert into asset_pos(p_name) values(\'{0}\')'.format(p_name)
	result = False
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		result = True
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	return result

#删除资产存放位置
def del_pos(p_id):
	sql = 'delete from asset_pos where p_id = \'{0}\''.format(p_id)
	result = False
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		result = True
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	return result

#修改资产存储位置
def update_pos(p_id,p_name):
	sql = 'update asset_pos set p_name = \'{1}\' where p_id = \'{0}\''.format(p_id,p_name)
	result = False
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		result = True
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	return result

#总账查询页数据显示
def get_total_data():
	data = {'instorage':0, 'zj':0, 'out': 0}
	sql = 'select count(a_cd),a_action_type from asset_material group by a_action_type'
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		if rows:
			for row in rows:
				count,a_action_type = row
				if a_action_type == 0 or a_action_type == 2 or a_action_type == 4:
					data['instorage'] += count
				elif a_action_type == 1:
					data['out'] += count
				elif a_action_type == 3:
					data['zj'] += count
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data