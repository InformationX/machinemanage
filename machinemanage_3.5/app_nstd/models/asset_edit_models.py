# -*- coding:utf-8 -*-
from django.db import connections,transaction
from config.models import common
import datetime

global MODEL
MODEL = 'asset_nstd'

def get_edit_base(a_cd):
	try:
		sql = 'select a_status,a_category,a_self_cd,a_type_cd,a_name,a_fuselage_cd,a_funds_type,a_supplier,a_project_cd, \
			a_price,a_currency,a_loc_cd,a_model,a_referendum,a_brand,a_amount,a_remark from asset_material where a_cd = \'{0}\''.format(a_cd)
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		row = cur.fetchone()
		if row:
			data = {
				'a_status':row[0],'a_category':row[1],'a_self_cd':row[2],'a_type_cd':row[3],
				'a_name':row[4],'a_fuselage_cd':row[5],'a_funds_type':row[6],'a_supplier':row[7],
				'a_project_cd':row[8],'a_price':row[9],'a_currency':row[10],'a_loc_cd':row[11],
				'a_model':row[12],'a_referendum':row[13],'a_brand':row[14],'a_amount':row[15],'a_remark':row[16]
			}
		else:
			data = {}
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

def edit_base(a_cd,a_status,a_category,a_self_cd,a_type_cd,a_name,a_fuselage_cd,a_funds_type,a_supplier,a_project_cd,a_price,a_currency,a_loc_cd,a_model,a_referendum,a_brand,a_amount,a_remark):
	result = False
	try:
		sql = 'update asset_material set a_status = \'{0}\',a_category=\'{1}\',a_self_cd=\'{2}\', \
			a_type_cd=\'{3}\',a_name=\'{4}\',a_fuselage_cd=\'{5}\',a_funds_type=\'{6}\',a_supplier=\'{7}\', \
			a_project_cd=\'{8}\',a_price=\'{9}\',a_currency=\'{10}\',a_loc_cd=\'{11}\',a_model=\'{12}\', \
			a_referendum=\'{13}\',a_brand=\'{14}\',a_amount=\'{15}\',a_remark=\'{16}\' where a_cd = \'{17}\' \
			'.format(a_status,a_category,a_self_cd,a_type_cd,a_name,a_fuselage_cd,a_funds_type,a_supplier,a_project_cd,a_price,a_currency,a_loc_cd,a_model,a_referendum,a_brand,a_amount,a_remark,a_cd)
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		if cur.rowcount == 1:
			result = True
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return result
	
def get_edit_out(a_cd):
	try:
		sql = 'select a_m.a_type_cd,a_m.a_name,a_a.a_action_depart,a_a.a_action_user,a_a.a_action_loc, \
			a_a.a_action_charge,a_a.a_action_model,a_a.a_action_state,a_a.a_action_category, \
			a_a.a_action_remark,a_a.a_action_type,a_m.a_action_id from asset_material a_m, \
			asset_action a_a where a_m.a_action_id = a_a.a_id and a_m.a_cd = \'{0}\''.format(a_cd)
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		row = cur.fetchone()
		if row:
			a_action_type = common.get_action_type(row[10])
			data = {
				'a_type_cd':row[0],'a_name':row[1],'a_action_depart':row[2],'a_action_user':row[3],
				'a_action_loc':row[4],'a_action_charge':row[5],'a_action_model':row[6],
				'a_action_state':row[7],'a_action_category':row[8],'a_action_remark':row[9],
				'a_action_type':a_action_type,'a_action_id':row[11]
			}
		else:
			data = {}
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

def edit_out(a_action_id,a_action_depart,a_action_user,a_action_loc,a_action_state,a_action_category,a_action_charge,a_action_model,a_action_remark):
	result = False
	try:
		sql = 'update asset_action set a_action_depart = \'{0}\',a_action_user=\'{1}\', \
			a_action_loc=\'{2}\', a_action_state = \'{3}\', a_action_category = \'{4}\' , \
			a_action_charge=\'{5}\',a_action_model=\'{6}\',a_action_remark=\'{7}\' where a_id = {8} \
			'.format(a_action_depart,a_action_user,a_action_loc,a_action_state,a_action_category,a_action_charge,a_action_model,a_action_remark,a_action_id)
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		if cur.rowcount == 1:
			result = True
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return result

