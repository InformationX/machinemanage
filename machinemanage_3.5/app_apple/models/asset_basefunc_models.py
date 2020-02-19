# -*- coding:utf-8 -*-
from django.db import connections,transaction
import datetime
from config.models import common

global MODEL
MODEL = 'asset_b'

#资产添加
def asset_add(a_cd,a_main_cd,a_type_cd,a_main_serial,a_dept_cd,a_loc_cd,a_state,a_remark,a_opr_user,a_add_time):
	sql = 'insert into asset_material(a_cd, a_main_cd, a_type_cd, a_main_serial, a_dept_cd, a_loc_cd, a_state, a_remark, a_opr_user, a_add_time) \
			values(\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\',\'{8}\',\'{9}\') \
			'.format(a_cd,a_main_cd,a_type_cd,a_main_serial,a_dept_cd,a_loc_cd,a_state,a_remark,a_opr_user,a_add_time)
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

#资产批量添加
def upload_add(a_opr_user,a_add_time,table_data):
	data = {'result':False}
	try:
		sql = 'insert into asset_material(a_cd,a_type_cd,a_fuselage_cd,a_main_cd,a_main_serial,a_dept_cd,a_loc_cd,a_state,a_remark,a_opr_user,a_add_time) \
			values(%s, %s, %s, %s, %s, %s, %s, %s,%s,\'{0}\',\'{1}\')'.format(a_opr_user,a_add_time)

		with transaction.atomic(using=MODEL):
			cur = connections[MODEL].cursor()
			cur.executemany(sql,table_data)
			if cur.rowcount == len(table_data):
				data['result'] = True
				data['num'] = cur.rowcount
	except Exception as e:
		raise e
		data['msg'] = '验证资产番号是否重复!'
	finally:
		connections[MODEL].close()
	return data

#资产批量支给
def upload_zj(zj_list,a_opr_user,a_add_time):
	data = {'result':False,'num':0}
	a_action_type = 3
	try:
		cur = connections[MODEL].cursor()
		with transaction.atomic(using=MODEL):
			for zj in zj_list:
				sql1 = 'insert into asset_zj(a_cd,a_zj_object,a_main_cd,a_main_serial,a_action_state,a_action_remark, \
					a_opr_user,a_add_time) values(\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\') \
					'.format(zj['a_cd'],zj['a_zj_object'], zj['a_main_cd'], zj['a_main_serial'], zj['a_action_state'],zj['a_action_remark'],a_opr_user,a_add_time)
				cur.execute(sql1)

				sql2 = 'select id from asset_zj where a_cd=\'{0}\' and a_add_time=\'{1}\' and a_main_cd=\'{2}\' \
					and a_main_serial=\'{3}\''.format(zj['a_cd'],a_add_time,zj['a_main_cd'],zj['a_main_serial'])
				cur.execute(sql2)
				row = cur.fetchone()
				if row:
					a_id = row[0]
					sql3 = 'update asset_material set a_action_id = \'{0}\',a_action_type=\'{1}\' where \
						a_cd=\'{2}\''.format(a_id,a_action_type,zj['a_cd'])
					cur.execute(sql3)
					if cur.rowcount == 1:
						data['num'] += 1 
	except Exception as e:
		raise e
	finally:
		cur.close()
		connections[MODEL].close()
	return data

def upload_excel_zj(zj_list,a_opr_user,a_add_time):
	'''
	批量支给（Excel）
	'''
	data = {'result':True,'num':0}
	a_action_type = 3
	try:
		cur = connections[MODEL].cursor()
		with transaction.atomic(using=MODEL):

			for zj in zj_list:
				sql1 = 'insert into asset_zj(a_cd,a_zj_object,a_zj_dept,a_main_cd,a_main_serial,a_action_state,a_action_remark,a_opr_user,a_add_time) \
					values(\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\',\'{8}\') returning id\
					'.format(zj['a_cd'],zj['a_zj_object'],zj['a_zj_dept'],zj['a_main_cd'],zj['a_main_serial'],zj['a_action_state'],zj['a_action_remark'],a_opr_user,a_add_time)
				cur.execute(sql1)
				if cur.rowcount == 1:
					a_id = cur.fetchone()[0]
					sql2 = 'update asset_material set a_action_id = {0},a_action_type={1} \
						where a_cd = \'{2}\''.format(a_id,a_action_type,zj['a_cd'])
					cur.execute(sql2)
					if cur.rowcount == 1:
						data['num'] += 1
	except Exception as e:
		data['result'] = False
		raise e
	finally:
		cur.close()
		connections[MODEL].close()
	return data

