# -*- coding:utf-8 -*-
from django.db import connections
import datetime

global MODEL
MODEL = 'asset_nstd'

#登录操作
def login(u_id,u_passwd):
	sql = 'select u.u_passwd,u.u_name,u.u_authority,d.d_name from users u,depart d \
		where u.u_dept_id = d.d_id and u.u_id = \'{0}\''.format(u_id)
	result = False
	u_name = authority_level = dept_name = ''
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		row = cur.fetchone()
		if row and u_passwd == row[0]:
			u_name = row[1]
			authority_level = row[2]
			dept_name = row[3]
			result = True
		else:
			authority_level = 0
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	return result,u_name,authority_level,dept_name

#修改密码
def upd_passwd(u_id,old_passwd,new_passwd):
	sql = 'select u_passwd from users where u_id = \'{0}\''.format(u_id)
	data = {'result':False}
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		row = cur.fetchone()
		if row and row[0] == old_passwd:
			sql = 'update users set u_passwd = \'{0}\' where u_id = \'{1}\''.format(new_passwd,u_id)
			cur.execute(sql)
			if cur.rowcount == 1:
				data['result'] = True
		else:
			data['msg'] = '原密码输入错误!'
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

#所有资产类型的数据统计
def total_search():
	data = {
		'instorage':0,'zj':0,'loan_revert':0,'online':0,'sale':0,'scrap':0
	}
	sql1 = 'select a_action_id,count(a_id) from asset_material where a_action_id = 0 \
			group by a_action_id'
	sql2 = 'select a_a.a_action_type,count(a_m.a_id) from asset_material a_m,asset_action a_a \
			where a_m.a_action_id = a_a.a_id group by a_a.a_action_type'
	sql = '{0} union all {1}'.format(sql1,sql2)
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for row in rows:
			a_type,num = row
			if a_type == 0 or a_type == 2 or a_type == 4 or a_type == 9:
				data['instorage'] += num
			elif a_type == 1:
				data['zj'] += num
			elif a_type == 3:
				data['loan_revert'] += num
			elif a_type == 5 or a_type == 8:
				data['online'] += num
			elif a_type == 6:
				data['sale'] += num
			elif a_type == 7:
				data['scrap'] += num
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data