def get_edit_back(a_cd):
	try:
		sql = 'select a_m.a_type_cd,a_m.a_name,a_a.a_action_user,a_a.a_action_loc,a_a.a_action_charge, \
			a_a.a_action_state,a_a.a_action_category,a_a.a_action_remark,a_a.a_action_type,a_a.a_id from asset_material a_m, \
			asset_action a_a where a_m.a_action_id = a_a.a_id and a_m.a_cd = \'{0}\''.format(a_cd)
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		row = cur.fetchone()
		if row:
			a_action_type = common.get_action_type(row[8])
			data = {
				'a_type_cd':row[0],'a_name':row[1],'a_action_user':row[2],'a_action_loc':row[3],
				'a_action_charge':row[4],'a_action_state':row[5],'a_action_category':row[6],
				'a_action_remark':row[7],'a_action_type':a_action_type,'a_action_id':row[9]
			}
		else:
			data = {}
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

def edit_back(a_action_id,a_action_user,a_action_loc,a_action_state,a_action_charge,a_action_category,a_action_remark):
	result = False
	try:
		sql = 'update asset_action set a_action_user = \'{0}\',a_action_loc = \'{1}\',a_action_state = \'{2}\', \
			a_action_charge = \'{3}\',a_action_category = \'{4}\',a_action_remark = \'{5}\' where a_id = {6} \
			'.format(a_action_user,a_action_loc,a_action_state,a_action_charge,a_action_category,a_action_remark,a_action_id)
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		if cur.rowcount == 1:
			result = True
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return result

def get_edit_zj(a_cd):
	try:
		sql = 'select a_m.a_name,a_a.a_action_charge,a_a.a_action_state,a_a.a_action_supplier, \
			a_a.a_action_type,a_a.a_id from asset_material a_m,asset_action a_a \
			where a_m.a_action_id = a_a.a_id and a_m.a_cd = \'{0}\' '.format(a_cd)
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		row = cur.fetchone()
		if row:
			a_action_type = common.get_action_type(row[4])
			data = {
				'a_name':row[0],'a_action_charge':row[1],'a_action_state':row[2],
				'a_action_supplier':row[3],'a_action_type':a_action_type,'a_action_id':row[5]
			}
			print(data)
		else:
			data = {}
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

def edit_zj(a_action_id,a_action_state,a_action_charge,a_action_supplier):
	result = False
	try:
		sql = 'update asset_action set a_action_state = \'{0}\',a_action_charge = \'{1}\',a_action_supplier = \'{2}\' \
			where a_id = {3}'.format(a_action_state,a_action_charge,a_action_supplier,a_action_id)
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		if cur.rowcount == 1:
			result = True
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return result

def get_edit_zj_back(a_cd):
	try:
		sql = 'select a_m.a_name,a_a.a_action_loc,a_a.a_action_state,a_a.a_action_category, \
			a_a.a_action_remark,a_a.a_action_type,a_a.a_id from asset_material a_m,asset_action a_a \
			where a_m.a_action_id = a_a.a_id and a_m.a_cd = \'{0}\''.format(a_cd)
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		row = cur.fetchone()
		if row:
			a_action_type = common.get_action_type(row[5])
			data = {
				'a_name':row[0],'a_action_loc':row[1],'a_action_state':row[2],'a_action_category':row[3],
				'a_action_remark':row[4],'a_action_type':a_action_type,'a_action_id':row[6]
			}
		else:
			data = {}
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

def edit_zj_back(a_action_id,a_action_loc,a_action_state,a_action_category,a_action_remark):
	result = False
	try:
		sql = 'update asset_action set a_action_loc = \'{0}\',a_action_state = \'{1}\', \
			a_action_category = \'{2}\', a_action_remark = \'{3}\' where a_id = {4} \
			'.format(a_action_loc,a_action_state,a_action_category,a_action_remark,a_action_id)
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		if cur.rowcount == 1:
			result = True
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return result
	
def get_edit_loan_back(a_cd):
	try:
		sql = 'select a_m.a_name,a_a.a_action_state,a_a.a_action_remark,a_a.a_action_type,a_a.a_id from \
			asset_material a_m,asset_action a_a where a_m.a_action_id = a_a.a_id and a_m.a_cd = \'{0}\''.format(a_cd)
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		row = cur.fetchone()
		if row:
			a_action_type = common.get_action_type(row[3])
			data = {
				'a_name':row[0],'a_action_state':row[1],'a_action_remark':row[2],
				'a_action_type':a_action_type,'a_action_id':row[4]
			}
		else:
			data = {}
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