def upload_excel_zj_revert(zj_revert_list,a_opr_user,a_add_time):
	'''
	批量支给归还(Excel)
	'''
	data = {'result':True,'num':0}
	a_action_type = 4
	try:
		cur = connections[MODEL].cursor()
		with transaction.atomic(using=MODEL):
			for item in zj_revert_list:
				sql1 = 'insert into asset_zj_back(a_cd,a_main_cd,a_main_serial,a_action_state,a_action_loc,a_action_remark,a_opr_user,a_add_time) \
					values(\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\') returning id \
					'.format(item['a_cd'],item['a_main_cd'],item['a_main_serial'],item['a_action_state'],item['a_action_loc'],item['a_action_remark'],a_opr_user,a_add_time)
				cur.execute(sql1)
				if cur.rowcount == 1:
					a_id = cur.fetchone()[0]
					sql2 = 'update asset_material set a_action_id = {0},a_action_type={1} \
						where a_cd = \'{2}\''.format(a_id,a_action_type,item['a_cd'])
					cur.execute(sql2)
					if cur.rowcount == 1:
						data['num'] += 1
	except Exception as e:
		data['result'] = False
		raise e
	finally:
		cur.close()
		connections[MODEL].close()
	return data

def upload_excel_out(out_list,a_opr_user,a_add_time):
	'''
	批量出库（Excel）
	'''
	data = {'result':True,'num':0}
	a_action_type = 1
	try:
		cur = connections[MODEL].cursor()
		with transaction.atomic(using=MODEL):
			for out in out_list:
				sql1 = 'insert into asset_out(a_cd,a_main_cd,a_main_serial,a_action_dept,a_action_loc,a_action_state,a_action_model,a_take_user,a_confirm_user,a_action_remark,a_opr_user,a_add_time) \
					values(\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\',\'{8}\',\'{9}\',\'{10}\',\'{11}\') returning id\
					'.format(out['a_cd'],out['a_main_cd'],out['a_main_serial'],out['a_action_dept'],out['a_action_loc'],out['a_action_state'],out['a_action_model'],out['a_take_user'],out['a_confirm_user'],out['a_action_remark'],a_opr_user,a_add_time)
				cur.execute(sql1)
				if cur.rowcount == 1:
					a_id = cur.fetchone()[0]
					sql2 = 'update asset_material set a_action_id = {0},a_action_type={1} \
						where a_cd = \'{2}\''.format(a_id,a_action_type,out['a_cd'])
					cur.execute(sql2)
					if cur.rowcount == 1:
						data['num'] += 1
	except Exception as e:
		data['result'] = False
		raise e
	finally:
		cur.close()
		connections[MODEL].close()
	return data

def upload_excel_out_back(assetList,a_opr_user,a_add_time):
	'''
	批量退库（Excel）
	'''
	data = {'result':True,'num':0}
	a_action_type = 2
	try:
		cur = connections[MODEL].cursor()
		with transaction.atomic(using=MODEL):
			for item in assetList:
				sql1 = 'insert into asset_out_back(a_cd,a_main_cd,a_main_serial,a_origin_loc,a_action_loc,a_action_state,a_back_user,a_confirm_user,a_action_remark,a_opr_user,a_add_time) \
					values(\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\',\'{8}\',\'{9}\',\'{10}\') returning id \
					'.format(item['a_cd'],item['a_main_cd'],item['a_main_serial'],item['a_origin_loc'],item['a_action_loc'],item['a_action_state'],item['a_back_user'],item['a_confirm_user'],item['a_action_remark'],a_opr_user,a_add_time)
				cur.execute(sql1)
				if cur.rowcount == 1:
					a_id = cur.fetchone()[0]
					sql2 = 'update asset_material set a_action_id = {0},a_action_type={1} \
						where a_cd = \'{2}\''.format(a_id,a_action_type,item['a_cd'])
					cur.execute(sql2)
					if cur.rowcount == 1:
						data['num'] += 1
	except Exception as e:
		data['result'] = False
		raise e
	finally:
		cur.close()
		connections[MODEL].close()
	return data

