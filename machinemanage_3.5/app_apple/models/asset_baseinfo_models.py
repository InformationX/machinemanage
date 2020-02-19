# -*- coding:utf-8 -*-
from django.db import connections, transaction
from config.models import common
import json,datetime

global MODEL
MODEL = 'asset_b'

#查询基础信息
def get_base_detail(a_cd):
	try:
		sql = 'select a_type_cd,a_fuselage_cd,a_main_cd,a_main_serial,a_loc_cd,a_state, \
			a_remark,a_dept_cd from asset_material where a_cd = \'{0}\''.format(a_cd)
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		row = cur.fetchone()
		if row:
			data = {
				'a_type_cd':row[0],'a_fuselage_cd':row[1],'a_main_cd':row[2],
				'a_main_serial':row[3],'a_action_loc':row[4],'a_action_state':row[5],
				'a_action_remark':row[6],'a_dept_cd':row[7],'result':True
			}
		else:
			data = {'result':False,'msg':'未搜索到数据!'}
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

#编辑基础信息
def edit_base(a_cd,a_type_cd,a_fuselage_cd,a_main_cd,a_main_serial,a_action_loc,a_action_state,a_dept_cd,a_action_remark):
	result = False
	try:
		sql = 'update asset_material set a_type_cd=\'{0}\',a_fuselage_cd=\'{1}\', a_main_cd=\'{2}\', \
			a_main_serial=\'{3}\', a_loc_cd=\'{4}\', a_state=\'{5}\', a_dept_cd=\'{6}\', a_remark=\'{7}\' where a_cd = \'{8}\' \
			'.format(a_type_cd,a_fuselage_cd,a_main_cd,a_main_serial,a_action_loc,a_action_state,a_dept_cd,a_action_remark,a_cd)
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		if cur.rowcount == 1:
			result = True
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return result

#获取出库详情
def get_out_detail(a_cd):
	try:
		sql = 'select a_m.a_type_cd,a_o.a_main_cd,a_o.a_main_serial,a_o.a_take_line,a_o.a_take_user, \
			a_o.a_action_loc,a_o.a_action_state, a_o.a_confirm_user,a_o.a_action_remark,a_o.id from asset_material a_m, \
			asset_out a_o where a_m.a_action_id = a_o.id and a_m.a_cd = \'{0}\''.format(a_cd)
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		row = cur.fetchone()
		if row:
			data = {
				'a_type_cd':row[0],'a_main_cd':row[1],'a_main_serial':row[2],
				'a_take_line':row[3],'a_take_user':row[4],'a_action_loc':row[5],
				'a_action_state':row[6],'a_confirm_user':row[7],'a_action_remark':row[8],
				'id':row[9],'result':True
			}
		else:
			data = {'result':False, 'msg':'未搜到出库数据!'}
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

#编辑退库信息
def edit_out(a_main_cd,a_main_serial,a_take_line,a_take_user,a_action_loc,a_action_state,a_confirm_user,a_action_remark,id):
	result = False	
	try:
		sql = 'update asset_out set a_main_cd = \'{0}\',a_main_serial = \'{1}\',a_take_line = \'{2}\',a_take_user = \'{3}\', \
			a_action_loc = \'{4}\', a_action_state = \'{5}\', a_confirm_user = \'{6}\', a_action_remark = \'{7}\' \
			where id = {8}'.format(a_main_cd,a_main_serial,a_take_line,a_take_user,a_action_loc,a_action_state,a_confirm_user,a_action_remark,id)
		cur = connections[MODEL].cursor()	
		cur.execute(sql)
		if cur.rowcount == 1:
			result = True		
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return result