def edit_loan_back(a_action_id,a_action_state,a_action_remark):
	result = False
	try:
		sql = 'update asset_action set a_action_state = \'{0}\',a_action_remark = \'{1}\' \
			where a_id = {2}'.format(a_action_state,a_action_remark,a_action_id)
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		if cur.rowcount == 1:
			result = True
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return result

def get_edit_storage_move(a_cd):
	try:
		sql = 'select a_m.a_name,a_a.a_action_loc,a_a.a_action_remark, \
			a_a.a_action_type,a_a.a_id from asset_material a_m,asset_action a_a \
			where a_m.a_action_id = a_a.a_id and a_m.a_cd = \'{0}\''.format(a_cd)

		cur = connections[MODEL].cursor()
		cur.execute(sql)
		row = cur.fetchone()
		if row:
			a_action_type = common.get_action_type(row[3])
			data = {
				'a_name':row[0],'a_action_loc':row[1],'a_action_remark':row[2],
				'a_action_type':a_action_type,'a_action_id':row[4]
			}
		else:
			data = {}
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

def edit_storage_move(a_action_id,a_action_loc,a_action_remark):
	result = False
	try:
		sql = 'update asset_action set a_action_loc = \'{0}\',a_action_remark = \'{1}\' \
			where a_id = {2}'.format(a_action_loc,a_action_remark,a_action_id)
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		if cur.rowcount == 1:
			result = True
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return result
	
def get_edit_online_move(a_cd):
	try:
		sql = 'select a_m.a_type_cd,a_m.a_name,a_a.a_action_depart,a_a.a_action_loc,a_a.a_action_user,a_a.a_action_charge, \
			a_a.a_action_model,a_a.a_action_remark,a_a.a_action_type,a_a.a_id from asset_material a_m, \
			asset_action a_a where a_m.a_action_id = a_a.a_id and a_m.a_cd = \'{0}\''.format(a_cd)
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		row = cur.fetchone()
		if row:
			a_action_type = common.get_action_type(row[8])
			data = {
				'a_type_cd':row[0],'a_name':row[1],'a_action_depart':row[2],'a_action_loc':row[3],
				'a_action_user':row[4],'a_action_charge':row[5],'a_action_model':row[6],
				'a_action_remark':row[7],'a_action_type':a_action_type,'a_action_id':row[9]
			}
		else:
			data = {}
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

def edit_online_move(a_action_id,a_action_depart,a_action_loc,a_action_user,a_action_charge,a_action_model,a_action_remark):
	result = False
	try:
		sql = 'update asset_action set a_action_depart = \'{0}\',a_action_loc = \'{1}\',a_action_user = \'{2}\', \
			a_action_charge = \'{3}\', a_action_model = \'{4}\',a_action_remark = \'{5}\' where a_id = {6} \
			'.format(a_action_depart,a_action_loc,a_action_user,a_action_charge,a_action_model,a_action_remark,a_action_id)
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		if cur.rowcount == 1:
			result = True
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return result

def get_edit_loc(a_cd):
	try:
		sql1 = 'select a_m.a_name,a_a.a_action_loc,a_a.a_id,a_m.a_id from asset_material a_m, \
			asset_action a_a where a_m.a_action_id = a_a.a_id and a_m.a_cd = \'{0}\''.format(a_cd)
		sql2 = 'select a_name,a_loc_cd,0,a_id from asset_material where a_cd = \'{0}\' and a_action_id = 0'.format(a_cd)
		sql = '{0} union all {1}'.format(sql1,sql2)
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		row = cur.fetchone()
		print(row)
		if row:
			data = {'a_name':row[0], 'a_action_loc':row[1], 'a_action_id':row[2], 'a_material_id':row[3]}
		else:
			data = {}
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