#出库前查询
'''
def get_out_data(assetList):
	data = []
	try:
		cur = connections[MODEL].cursor()
		for asset in assetList:
			sql = 'select a_type_cd,a_main_cd,a_main_serial,a_loc_cd,a_action_id,a_action_type, \
				a_state,a_remark from asset_material where a_cd = \'{0}\''.format(asset)
			cur.execute(sql)
			row = cur.fetchone()
			if row:
				a_type_cd,a_main_cd,a_main_serial,a_loc_cd,a_action_id,a_action_type,a_state,a_remark = row
				item = {
					'a_cd':asset,'a_type_cd':a_type_cd,'a_main_cd':a_main_cd,
					'a_action_remark':a_remark,'a_main_serial':a_main_serial,'a_action_upload':'未上传'
				}

				if a_action_type == 0:
					item['a_current_line'] = '库房'
					item['a_current_loc'] = a_loc_cd
					item['a_action_state'] = a_state
					item['a_action_type'] = '在库'
				elif a_action_type == 1:
					sql = 'select a_o.a_main_cd,a_o.a_main_serial,a_o.a_take_line,a_o.a_action_loc, \
						a_o.a_take_user,a_o.a_confirm_user,a_o.a_action_remark from asset_material a_m, \
						asset_out a_o where a_m.a_action_id = a_o.id and a_m.a_cd = \'{0}\''.format(asset)
					cur.execute(sql)
					row = cur.fetchone()
					if row:
						item['a_main_cd'] = row[0]
						item['a_main_serial'] = row[1]
						item['a_current_line'] = row[2]
						item['a_current_loc'] = row[3]
						item['a_take_user'] = row[4]
						item['a_confirm_user'] = row[5]
						item['a_action_remark'] = row[6]
						item['a_action_type'] = '出库'
				data.append(item)
			else:
				data.append({'a_cd':asset,'a_action_type':'未入库'})
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data
'''

#资产出库
def upload_out(assetList,a_opr_user,a_add_time):
	num = 0
	a_action_type = 1
	try:
		cur = connections[MODEL].cursor()
		with transaction.atomic(using=MODEL):
			for asset in assetList:
				sql1 = 'insert into asset_out(a_cd,a_action_state,a_main_cd,a_main_serial,a_take_line, \
					a_action_loc,a_take_user,a_confirm_user,a_action_remark,a_opr_user,a_add_time) values \
					(\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\',\'{8}\',\'{9}\',\'{10}\') \
					'.format(asset['a_cd'],asset['a_action_state'],asset['a_main_cd'],asset['a_main_serial'],
						asset['a_take_line'],asset['a_action_loc'],asset['a_take_user'],
						asset['a_confirm_user'],asset['a_action_remark'],a_opr_user,a_add_time)
				cur.execute(sql1)
				if cur.rowcount == 1:
					sql2 = 'select id from asset_out where a_cd = \'{0}\' and a_add_time = \'{1}\''.format(asset['a_cd'],a_add_time)
					cur.execute(sql2)
					row = cur.fetchone()
					if row:
						a_id = row[0]
						sql3 = 'update asset_material set a_action_id = {0},a_action_type={1} where a_cd = \'{2}\''.format(a_id,a_action_type,asset['a_cd'])
						cur.execute(sql3)
						if cur.rowcount == 1:
							num += 1
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return num