#查询退库详情
def get_out_back(a_cd):
	try:
		sql = 'select a_m.a_type_cd, aob.a_main_cd, aob.a_main_serial, aob.a_back_user, \
			aob.a_action_loc, aob.a_action_state, aob.a_confirm_user, aob.a_action_remark, aob.id \
		 	from asset_material a_m, asset_out_back aob where a_m.a_action_id = aob.id and a_m.a_cd = \'{0}\''.format(a_cd)
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		row =cur.fetchone()
		if row:
			data = {
				'a_type_cd':row[0], 'a_main_cd':row[1], 'a_main_serial':row[2],
				'a_back_user':row[3], 'a_action_loc':row[4], 'a_action_state':row[5],
				'a_confirm_user':row[6], 'a_action_remark':row[7], 'id':row[8], 'result':True
			}
		else:
			data = {'result':False, 'msg':'未搜索到退库数据'}
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

#编辑退库信息
def edit_out_back(a_main_cd,a_main_serial,a_back_user,a_action_loc,a_action_state,a_confirm_user,a_action_remark,id):
	result = False	
	try:
		sql = 'update asset_out_back set a_main_cd = \'{0}\',a_main_serial = \'{1}\', \
			a_back_user = \'{2}\',a_action_loc = \'{3}\',a_action_state = \'{4}\', \
			a_confirm_user = \'{5}\',a_action_remark = \'{6}\' where id = {7} \
			'.format(a_main_cd,a_main_serial,a_back_user,a_action_loc,a_action_state,a_confirm_user,a_action_remark,id)
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		if cur.rowcount == 1:
			result = True
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return result

#查询支给详情
def get_zj_detail(a_cd):
	try:
		sql = 'select a_m.a_type_cd, a_z.a_main_cd, a_z.a_main_serial, a_z.a_zj_object, a_z.a_action_state, \
			a_z.a_action_remark, a_z.id from asset_material a_m,asset_zj a_z where a_m.a_action_id = a_z.id \
			and a_m.a_cd = \'{0}\''.format(a_cd)
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		row = cur.fetchone()
		if row:
			data = {
				'a_type_cd':row[0],'a_main_cd':row[1],'a_main_serial':row[2],'a_zj_object':row[3],
				'a_action_state':row[4],'a_action_remark':row[5],'id':row[6],'result':True
			}
		else:
			data = {'result':False, 'msg':'未搜索到支给数据!'}
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

#编辑支给信息
def edit_zj(a_main_cd,a_main_serial,a_zj_object,a_action_state,a_action_remark,id):
	result = False
	try:
		sql = 'update asset_zj set a_main_cd = \'{0}\', a_main_serial = \'{1}\', \
			a_zj_object = \'{2}\', a_action_state = \'{3}\', a_action_remark = \'{4}\' where id = {5} \
			'.format(a_main_cd,a_main_serial,a_zj_object,a_action_state,a_action_remark,id)
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		if cur.rowcount == 1:
			result = True
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return result

#查询支给归还
def get_zj_back(a_cd):
	try:
		sql = 'select a_m.a_type_cd,azb.a_main_cd,azb.a_main_serial,azb.a_action_loc, \
			azb.a_action_state,azb.a_action_remark,azb.id from asset_material a_m,asset_zj_back azb \
			where a_m.a_action_id = azb.id and a_m.a_cd = \'{0}\''.format(a_cd)
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		row = cur.fetchone()
		if row:
			data = {
				'a_type_cd':row[0],'a_main_cd':row[1],'a_main_serial':row[2],'a_action_loc':row[3],
				'a_action_state':row[4],'a_action_remark':row[5],'id':row[6],'result':True
			}
		else:
			data = {'result':False, 'msg':'未搜索到支给归还数据'}
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

#支给归还
def edit_zj_back(a_main_cd,a_main_serial,a_action_loc,a_action_state,a_action_remark,id):
	result = False
	try:
		sql = 'update asset_zj_back set a_main_cd = \'{0}\',a_main_serial = \'{1}\', \
			a_action_loc = \'{2}\',a_action_state = \'{3}\',a_action_remark = \'{4}\' \
			where id = {5}'.format(a_main_cd,a_main_serial,a_action_loc,a_action_state,a_action_remark,id)
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		if cur.rowcount == 1:
			result = True
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return result
	