def edit_loc(a_cd,a_material_id,a_action_id,a_origin_loc,a_action_loc,a_opr_user,a_record_time,a_action_type):
	result = False
	try:
		with transaction.atomic(using=MODEL):
			'''
			sql = 'select a_action_supplier,a_origin_state,a_action_state,a_action_remark,a_action_depart, \
				a_action_user,a_action_model,a_action_charge,a_origin_depart,a_action_category,a_origin_cd \
				from asset_action where a_id = {0}'.format(a_action_id)
			cur = connections[MODEL].cursor()
			cur.execute(sql)
			row = cur.fetchone()
			if row:
				sql = 'insert into asset_action(a_action_supplier,a_origin_state,a_action_state,a_action_remark, \
					a_action_depart,a_action_user,a_action_model,a_action_charge,a_origin_depart,a_action_category, \
					a_origin_cd,a_cd,a_origin_loc,a_action_loc,a_opr_user,a_record_time,a_material_id,a_action_type) values \
					(\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\',\'{8}\',\'{9}\',\'{10}\',\'{11}\',\'{12}\',\'{13}\',\'{14}\',\'{15}\',{16},{17}) returning a_id \
					'.format(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],a_cd,a_origin_loc,a_action_loc,a_opr_user,a_record_time,a_material_id,a_action_type)
				cur.execute(sql)
				row = cur.fetchone()
				if row:
					a_id = row[0]
					sql = 'update asset_material set a_action_id = {0} where a_cd = \'{1}\''.format(a_id,a_cd)
					cur.execute(sql)
					if cur.rowcount == 1:
						result = True
			'''

			sql = 'insert into asset_operation(a_material_id,a_cd,a_origin_loc,a_action_loc,a_opr_user,a_record_time,a_action_type) \
				values({0},\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',{6})'.format(a_material_id,a_cd,a_origin_loc,a_action_loc,a_opr_user,a_record_time,a_action_type)
			cur = connections[MODEL].cursor()
			cur.execute(sql)
			if cur.rowcount == 1:
				if int(a_action_id) != 0:
					sql = 'update asset_action set a_action_loc = \'{0}\' where a_id = {1}'.format(a_action_loc,a_action_id)
				else:
					sql = 'update asset_material set a_loc_cd = \'{0}\' where a_id = {1}'.format(a_action_loc,a_material_id)
				cur.execute(sql)
				if cur.rowcount == 1:
					result = True

	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return result

def get_edit_state(a_cd):
	try:
		sql1 = 'select a_m.a_name,a_a.a_action_state,a_a.a_id,a_m.a_id from asset_material a_m, \
			asset_action a_a where a_m.a_action_id = a_a.a_id and a_m.a_cd = \'{0}\''.format(a_cd)
		sql2 = 'select a_name,a_status,0,a_id from asset_material where a_cd = \'{0}\' and a_action_id = 0'.format(a_cd)
		sql = '{0} union all {1}'.format(sql1,sql2)
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		row = cur.fetchone()
		if row:
			data = {'a_name':row[0],'a_action_state':row[1],'a_action_id':row[2],'a_material_id':row[3]}
		else:
			data = {}
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

def edit_state(a_cd,a_material_id,a_action_id,a_origin_state,a_action_state,a_opr_user,a_record_time,a_action_type):
	try:
		with transaction.atomic(using=MODEL):
			'''
			sql = 'select a_action_supplier,a_origin_loc,a_action_loc,a_action_remark,a_action_depart, \
				a_action_user,a_action_model,a_action_charge,a_origin_depart,a_action_category,a_origin_cd \
				from asset_action where a_id = {0}'.format(a_action_id)
			cur = connections[MODEL].cursor()
			cur.execute(sql)
			row = cur.fetchone()
			if row:
				sql = 'insert into asset_action(a_action_supplier,a_origin_loc,a_action_loc,a_action_remark, \
					a_action_depart,a_action_user,a_action_model,a_action_charge,a_origin_depart,a_action_category, \
					a_origin_cd,a_cd,a_origin_state,a_action_state,a_opr_user,a_record_time,a_material_id,a_action_type) values \
					(\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\',\'{8}\',\'{9}\',\'{10}\',\'{11}\',\'{12}\',\'{13}\',\'{14}\',\'{15}\',{16},{17}) returning a_id \
					'.format(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],a_cd,a_origin_state,a_action_state,a_opr_user,a_record_time,a_material_id,a_action_type)
				cur.execute(sql)
				row = cur.fetchone()
				if row:
					a_id = row[0]
					sql = 'update asset_material set a_action_id = {0} where a_cd = \'{1}\''.format(a_id,a_cd)
					cur.execute(sql)
					if cur.rowcount == 1:
						result = True
			'''
			sql = 'insert into asset_operation(a_material_id,a_cd,a_origin_state,a_action_state,a_opr_user,a_record_time,a_action_type) \
				values({0},\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',{6})'.format(a_material_id,a_cd,a_origin_state,a_action_state,a_opr_user,a_record_time,a_action_type)
			cur = connections[MODEL].cursor()
			cur.execute(sql)
			if cur.rowcount == 1:
				if int(a_action_id) != 0:
					sql = 'update asset_action set a_action_state = \'{0}\' where a_id = {1}'.format(a_action_state,a_action_id)
				else:
					sql = 'update asset_material set a_status = \'{0}\' where a_id = {1}'.format(a_action_state,a_material_id)
				cur.execute(sql)
				if cur.rowcount == 1:
					result = True
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return result