def asset_out_detail(a_cd):
	a_action_type = 1
	try:
		cur = connections[MODEL].cursor()
		sql = 'select a_m.a_type_cd,a_m.a_fuselage_cd,a_o.a_main_cd,a_o.a_main_serial, \
			a_o.a_take_line,a_o.a_action_loc,a_o.a_action_state from asset_material a_m,asset_out a_o \
			where a_m.a_action_id = a_o.id and a_m.a_cd = \'{0}\' \
			and a_m.a_action_type = {1}'.format(a_cd,a_action_type)
		cur.execute(sql)
		row = cur.fetchone()
		if row:
			data = {
				'a_type_cd':row[0],'a_fuselage_cd':row[1],'a_main_cd':row[3],
				'a_main_serial':row[3],'a_take_line':row[4],'a_action_loc':row[5],
				'a_action_state':row[6],'result':True,'a_action_type':'已出库'
			}
		else:
			sql = 'select a_type_cd,a_fuselage_cd,a_action_type from asset_material where a_cd = \'{0}\''.format(a_cd)
			cur.execute(sql)
			row = cur.fetchone()
			if row:
				a_action_type = common.getAppleActionType(row[2])
				data = {
					'a_type_cd':row[0],'a_fuselage_cd':row[1],'a_cd':a_cd,
					'a_action_type':a_action_type,'result':False,'msg':'该资产未出库!'
				}
			else:
				data = {'result':False,'msg':'未搜索到出库数据!'}
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

def asset_out_single(a_cd,a_action_shelf,a_action_state,a_back_user,a_confirm_user,a_main_cd,a_main_serial,a_opr_user,a_add_time):
	result = False
	a_action_type = 2
	try:
		with transaction.atomic(using=MODEL):
			cur = connections[MODEL].cursor()
			sql = 'insert into asset_out_back(a_cd,a_action_shelf,a_action_state, \
				a_back_user,a_confirm_user,a_main_cd,a_main_serial,a_opr_user,a_add_time) \
				values(\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\',\'{8}\') \
				'.format(a_cd,a_action_shelf,a_action_state,a_back_user,a_confirm_user,a_main_cd,a_main_serial,a_opr_user,a_add_time)
			cur.execute(sql)
			if cur.rowcount == 1:
				sql = 'select id from asset_out_back where a_cd = \'{0}\' and a_add_time = \'{1}\''.format(a_cd,a_add_time)
				cur.execute(sql)
				row = cur.fetchone()
				if row:
					id = row[0]
					sql = 'update asset_material set a_action_id = {0},a_action_type = {1} where a_cd = \'{2}\''.format(id,a_action_type,a_cd)
					cur.execute(sql)
					if cur.rowcount == 1:
						result = 1
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return result

#支给前查询
def zj_revert_detail(assetList):
	data = []
	try:
		cur = connections[MODEL].cursor()
		sql = 'select * from (select a_m.a_cd,a_m.a_type_cd,a_m.a_fuselage_cd,a_z.a_zj_object,\
			a_z.a_action_state,a_z.a_main_cd,a_z.a_main_serial,a_m.a_action_type \
			from asset_material a_m left join asset_zj a_z on a_m.a_action_id = a_z.id) zj \
			where zj.a_cd in ('
		for index,a_cd in enumerate(assetList):
			if index < len(assetList) - 1:
				sql += '\'{0}\','.format(a_cd)
			else:
				sql += '\'{0}\''.format(a_cd)
		sql += ')'
		cur.execute(sql)
		rows = cur.fetchall()
		for row in rows:
			a_action_type = common.getAppleActionType(row[7])
			data.append({
				'a_cd':row[0],'a_type_cd':row[1],'a_fuselage_cd':row[2],'a_zj_object':row[3],
				'a_action_state':row[4],'a_main_cd':row[5],'a_main_serial':row[6],'a_action_type':a_action_type
			})
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data
	
def zj_back(assetList,a_opr_user,a_add_time):
	a_action_type = 4
	num = 0
	try:
		with transaction.atomic(using=MODEL):
			cur = connections[MODEL].cursor()
			for asset in assetList:
				sql = 'insert into asset_zj_back(a_cd,a_action_state,a_action_loc,a_main_cd,a_main_serial,a_action_remark,a_opr_user,a_add_time) \
					 values (\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\') \
					'.format(asset['a_cd'],asset['a_action_state'],asset['a_action_loc'],asset['a_main_cd'],asset['a_main_serial'],asset['a_action_remark'],a_opr_user,a_add_time)
				cur.execute(sql)
				if cur.rowcount == 1:
					sql = 'select id from asset_zj_back where a_cd = \'{0}\' and a_add_time = \'{1}\''.format(asset['a_cd'],a_add_time)
					cur.execute(sql)
					row = cur.fetchone()
					if row:
						id = row[0]
						sql = 'update asset_material set a_action_type = {0},a_action_id = {1} where a_cd = \'{2}\''.format(a_action_type,id,asset['a_cd'])
						cur.execute(sql)
						if cur.rowcount == 1:
							num += 1
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return num

