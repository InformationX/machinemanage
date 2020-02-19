# -*- coding:utf-8 -*-
from django.db import connections

global MODEL
MODEL = 'asset_b'

def get_detail(a_cd):
	sql = 'select a_action_type from asset_material where a_cd = \'{0}\''.format(a_cd)
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		row = cur.fetchone()
		if row:
			a_action_type = trans_action_type(row[0])
		else:
			a_action_type = '未入库'
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return (a_action_type,)

def getDetailMsg(a_cd):
	data = {}

	sql_0 = 'select a_type_cd,a_action_type,a_action_id,a_loc_cd from asset_material where a_cd = \'{0}\' and a_action_type = 0'.format(a_cd)
	sql_1 = 'select a_m.a_type_cd,a_m.a_action_type,a_m.a_action_id,a_o.a_action_loc from asset_material a_m,asset_out a_o where a_m.a_action_type = 1 and a_m.a_action_id = a_o.id and a_m.a_cd = \'{0}\''.format(a_cd)
	sql_2 = 'select a_m.a_type_cd,a_m.a_action_type,a_m.a_action_id,aob.a_action_loc from asset_material a_m,asset_out_back aob where a_m.a_action_type = 2 and a_m.a_action_id = aob.id and a_m.a_cd = \'{0}\''.format(a_cd)
	sql_3 = 'select a_m.a_type_cd,a_m.a_action_type,a_m.a_action_id,azj.a_zj_object from asset_material a_m,asset_zj azj where a_m.a_action_type = 3 and a_m.a_action_id = azj.id and a_m.a_cd = \'{0}\''.format(a_cd)
	sql_4 = 'select a_m.a_type_cd,a_m.a_action_type,a_m.a_action_id,azb.a_action_loc from asset_material a_m,asset_zj_back azb where a_m.a_action_type = 4 and a_m.a_action_id = azb.id and a_m.a_cd = \'{0}\''.format(a_cd)
	sql = '{0} union {1} union {2} union {3} union {4}'.format(sql_0,sql_1,sql_2,sql_3,sql_4)
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		row = cur.fetchone()
		if row:
			data['a_type_cd'] = row[0]
			data['a_action_type'] = row[1]
			data['a_action_id'] = row[2]
			data['a_action_loc'] = row[3]
		else:
			data['a_type_cd'] = '未入库'
			data['a_action_type'] = '未入库'
			data['a_action_loc'] = '未入库'
			data['a_action_id'] = 0
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

def trans_action_type(a_action_type):
	if a_action_type != '未入库':
		a_action_type = int(a_action_type)
	if a_action_type == 0:
		a_action_type = '入库'
	elif a_action_type == 1:
		a_action_type = '已出库'
	elif a_action_type == 2:
		a_action_type = '退库'		
	elif a_action_type == 3:
		a_action_type = '已支给'
	elif a_action_type == 4:
		a_action_type = '支给归还'
	return a_action_type