def get_edit_category(a_cd):
	try:
		sql = 'select a_m.a_name,a_a.a_action_category,a_a.a_id,a_m.a_id from asset_material a_m, \
			asset_action a_a where a_m.a_action_id = a_a.a_id and a_m.a_cd = \'{0}\''.format(a_cd)
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		row = cur.fetchone()
		if row:
			data = {'a_name':row[0],'a_action_category':row[1],'a_action_id':row[2],'a_material_id':row[3]}
		else:
			data = {}
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

def edit_category(a_cd,a_material_id,a_action_id,a_origin_category,a_action_category,a_opr_user,a_record_time,a_action_type):
	try:
		with transaction.atomic(using=MODEL):
			sql = 'select a_action_supplier,a_origin_loc,a_action_loc,a_action_remark,a_action_depart, \
				a_action_user,a_action_model,a_action_charge,a_origin_depart,a_action_state,a_origin_cd \
				from asset_action where a_id = {0}'.format(a_action_id)
			cur = connections[MODEL].cursor()
			cur.execute(sql)
			row = cur.fetchone()
			if row:
				sql = 'insert into asset_action(a_action_supplier,a_origin_loc,a_action_loc,a_action_remark,a_action_depart, \
					a_action_user,a_action_model,a_action_charge,a_origin_depart,a_action_state,a_origin_cd,a_cd, \
					a_origin_category,a_action_category,a_opr_user,a_record_time,a_material_id,a_action_type) values \
					(\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\',\'{8}\',\'{9}\',\'{10}\',\'{11}\',\'{12}\',\'{13}\',\'{14}\',\'{15}\',{16},{17}) returning a_id \
					'.format(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],a_cd,a_origin_category,a_action_category,a_opr_user,a_record_time,a_material_id,a_action_type)
				cur.execute(sql)
				row = cur.fetchone()
				if row:
					a_id = row[0]
					sql = 'update asset_material set a_action_id = {0} where a_cd = \'{1}\''.format(a_id,a_cd)
					cur.execute(sql)
					if cur.rowcount == 1:
						result = True
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return result

def get_edit_depart(a_cd):
	try:
		sql1 = 'select a_m.a_name,a_a.a_action_depart,a_a.a_id,a_m.a_id from asset_material a_m, \
			asset_action a_a where a_m.a_action_id = a_a.a_id and a_m.a_cd = \'{0}\''.format(a_cd)
		sql2 = 'select a_name,a_depart,0,a_id from asset_material where a_cd = \'{0}\' and a_action_id = 0'.format(a_cd)
		sql = '{0} union all {1}'.format(sql1,sql2)

		cur = connections[MODEL].cursor()
		cur.execute(sql)
		row = cur.fetchone()
		if row:
			data = {'a_name':row[0],'a_origin_depart':row[1],'a_action_id':row[2],'a_material_id':row[3]}
		else:
			data = {}
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	return data

def edit_depart(a_cd,a_material_id,a_action_id,a_origin_depart,a_action_depart,a_opr_user,a_record_time,a_action_type):
	try:
		with transaction.atomic(using=MODEL):
			sql = 'insert into asset_operation(a_material_id,a_cd,a_origin_depart,a_action_depart,a_opr_user,a_record_time,a_action_type) \
				values({0},\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',{6})'.format(a_material_id,a_cd,a_origin_depart,a_action_depart,a_opr_user,a_record_time,a_action_type)
			cur = connections[MODEL].cursor()
			cur.execute(sql)
			if cur.rowcount == 1:
				if int(a_action_id) != 0:
					sql = 'update asset_action set a_action_depart = \'{0}\' where a_id = {1}'.format(a_action_depart,a_action_id)
				else:
					sql = 'update asset_material set a_depart = \'{0}\' where a_id = {1}'.format(a_action_depart,a_material_id)
				cur.execute(sql)
				if cur.rowcount == 1:
					result = True
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return result