#资产退库
def upload_out_back(assetList,a_opr_user,a_add_time):
	a_action_type = 2
	num = 0
	try:
		with transaction.atomic(using=MODEL):
			cur = connections[MODEL].cursor()
			for asset in assetList:
				sql = 'insert into asset_out_back(a_cd,a_action_state,a_action_loc,a_main_cd, \
					a_main_serial,a_back_user,a_confirm_user,a_action_remark,a_opr_user,a_add_time) \
					values(\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\',\'{8}\',\'{9}\') \
					'.format(asset['a_cd'],asset['a_action_state'],asset['a_action_loc'],asset['a_main_cd'],
						asset['a_main_serial'],asset['a_back_user'],asset['a_confirm_user'],
						asset['a_action_remark'],a_opr_user,a_add_time)
				cur.execute(sql)
				if cur.rowcount == 1:
					sql = 'select id from asset_out_back where a_cd = \'{0}\' and a_add_time = \'{1}\''.format(asset['a_cd'],a_add_time)
					cur.execute(sql)
					row = cur.fetchone()
					if row:
						id = row[0]
						sql = 'update asset_material set a_action_type = {0},a_action_id = {1} where a_cd = \'{2}\''.format(a_action_type,id,asset['a_cd'])
						cur.execute(sql)
						if cur.rowcount == 1:
							num += 1
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return num

#批量修改资产位置
def upload_edit_loc(editList):
	data = {'num':0, 'result':True}
	try:
		with transaction.atomic(using=MODEL):
			cur = connections[MODEL].cursor()
			for edit in editList:
				a_action_type = edit['a_action_type']
				if a_action_type == '入库':
					sql = 'update asset_material set a_main_cd = \'{0}\', a_main_serial = \'{1}\', a_dept_cd = \'{2}\', a_loc_cd = \'{3}\' where a_cd = \'{4}\''.format(edit['a_main_cd'],edit['a_main_serial'],edit['a_action_dept'],edit['a_action_loc'],edit['a_cd'])
				elif a_action_type == '已出库':
					sql = 'update asset_out set a_main_cd = \'{0}\', a_main_serial = \'{1}\', a_action_dept = \'{2}\', a_action_loc = \'{3}\' where id = {4}'.format(edit['a_main_cd'],edit['a_main_serial'],edit['a_action_dept'],edit['a_action_loc'],edit['a_action_id'])
				elif a_action_type == '退库':
					sql = 'update asset_out_back set a_main_cd = \'{0}\', a_main_serial = \'{1}\', a_action_dept = \'{2}\', a_action_loc = \'{3}\' where id = {4}'.format(edit['a_main_cd'],edit['a_main_serial'],edit['a_action_dept'],edit['a_action_loc'],edit['a_action_id'])
				elif a_action_type == '已支给':
					sql = 'update asset_zj set a_main_cd = \'{0}\', a_main_serial = \'{1}\', a_zj_dept = \'{2}\', a_zj_object = \'{3}\' where id = {4}'.format(edit['a_main_cd'],edit['a_main_serial'],edit['a_action_dept'],edit['a_action_loc'],edit['a_action_id'])
				elif a_action_type == '支给归还':
					sql = 'update asset_out_back set a_main_cd = \'{0}\', a_main_serial = \'{1}\', a_action_dept = \'{2}\', a_action_loc = \'{3}\' where id = {4}'.format(edit['a_main_cd'],edit['a_main_serial'],edit['a_action_dept'],edit['a_action_loc'],edit['a_action_id'])
				else:
					continue

				cur.execute(sql)
				if cur.rowcount == 1:
					data['num'] += 1
	except Exception as e:
		data['result'] = False
		raise e
	finally:
		connections[MODEL].close()
	return data