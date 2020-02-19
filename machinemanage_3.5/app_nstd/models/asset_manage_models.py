# -*- coding:utf-8 -*-
from django.db import connections,transaction
import datetime

global MODEL
MODEL = 'asset_nstd'

#获取用户
def getUser():
	data = []
	try:
		sql = 'select u.u_id,u.u_name,u.u_authority,u.u_phone,u.u_email,u.u_title,u.u_dept_id,d.d_name \
			from users u,depart d where u.u_dept_id = d.d_id and u.u_authority = 2 order by u.u_add_time desc'
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		if rows:
			for row in rows:
				data.append({
					'user_num':row[0],'user_name':row[1],'user_authority':row[2],'user_phone':row[3],
					'user_email':row[4],'user_title':row[5],'dept_id':row[6],'depart_name':row[7]
				})
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

#删除用户
def userDelete(user_num):
	result = False
	try:
		sql = 'delete from users where u_id = \'{0}\''.format(user_num)
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		if cur.rowcount == 1:
			result = True
	except Exception as e:
		raise e
	finally:
		connections[MODEL].cursor()
	return result

#更新用户
def userUpdate(user_num,user_name,user_depart,user_phone,user_email,user_title):
	result = False
	try:
		sql = 'update users set u_name = \'{0}\',u_phone=\'{1}\',u_email=\'{2}\',u_title=\'{3}\',u_dept_id=\'{4}\' \
			where u_id = \'{5}\''.format(user_name,user_phone,user_email,user_title,user_depart,user_num)
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		if cur.rowcount == 1:
			result = True
	except Exception as e:
		raise e
	finally:
		connections[MODEL].cursor()
	return result

#添加用户
def userAdd(user_num,user_name,user_depart,user_phone,user_email,user_title,u_opr_user,u_add_time):
	result = False
	try:
		sql = 'insert into users(u_id,u_name,u_phone,u_email,u_title,u_dept_id,u_opr_user,u_add_time) \
			values(\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\') \
			'.format(user_num,user_name,user_phone,user_email,user_title,user_depart,u_opr_user,u_add_time)
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		if cur.rowcount == 1:
			result = True
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].cursor()
	return result

#修改用户权限
def updateAuthority(user_num,data):
	result = False
	try:
		sql = 'select user_num from asset_authority where user_num = \'{0}\''.format(user_num)
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		row = cur.fetchone()
		if row:
			sql = 'update asset_authority set user_authority = \'{0}\' where user_num = \'{1}\''.format(data,user_num)
		else:
			sql = 'insert into asset_authority(user_num,user_authority) values(\'{0}\',\'{1}\')'.format(user_num,data)
		cur.execute(sql)
		if cur.rowcount == 1:
			result = True
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return result

#查询用户权限
def getAuthority(user_num):
	data = {'result':False}
	try:
		sql = 'select user_authority from asset_authority where user_num = \'{0}\''.format(user_num)
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		row = cur.fetchone()
		if row:
			data['user_authority'],data['result'] = row[0],True
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data