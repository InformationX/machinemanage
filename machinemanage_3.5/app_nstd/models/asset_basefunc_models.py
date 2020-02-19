# -*- coding:utf-8 -*-
from django.db import connections,transaction
import datetime
from config.models import common

global MODEL
MODEL = 'asset_nstd'

def asset_add(a_cd,a_self_cd,a_name,a_type_cd,a_fuselage_cd,a_amount,a_price,a_currency,
		a_out_time,a_purchase_time,a_funds_type,a_project_cd,a_depart,a_budget,a_model,
		a_po_cd,a_brand,a_supplier,a_sap_cd,a_status,a_category,a_referendum,a_loc_cd,
		a_need_cal,a_b_nstd,a_remark,a_user_id,a_record_time):
	sql = 'insert into asset_material(a_cd,a_self_cd,a_name,a_type_cd,a_fuselage_cd,a_amount,a_price, \
		a_currency,a_out_time,a_purchase_time,a_funds_type,a_project_cd,a_depart,a_budget,a_model, \
		a_po_cd,a_brand,a_supplier,a_sap_cd,a_status,a_category,a_referendum,a_loc_cd,a_need_cal, \
		a_b_nstd,a_remark,a_user_id,a_record_time) values ( \
		\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\',\'{8}\',\'{9}\',\'{10}\', \
		\'{11}\',\'{12}\',\'{13}\',\'{14}\',\'{15}\',\'{16}\',\'{17}\',\'{18}\',\'{19}\',\'{20}\', \
		\'{21}\',\'{22}\',\'{23}\',\'{24}\',\'{25}\',\'{26}\',\'{27}\') \
		'.format(a_cd,a_self_cd,a_name,a_type_cd,a_fuselage_cd,a_amount,a_price,a_currency,a_out_time,
		a_purchase_time,a_funds_type,a_project_cd,a_depart,a_budget,a_model,a_po_cd,a_brand,a_supplier,
		a_sap_cd,a_status,a_category,a_referendum,a_loc_cd,a_need_cal,a_b_nstd,a_remark,a_user_id,a_record_time)
	data = {'result':False}
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		if cur.rowcount == 1:
			data['result'] = True
	except Exception as e:
		print(str(e))
		if('already exists' in str(e)):
			data['msg'] = '机身号重复，录入失败!'
	finally:
		connections[MODEL].close()
	return data

#支给设备 -> 根据资产编号搜索详情
def before_zj_detail(a_cd):
	sql = 'select a_id,a_action_id from asset_material where a_cd = \'{0}\''.format(a_cd)
	data = {'result':False}
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		row = cur.fetchone()
		if row:
			a_material_id,a_action_id = row
			if a_action_id == 0:
				sql = 'select a_self_cd,a_name,a_type_cd,a_fuselage_cd,a_amount,a_price \
				,a_currency,a_project_cd,a_out_time,a_purchase_time,a_brand,a_model,a_category \
				,a_loc_cd,a_status,a_budget,a_referendum,a_po_cd,a_sap_cd,a_depart,a_action_id \
				from asset_material where a_cd = \'{0}\''.format(a_cd)
			else:
				sql = 'select a_m.a_self_cd,a_m.a_name,a_m.a_type_cd,a_m.a_fuselage_cd,a_m.a_amount, \
					a_m.a_price,a_m.a_currency,a_m.a_project_cd,a_m.a_out_time,a_m.a_purchase_time, \
					a_m.a_brand,a_model,a_m.a_category,a_a.a_action_loc,a_a.a_action_state,a_m.a_budget,\
					a_m.a_referendum,a_m.a_po_cd,a_m.a_sap_cd,a_m.a_depart,a_a.a_action_type from asset_material a_m, \
					asset_action a_a where a_m.a_action_id = a_a.a_id and a_a.a_action_type not in(3,6,7) \
					and a_m.a_cd = \'{0}\''.format(a_cd)
			cur.execute(sql)
			row = cur.fetchone()
			if row:
				a_action_type = common.get_action_type(row[20])
				data = {
					'a_self_cd':row[0],'a_name':row[1],'a_type_cd':row[2],'a_fuselage_cd':row[3],
					'a_amount':row[4],'a_price':row[5],'a_currency':row[6],'a_project_cd':row[7],
					'a_out_time':str(row[8])[0:10],'a_purchase_time':str(row[9]),'a_brand':row[10],
					'a_model':row[11],'a_category':row[12],'a_loc_cd':row[13],'a_status':row[14],
					'a_budget':row[15],'a_referendum':row[16],'a_po_cd':row[17],'a_sap_cd':row[18],
					'a_depart':row[19],'a_material_id':a_material_id,'a_action_type':a_action_type,'result':True
				}
			else:
				data['msg'] = '未搜索到数据'
		else:
			data['msg'] = '未搜索到数据'
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	return data

#支给归还 -> 根据资产编号搜索详情
def get_zj_detail(a_cd):
	sql = 'select a_m.a_self_cd,a_m.a_name,a_m.a_category,a_m.a_type_cd,a_m.a_fuselage_cd,a_m.a_amount, \
		a_m.a_price,a_m.a_currency,a_m.a_brand,a_m.a_out_time,a_m.a_purchase_time,a_m.a_project_cd, \
		a_a.a_action_state,a_a.a_action_supplier,a_m.a_depart,a_m.a_model,a_m.a_budget,a_m.a_referendum,\
		a_m.a_po_cd,a_m.a_sap_cd,a_a.a_action_type from asset_material a_m,asset_action a_a where \
		a_m.a_action_id = a_a.a_id and a_m.a_cd = \'{0}\' and a_a.a_action_type = 1'.format(a_cd)
	data = {'result':False}
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		row = cur.fetchone()
		if row:
			a_action_type = common.get_action_type(row[20])
			data = {
				'a_self_cd':row[0],'a_name':row[1],'a_category':row[2],'a_type_cd':row[3],'a_fuselage_cd':row[4],
				'a_amount':row[5],'a_price':row[6],'a_currency':row[7],'a_brand':row[8],'a_out_time':str(row[9]),
				'a_purchase_time':str(row[10]),'a_project_cd':row[11],'a_zj_state':row[12],'a_action_supplier':row[13],
				'a_depart':row[14],'a_model':row[15],'a_budget':row[16],'a_referendum':row[17],'a_po_cd':row[18],
				'a_sap_cd':row[19],'a_action_type':a_action_type,'result':True
			}
		else:
			data['msg'] = '未搜索到支给信息'
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	return data

#验证资产状态
def before_action_vde(a_material_id):
	sql = 'select a_a.a_action_type from asset_material a_m,asset_action a_a where \
		a_m.a_action_id = a_a.a_id and a_m.a_id = \'{0}\''.format(a_material_id)
	data = {'result':False}
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		row = cur.fetchone()
		if row:
			a_action_type = row[0]
			if a_action_type == 1:
				data['msg'] = '该资产已支给'
			elif a_action_type == 3:
				data['msg'] = '该资产已归还供应商'
			elif a_action_type == 5 or a_action_type == 8:
				data['msg'] = '该资产已出库'
			elif a_action_type == 6:
				data['msg'] = '该资产已销售'
			elif a_action_type == 7:
				data['msg'] = '该资产已报废'
			else:
				data['result'] = True
		else:
			data['result'] = True
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

#确认支给
def action_zj(a_cd,a_action_type,a_record_time,a_action_supplier,a_opr_user,a_material_id,a_action_loc,a_action_state):
	sql = 'insert into asset_action(a_action_type,a_record_time,a_action_supplier,\
		a_opr_user,a_material_id,a_action_loc,a_action_state,a_cd) \
		values(\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\') \
		'.format(a_action_type,a_record_time,a_action_supplier,a_opr_user,a_material_id,a_action_loc,a_action_state,a_cd)
	result = False
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		if cur.rowcount == 1:
			sql2 = 'select a_id from asset_action where a_material_id = \'{0}\' and a_action_type = \'{1}\' \
				and a_record_time = \'{2}\''.format(a_material_id,a_action_type,a_record_time)
			cur.execute(sql2)
			row = cur.fetchone()
			if row:
				a_id = row[0]
				sql3 = 'update asset_material set a_action_id = \'{0}\' where a_id = \'{1}\''.format(a_id,a_material_id)
				cur.execute(sql3)
				if cur.rowcount == 1:
					result = True
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	return result

#支给归还
def revert_zj(a_cd,a_action_loc,a_fuselage_cd,a_action_state,a_action_remark,a_opr_user,a_record_time,a_action_type):
	sql = 'insert into asset_action(a_cd,a_action_loc,a_fuselage_cd,a_action_state,a_action_remark,a_opr_user, \
		a_record_time,a_action_type) values(\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\') \
		'.format(a_cd,a_action_loc,a_fuselage_cd,a_action_state,a_action_remark,a_opr_user,a_record_time,a_action_type)
	result = False
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		if cur.rowcount == 1:
			sql2 = 'select a_id from asset_action where a_fuselage_cd = \'{0}\' and a_record_time = \'{1}\' \
				and a_action_type = \'{2}\''.format(a_fuselage_cd,a_record_time,a_action_type)
			cur.execute(sql2)
			row = cur.fetchone()
			if row:
				a_id = row[0]
				sql3 = 'update asset_material set a_action_id = \'{0}\' where a_fuselage_cd = \'{1}\''.format(a_id,a_fuselage_cd)
				cur.execute(sql3)
				if cur.rowcount == 1:
					result = True
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	return result

#设备出库前根据资产番号搜索详情
def get_out_detail(a_cd):
	data = {'result':False}
	try:
		sql1 = 'select a_action_id from asset_material where a_cd = \'{0}\''.format(a_cd)
		cur = connections[MODEL].cursor()
		cur.execute(sql1)
		row = cur.fetchone()
		if row:
			a_action_id = row[0]
			if a_action_id == 0:
				sql2 = 'select a_id,a_self_cd,a_name,a_type_cd,a_fuselage_cd,a_amount,a_price, \
					a_currency,a_project_cd,a_purchase_time,a_supplier,a_depart,a_category, \
					a_model,a_loc_cd,a_status,a_action_id from asset_material \
				 	where a_cd = \'{0}\''.format(a_cd)
			else:
				sql2 = 'select a_m.a_id,a_m.a_self_cd,a_m.a_name,a_m.a_type_cd,a_m.a_fuselage_cd, \
					a_m.a_amount,a_m.a_price, a_m.a_currency,a_m.a_project_cd,a_m.a_purchase_time, \
					a_m.a_supplier,a_a.a_action_depart,a_a.a_action_category,a_a.a_action_model, \
					a_a.a_action_loc,a_a.a_action_state,a_a.a_action_type from asset_material a_m, \
					asset_action a_a where a_m.a_action_id = a_a.a_id and a_a.a_action_type not in (3,6,7) \
					and a_m.a_cd = \'{0}\''.format(a_cd)
			cur.execute(sql2)
			row = cur.fetchone()
			if row:
				data = {
					'a_material_id':row[0],'a_self_cd':row[1],'a_name':row[2],'a_type_cd':row[3],
					'a_fuselage_cd':row[4],'a_amount':row[5],'a_price':row[6],'a_currency':row[7],
					'a_project_cd':row[8],'a_purchase_time':str(row[9]),'a_supplier':row[10],
					'a_action_depart':row[11],'a_action_category':row[12],'a_action_model':row[13],
					'a_action_loc':row[14],'a_action_state':row[15],'a_action_id':a_action_id,'result':True
				}
				a_action_type = row[16]
				data['a_action_type'] = common.get_action_type(a_action_type)
			else:
				data['msg'] = '未搜索到数据!'		#已归还供应商、销售、报废
		else:
			data['msg'] = '未搜索到数据!'
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	return data

#设备退库前根据资产番号搜索详情
def get_back_detail(a_cd):
	data = {'result':False}
	try:
		sql1 = 'select a_action_id from asset_material where a_cd = \'{0}\''.format(a_cd)
		cur = connections[MODEL].cursor()
		cur.execute(sql1)
		row = cur.fetchone()
		if row:
			a_action_id = row[0]
			sql2 = 'select a_m.a_id,a_m.a_self_cd,a_m.a_name,a_m.a_type_cd,a_m.a_fuselage_cd, \
				a_m.a_amount,a_m.a_price, a_m.a_currency,a_m.a_project_cd,a_m.a_purchase_time, \
				a_m.a_supplier,a_a.a_action_depart,a_a.a_action_category,a_a.a_action_model, \
				a_a.a_action_loc,a_a.a_action_state,a_a.a_action_type from asset_material a_m, \
				asset_action a_a where a_m.a_action_id = a_a.a_id and a_m.a_cd = \'{0}\''.format(a_cd)
			cur.execute(sql2)
			row = cur.fetchone()
			if row:
				data = {
					'a_material_id':row[0],'a_self_cd':row[1],'a_name':row[2],'a_type_cd':row[3],
					'a_fuselage_cd':row[4],'a_amount':row[5],'a_price':row[6],'a_currency':row[7],
					'a_project_cd':row[8],'a_purchase_time':str(row[9]),'a_supplier':row[10],
					'a_action_depart':row[11],'a_action_category':row[12],'a_action_model':row[13],
					'a_action_loc':row[14],'a_action_state':row[15],'a_action_id':a_action_id,'result':True
				}
				a_action_type = row[16]
				data['a_action_type'] = common.get_action_type(a_action_type)
			else:
				data['msg'] = '未搜索到数据!'		#已归还供应商、销售、报废
		else:
			data['msg'] = '未搜索到数据!'
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	return data

#设备出库前验证
def before_out_vde(a_material_id):
	sql = 'select a_a.a_action_type from asset_material a_m,asset_action a_a where \
		a_m.a_action_id = a_a.a_id and a_m.a_id = \'{0}\''.format(a_material_id)
	data = {'result':False}
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		row = cur.fetchone()
		if row:
			data['msg'] = common.get_action_type(row[0])
			if data['msg'] == '在库':
				data['result'] = True
		else:
			data['result'] = True
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	return data

#设备出库
def asset_out(a_material_id,a_record_time,a_action_depart,a_action_user,a_action_charge,
		a_action_loc,a_action_state,a_action_remark,a_action_type,a_opr_user,a_action_model):
	sql = 'insert into asset_action(a_material_id,a_record_time,a_action_depart,a_action_user, \
		a_action_charge,a_action_loc,a_action_state,a_action_remark,a_action_type,a_opr_user,a_action_model) \
		values(\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\',\'{8}\',\'{9}\',\'{10}\') \
		'.format(a_material_id,a_record_time,a_action_depart,a_action_user,a_action_charge,
			a_action_loc,a_action_state,a_action_remark,a_action_type,a_opr_user,a_action_model)
	result = False
	try:
		with transaction.atomic(using="asset_nstd"):
			cur = connections[MODEL].cursor()
			cur.execute(sql)
			if cur.rowcount == 1:
				sql2 = 'select a_id from asset_action where a_material_id = \'{0}\' and a_action_type = {1} \
					and a_record_time = \'{2}\''.format(a_material_id,a_action_type,a_record_time)
				cur.execute(sql2)
				row = cur.fetchone()
				if row:
					a_id = row[0]
					sql3 = 'update asset_material set a_action_id = \'{0}\' where a_id = \'{1}\''.format(a_id,a_material_id)
					cur.execute(sql3)
					if cur.rowcount == 1:
						result = True
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].cursor()
	return result

#资产退库前验证
def before_back_vde(a_material_id):
	sql = 'select a_a.a_action_type from asset_material a_m,asset_action a_a where \
		a_m.a_action_id = a_a.a_id and a_m.a_id = \'{0}\''.format(a_material_id)

	data = {'result':False}
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		row = cur.fetchone()
		if row:
			a_action_type = row[0]
			if a_action_type == 1:
				data['msg'] = '该设备已支给'
			elif a_action_type == 2 or a_action_type == 9:
				data['msg'] = '该设备已在库'
			elif a_action_type == 3:
				data['msg'] = '该设备已归还供应商'
			elif a_action_type == 4:
				data['msg'] = '该设备已退库'
			elif a_action_type == 6:
				data['msg'] = '该设备已销售'
			elif a_action_type == 7:
				data['msg'] = '该设备已报废'
			elif a_action_type == 10:
				data['msg'] = '该资产已送检'
			else:
				data['result'] = True
		else:
			data['result'] = True
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	return data

#资产退库
def asset_back(a_cd,a_material_id,a_action_user,a_action_state,a_action_charge,a_action_loc,
		a_action_remark,a_action_type,a_record_time,a_opr_user,a_action_category):
	sql = 'insert into asset_action(a_action_type,a_material_id,a_action_user,a_action_state, \
		a_action_charge,a_action_loc,a_action_remark,a_action_category,a_record_time,a_opr_user,a_cd) \
		values(\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\',\'{8}\',\'{9}\',\'{10}\') \
		'.format(a_action_type,a_material_id,a_action_user,a_action_state,a_action_charge,
			a_action_loc,a_action_remark,a_action_category,a_record_time,a_opr_user,a_cd)
	result = False
	try:
		with transaction.atomic(using=MODEL):
			cur = connections[MODEL].cursor()
			cur.execute(sql)
			rowcount = cur.rowcount
			if rowcount == 1:
				sql2 = 'select a_id from asset_action where a_material_id = \'{0}\' and a_record_time = \'{1}\' \
					and a_action_type = \'{2}\''.format(a_material_id,a_record_time,a_action_type)
				cur.execute(sql2)
				row = cur.fetchone()
				if row:
					a_id = row[0]
					sql3 = 'update asset_material set a_action_id = \'{0}\' where a_id = \'{1}\''.format(a_id,a_material_id)
					cur.execute(sql3)
					if cur.rowcount == 1:
						result = True
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	return result

#借用设备归还前查询
def loan_revert_detail(a_cd):
	sql = 'select a_action_id,a_id,a_fuselage_cd from asset_material where a_cd = \'{0}\''.format(a_cd)
	data = {'result':False}
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		row = cur.fetchone()
		if row:
			a_action_id,a_material_id,a_fuselage_cd = row
			if a_action_id == 0:
				sql2 = 'select a_self_cd,a_name,a_type_cd,a_status,a_loc_cd,a_out_time,a_purchase_time, \
					a_project_cd,a_supplier,a_category,a_depart,a_model,a_amount,a_price,a_currency, \
					a_funds_type,a_budget,a_referendum,a_po_cd,a_sap_cd,a_action_id from asset_material \
					where a_id = \'{0}\''.format(a_material_id)
			else:
				sql2 = 'select a_m.a_self_cd,a_m.a_name,a_m.a_type_cd,a_a.a_action_state,a_a.a_action_loc, \
					a_m.a_out_time,a_m.a_purchase_time,a_m.a_project_cd,a_m.a_supplier,a_m.a_category, \
					a_m.a_depart,a_m.a_model,a_m.a_amount,a_m.a_price,a_m.a_currency,a_m.a_funds_type, \
					a_m.a_budget,a_m.a_referendum,a_m.a_po_cd,a_m.a_sap_cd,a_a.a_action_type \
					from asset_material a_m,asset_action a_a where a_m.a_action_id = a_a.a_id \
					and a_a.a_action_type not in(3,6,7) and a_m.a_id = \'{0}\''.format(a_material_id)
			cur.execute(sql2)
			row = cur.fetchone()
			if row:
				a_action_type = common.get_action_type(row[20])
				data = {
					'a_self_cd':row[0],'a_name':row[1],'a_type_cd':row[2],'a_action_state':row[3],
					'a_action_loc':row[4],'a_out_time':str(row[5])[0:10],'a_purchase_time':str(row[6]),
					'a_project_cd':row[7],'a_supplier':row[8],'a_category':row[9],'a_depart':row[10],
					'a_model':row[11],'a_amount':row[12],'a_price':row[13],'a_currency':row[14],
					'a_funds_type':row[15],'a_budget':row[16],'a_referendum':row[17],'a_po_cd':row[18],
					'a_sap_cd':row[19],'a_action_type':a_action_type,'a_material_id':a_material_id,
					'a_fuselage_cd':a_fuselage_cd,'result':True
				}
				data['result'] = True
			else:
				data['msg'] = '未搜索到数据!'
		else:
			data['msg'] = '未搜索到数据!'
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	return data

#借用设备归还
def loan_revert(a_cd,a_action_state,a_material_id,a_action_type,a_record_time,a_opr_user):
	result = False
	try:
		with transaction.atomic(using="asset_nstd"):
			cur = connections[MODEL].cursor()
			sql = 'insert into asset_action(a_cd,a_action_state,a_material_id,a_action_type,a_record_time,a_opr_user) \
				values(\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\') \
				'.format(a_cd,a_action_state,a_material_id,a_action_type,a_record_time,a_opr_user)
			cur.execute(sql)
			if cur.rowcount == 1:
				sql2 = 'select a_id from asset_action where a_material_id = \'{0}\' and a_record_time = \'{1}\' \
					and a_action_type = \'{2}\''.format(a_material_id,a_record_time,a_action_type)
				cur.execute(sql2)
				row = cur.fetchone()
				if row:
					a_id = row[0]
					sql3 = 'update asset_material set a_action_id = \'{0}\' \
						where a_id = \'{1}\''.format(a_id,a_material_id)
					cur.execute(sql3)
					if cur.rowcount == 1:
						result = True
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	return result

def get_sale_detail(a_cd):
	sql = 'select a_action_id,a_fuselage_cd,a_id from asset_material where a_cd = \'{0}\''.format(a_cd)
	data = {'result':False}
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		row = cur.fetchone()
		if row:
			a_action_id,a_fuselage_cd,a_material_id = row
			if a_action_id == 0:
				sql2 = 'select a_self_cd,a_name,a_type_cd,a_amount,a_price,a_currency,a_project_cd, \
					a_out_time,a_purchase_time,a_supplier,a_brand,a_model,a_loc_cd,a_status,a_action_id \
					from asset_material where a_cd = \'{0}\''.format(a_cd)
			else:
				sql2 = 'select a_m.a_self_cd,a_m.a_name,a_m.a_type_cd,a_m.a_amount,a_m.a_price, \
					a_m.a_currency,a_m.a_project_cd,a_m.a_out_time,a_m.a_purchase_time,a_m.a_supplier, \
					a_m.a_brand,a_m.a_model,a_a.a_action_loc,a_a.a_action_state,a_a.a_action_type \
					from asset_material a_m,asset_action a_a where a_m.a_action_id = a_a.a_id \
					and a_a.a_action_type not in(3,6,7) and a_m.a_cd = \'{0}\''.format(a_cd)
			cur.execute(sql2)
			row = cur.fetchone()
			if row:
				a_action_type = common.get_action_type(row[14])
				data = {
					'a_self_cd':row[0],'a_name':row[1],'a_type_cd':row[2],'a_amount':row[3],
					'a_price':row[4],'a_currency':row[5],'a_project_cd':row[6],'a_out_time':str(row[7])[0:10],
					'a_purchase_time':str(row[8]),'a_supplier':row[9],'a_brand':row[10],'a_model':row[11],
					'a_cur_pos':row[12],'a_cur_state':row[13],'a_action_type':a_action_type,
					'a_fuselage_cd':a_fuselage_cd,'a_material_id':a_material_id,'result':True
				}
			else:
				data['msg'] = '未搜索到数据!'
		else:
			data['msg'] = '未搜索到数据!'
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	return data

#设备销售记账
def asset_sale(a_cd,a_action_supplier,a_material_id,a_action_remark,a_record_time,a_action_type,a_opr_user):
	sql = 'insert into asset_action(a_action_supplier,a_material_id,a_action_remark,a_record_time, \
		a_action_type,a_opr_user,a_cd) values(\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\') \
		'.format(a_action_supplier,a_material_id,a_action_remark,a_record_time,a_action_type,a_opr_user,a_cd)
	result = False	
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		if cur.rowcount == 1:
			sql2 = 'select a_id from asset_action where a_material_id = \'{0}\' and a_record_time = \'{1}\' \
				and a_action_type = \'{2}\''.format(a_material_id,a_record_time,a_action_type)
			cur.execute(sql2)
			row = cur.fetchone()
			if row:
				a_id = row[0]
				sql3 = 'update asset_material set a_action_id = \'{0}\' where a_id = \'{1}\''.format(a_id,a_material_id)
				cur.execute(sql3)
				if cur.rowcount == 1:
					result = True
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return result

#设备报废记账
def asset_scrap(a_cd,a_material_id,a_action_remark,a_record_time,a_action_type,a_opr_user):
	sql = 'insert into asset_action(a_cd,a_material_id,a_action_remark,a_record_time, \
		a_action_type,a_opr_user) values(\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\') \
		'.format(a_cd,a_material_id,a_action_remark,a_record_time,a_action_type,a_opr_user)
	result = False
	try:
		with transaction.atomic(using="asset_nstd"):
			cur = connections[MODEL].cursor()
			cur.execute(sql)
			if cur.rowcount == 1:
				sql2 = 'select a_id from asset_action where a_material_id = \'{0}\' and a_record_time = \'{1}\' \
					and a_action_type = \'{2}\''.format(a_material_id,a_record_time,a_action_type)
				cur.execute(sql2)
				row = cur.fetchone()
				if row:
					a_id = row[0]
					sql3 = 'update asset_material set a_action_id = \'{0}\' \
						where a_id = \'{1}\''.format(a_id,a_material_id)
					cur.execute(sql3)
					if cur.rowcount == 1:
						result = True
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	return result

#设备移动记账
def asset_move_detail(a_cd):
	sql = 'select a_action_id,a_id from asset_material where a_cd = \'{0}\''.format(a_cd)
	data = {'result':False}
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		row = cur.fetchone()
		if row:
			a_action_id,a_material_id = row
			if a_action_id == 0:
				sql2 = 'select a_name,a_type_cd,a_fuselage_cd,a_depart,a_loc_cd,a_action_id, \
					a_status,a_category from asset_material where a_cd = \'{0}\''.format(a_cd)
			else:
				sql2 = 'select a_m.a_name,a_m.a_type_cd,a_m.a_fuselage_cd,a_a.a_action_depart, \
					a_a.a_action_loc,a_a.a_action_type,a_action_state,a_action_category from \
					asset_material a_m, asset_action a_a \
					where a_m.a_action_id = a_a.a_id and a_m.a_cd = \'{0}\''.format(a_cd)
			cur.execute(sql2)
			row = cur.fetchone()
			if row:
				data = {
					'a_name':row[0],'a_type_cd':row[1],'a_fuselage_cd':row[2],'a_depart':row[3],
					'a_action_loc':row[4],'a_action_type':row[5],'a_action_state':row[6],
					'a_action_category':row[7],'a_material_id':a_material_id,'result':True
				}
		else:
			data['msg'] = '未搜索到数据'
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

#资产移动
def asset_move(asset_list,a_action_user,a_action_charge,a_opr_user,a_record_time,a_action_type):
	result = False
	try:
		cur = connections[MODEL].cursor()
		for asset in asset_list:
			a_cd = asset['a_cd']
			a_material_id = asset['a_material_id']
			a_action_state = asset['a_action_state']
			a_action_category = asset['a_action_category']
			a_origin_loc = asset['a_origin_loc']
			a_action_loc = asset['a_action_loc']
			a_origin_depart = asset['a_origin_depart']
			a_action_depart = asset['a_action_depart']
			a_action_model = asset['a_action_model']

			sql = 'insert into asset_action(a_cd,a_material_id,a_action_state,a_origin_depart,a_action_depart, \
				a_origin_loc,a_action_loc,a_action_user,a_action_charge,a_opr_user,a_record_time,a_action_type, \
				a_action_model,a_action_category) \
				values(\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\',\'{8}\',\'{9}\',\'{10}\',\'{11}\',\'{12}\',\'{13}\') \
				'.format(a_cd,a_material_id,a_action_state,a_origin_depart,a_action_depart,a_origin_loc,a_action_loc,
					a_action_user,a_action_charge,a_opr_user,a_record_time,a_action_type,a_action_model,a_action_category)
			cur.execute(sql)
			if cur.rowcount == 1:
				sql2 = 'select a_id from asset_action where a_material_id = \'{0}\' and a_record_time = \'{1}\' \
					and a_action_type = \'{2}\''.format(a_material_id,a_record_time,a_action_type)
				cur.execute(sql2)
				row = cur.fetchone()
				if row:
					a_id = row[0]
					sql3 = 'update asset_material set a_action_id = \'{0}\' where a_id = \'{1}\''.format(a_id,a_material_id)
					cur.execute(sql3)				
		result = True
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return result

#批量添加资产数据
def upload_add(table_data,a_opr_user,a_record_time):
	data = {'result':False}

	

	try:
		sql = 'insert into asset_material(a_cd,a_self_cd,a_name,a_type_cd,a_fuselage_cd,a_amount,\
			a_price,a_currency,a_out_time,a_purchase_time,a_project_cd,a_depart,a_brand,a_supplier,\
			a_loc_cd,a_status,a_category,a_model,a_funds_type,a_budget,a_referendum,a_po_cd,\
			a_sap_cd,a_b_nstd,a_need_cal,a_remark,a_user_id,a_record_time) values(%s, %s, %s, %s, %s, \
			%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
			%s, %s, %s, %s, \'{0}\',\'{1}\')'.format(a_opr_user,a_record_time)
		with transaction.atomic(using="asset_nstd"):
			cur = connections[MODEL].cursor()

			#验证资产番号是否已经录入
			for index,item in enumerate(table_data):
				a_cd = item[0]
				sql2 = 'select count(a_cd) from asset_material where a_cd = \'{0}\''.format(a_cd)
				cur.execute(sql2)
				row = cur.fetchone()
				if row[0] > 0:
					data['msg'] = '第{0}行，资产番号{1}已录入，不能重复录入!'.format(index + 1,a_cd)
					return data

			cur.executemany(sql,table_data)
			if cur.rowcount == len(table_data):
				data['result'] = True
				data['num'] = cur.rowcount
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	return data

#通过资产番号获取是详情信息
def is_instorage_by_a_cd(a_cd):
	a_action_type = '在库'
	sql = 'select a_action_id,a_id,a_status,a_loc_cd,a_category,a_price,a_supplier,a_name,a_type_cd, \
		a_depart,a_fuselage_cd,a_self_cd,a_need_cal,a_remark from asset_material where a_cd = \'{0}\''.format(a_cd)
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		row = cur.fetchone()

		if row:
			a_action_id,a_material_id,a_action_state,a_action_loc,a_action_category,a_price,a_supplier,a_name,a_type_cd,a_action_depart,a_fuselage_cd,a_self_cd,a_need_cal,a_action_remark = row
			if a_action_id != 0:
				'''
				if opr_his:
					sql_1 = 'select a_a.a_action_type,a_a.a_action_state,a_a.a_action_loc,a_a.a_action_category, \
						a_a.a_action_depart,a_a.a_action_remark,a_a.a_record_time from asset_material a_m,asset_action a_a \
						where a_m.a_action_id = a_a.a_id and a_m.a_cd = \'{0}\''.format(a_cd)
					sql_2 = 'select a_o.a_action_type,a_o.a_action_state,null,null,null,null,a_o.a_record_time from asset_material a_m, \
						asset_operation a_o where a_m.a_action_id = a_o.a_id and a_m.a_cd = \'{0}\''.format(a_cd)
					sql = '{0} union all {1} order by a_record_time desc limit 1'.format(sql_1,sql_2)
				else:
				'''
				sql = 'select a_a.a_action_type,a_a.a_action_state,a_a.a_action_loc,a_a.a_action_category, \
					a_a.a_action_depart,a_a.a_action_remark,a_a.a_record_time from asset_material a_m,asset_action a_a \
					where a_m.a_action_id = a_a.a_id and a_m.a_cd = \'{0}\''.format(a_cd)

				cur.execute(sql)
				row = cur.fetchone()
				if row:
					action_type,a_action_state,a_action_loc,a_action_category,a_action_depart,a_action_remark,a_record_time = row
					if action_type == 1:
						a_action_type = '已支给'
					elif action_type == 3:
						a_action_type = '已归还供应商'
					elif action_type == 5:
						a_action_type = '已出库'
					elif action_type == 6:
						a_action_type = '已销售'
					elif action_type == 7:
						a_action_type = '已报废'
					elif action_type == 8:
						a_action_type = '在线移动'
					elif action_type == 9:
						a_action_type = '库房移动'
					elif action_type == 10:
						a_action_type = '资产转换'
					elif action_type == 11:
						a_action_type = '修改位置'
					elif action_type == 12:
						a_action_type = '修改状态'
					elif action_type == 13:
						a_action_type = '修改折旧类别'
		else:
			a_action_type = '未入库'
			a_material_id = a_action_state = a_action_loc = a_price = a_supplier = a_action_remark = ''
			a_name = a_type_cd = a_action_category = a_action_depart = a_fuselage_cd = a_self_cd = a_need_cal = ''
			return [a_action_type,'','','','','','','','','','','','','','']
	except Exception as e:
		raise
	finally:
		connections[MODEL].close()
	return (a_action_type,a_material_id,a_action_state,a_action_loc,a_price,a_supplier,a_name,a_type_cd,
		a_action_depart,a_fuselage_cd,a_self_cd,a_need_cal,a_action_id,a_action_category,a_action_remark)

#资产批量出库
def upload_out(a_action_type,a_record_time,a_opr_user,table_data):
	num = 0
	try:
		cur = connections[MODEL].cursor()
		with transaction.atomic(using="asset_nstd"):
			for data in table_data:
				a_cd,a_action_state,a_action_depart,a_action_user,a_origin_loc,a_action_loc,a_action_model,a_action_charge,a_action_category,a_action_remark,a_material_id = data
				sql = 'insert into asset_action(a_action_type,a_record_time,a_opr_user,a_material_id, \
					a_action_depart,a_action_user,a_origin_loc,a_action_loc,a_action_model,a_action_state, \
					a_action_charge,a_action_category,a_action_remark,a_cd) values({0},\'{1}\',\'{2}\',\'{3}\', \
					\'{4}\',\'{5}\',\'{6}\',\'{7}\',\'{8}\',\'{9}\',\'{10}\',\'{11}\',\'{12}\',\'{13}\') \
					'.format(a_action_type,a_record_time,a_opr_user,a_material_id,a_action_depart,a_action_user,a_origin_loc,a_action_loc,a_action_model,a_action_state,a_action_charge,a_action_category,a_action_remark,a_cd)
				cur.execute(sql)
				if cur.rowcount == 1:
					sql2 = 'select a_id from asset_action where a_material_id = \'{0}\' and a_record_time = \'{1}\' \
						and a_action_type = {2}'.format(a_material_id,a_record_time,a_action_type)
					cur.execute(sql2)
					row = cur.fetchone()
					if row:
						a_id = row[0]
						sql3 = 'update asset_material set a_action_id = \'{0}\' where a_id = \'{1}\''.format(a_id,a_material_id)
						cur.execute(sql3)
						if cur.rowcount == 1:
							num += 1
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return num

#资产批量退库
def upload_back(a_action_type,a_record_time,a_opr_user,table_data):
	num = 0
	try:
		cur = connections[MODEL].cursor()
		with transaction.atomic(using="asset_nstd"):
			for data in table_data:
				a_cd,a_origin_loc,a_action_loc,a_action_user,a_action_state,a_action_charge,a_action_category,a_action_remark,a_material_id = data
				sql = 'insert into asset_action(a_action_type,a_record_time,a_opr_user,a_action_user,a_action_depart, \
					a_action_state,a_action_loc,a_action_charge,a_action_category,a_action_remark,a_material_id,a_origin_loc,a_cd) \
					values({0},\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\',\'{8}\',\'{9}\',\'{10}\',\'{11}\',\'{12}\') \
					'.format(a_action_type,a_record_time,a_opr_user,a_action_user,'IDLE',a_action_state,a_action_loc,
						a_action_charge,a_action_category,a_action_remark,a_material_id,a_origin_loc,a_cd)
				cur.execute(sql)
				if cur.rowcount == 1:
					sql2 = 'select a_id from asset_action where a_material_id = \'{0}\' and a_record_time = \'{1}\' \
						and a_action_type = \'{2}\''.format(a_material_id,a_record_time,a_action_type)
					cur.execute(sql2)
					row = cur.fetchone()
					if row:
						a_id = row[0]
						sql3 = 'update asset_material set a_action_id = \'{0}\' where a_id = \'{1}\''.format(a_id,a_material_id)
						cur.execute(sql3)
						if cur.rowcount == 1:
							num += 1
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return num

#资产批量支给
def upload_zj(a_action_type,a_record_time,a_opr_user,table_data):
	num = 0
	try:
		cur = connections[MODEL].cursor()
		with transaction.atomic(using="asset_nstd"):
			for data in table_data:
				a_cd,a_action_depart,a_action_charge,a_action_remark,a_action_loc,a_action_state,a_action_category,a_material_id = data
				sql = 'insert into asset_action(a_action_type,a_record_time,a_opr_user,a_action_depart,a_action_charge, \
					a_action_remark,a_action_loc,a_action_state,a_action_category,a_material_id,a_cd) \
					values({0},\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\',\'{8}\',\'{9}\',\'{10}\') \
					'.format(a_action_type,a_record_time,a_opr_user,a_action_depart,a_action_charge,a_action_remark,a_action_loc,a_action_state,a_action_category,a_material_id,a_cd)
				cur.execute(sql)
				if cur.rowcount == 1:
					sql2 = 'select a_id from asset_action where a_material_id = \'{0}\' and a_record_time = \'{1}\' \
						and a_action_type = \'{2}\''.format(a_material_id,a_record_time,a_action_type)
					cur.execute(sql2)
					row = cur.fetchone()
					if row:
						a_id = row[0]
						sql3 = 'update asset_material set a_action_id = \'{0}\' where a_id = \'{1}\''.format(a_id,a_material_id)
						cur.execute(sql3)
						if cur.rowcount == 1:
							num += 1
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return num

#资产批量支给归还
def upload_zj_revert(a_action_type,a_record_time,a_opr_user,table_data):
	num = 0
	try:
		cur = connections[MODEL].cursor()
		with transaction.atomic(using="asset_nstd"):
			for data in table_data:
				a_cd,a_action_loc,a_action_state,a_action_category,a_action_remark,a_material_id,a_action_supplier = data
				sql = 'insert into asset_action(a_action_type,a_record_time,a_opr_user, \
					a_action_loc,a_action_state,a_action_category,a_action_remark,a_material_id,a_cd,a_origin_loc) \
					values({0},\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\',\'{8}\',\'{9}\') \
					'.format(a_action_type,a_record_time,a_opr_user,a_action_loc,a_action_state,a_action_category,a_action_remark,a_material_id,a_cd,a_action_supplier)
				cur.execute(sql)
				if cur.rowcount == 1:
					sql2 = 'select a_id from asset_action where a_material_id = \'{0}\' and a_record_time = \'{1}\' \
						and a_action_type = \'{2}\''.format(a_material_id,a_record_time,a_action_type)
					cur.execute(sql2)
					row = cur.fetchone()
					if row:
						a_id = row[0]
						sql3 = 'update asset_material set a_action_id = \'{0}\' where a_id = \'{1}\''.format(a_id,a_material_id)
						cur.execute(sql3)
						if cur.rowcount == 1:
							num += 1
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return num

#借用资产批量归还
def upload_loan_revert(a_action_type,a_record_time,a_opr_user,table_data):
	num = 0
	try:
		cur = connections[MODEL].cursor()
		with transaction.atomic(using="asset_nstd"):
			for data in table_data:
				a_cd,a_material_id,a_action_supplier,a_action_remark = data
				sql = 'insert into asset_action(a_action_type, a_record_time, \
					a_opr_user, a_material_id, a_action_supplier, a_action_remark, a_cd) \
					values({0},\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\') \
					'.format(a_action_type,a_record_time,a_opr_user,a_material_id,a_action_supplier,a_action_remark,a_cd)
				cur.execute(sql)
				if cur.rowcount == 1:
					sql2 = 'select a_id from asset_action where a_material_id = \'{0}\' and a_record_time = \'{1}\' \
						and a_action_type = \'{2}\''.format(a_material_id,a_record_time,a_action_type)
					cur.execute(sql2)
					row = cur.fetchone()
					if row:
						a_id = row[0]
						sql3 = 'update asset_material set a_action_id = \'{0}\' where a_id = \'{1}\''.format(a_id,a_material_id)
						cur.execute(sql3)
						if cur.rowcount == 1:
							num += 1
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return num

#资产批量销售
def upload_sale(a_action_type,a_record_time,a_opr_user,table_data):
	num = 0
	try:
		cur = connections[MODEL].cursor()
		with transaction.atomic(using="asset_nstd"):
			for data in table_data:
				a_cd,a_action_supplier,a_action_remark,a_material_id = data
				sql = 'insert into asset_action(a_action_type,a_record_time,a_opr_user,a_cd,a_action_supplier, \
					a_action_remark,a_material_id) values({0},\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\') \
					'.format(a_action_type,a_record_time,a_opr_user,a_cd,a_action_supplier,a_action_remark,a_material_id)
				cur.execute(sql)
				if cur.rowcount == 1:
					sql2 = 'select a_id from asset_action where a_material_id = \'{0}\' and a_record_time = \'{1}\' \
						and a_action_type = \'{2}\''.format(a_material_id,a_record_time,a_action_type)
					cur.execute(sql2)
					row = cur.fetchone()
					if row:
						a_id = row[0]
						sql3 = 'update asset_material set a_action_id = \'{0}\' where a_id = \'{1}\''.format(a_id,a_material_id)
						cur.execute(sql3)
						if cur.rowcount == 1:
							num += 1
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return num

#资产批量报废
def upload_scrap(a_action_type,a_record_time,a_opr_user,table_data):
	num = 0
	try:
		cur = connections[MODEL].cursor()
		with transaction.atomic(using="asset_nstd"):
			for data in table_data:
				a_cd,a_action_remark,a_material_id = data
				sql = 'insert into asset_action(a_action_type,a_record_time,a_opr_user, \
					a_action_remark,a_material_id,a_cd) values({0},\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\') \
					'.format(a_action_type,a_record_time,a_opr_user,a_action_remark,a_material_id,a_cd)
				cur.execute(sql)
				if cur.rowcount == 1:
					sql2 = 'select a_id from asset_action where a_material_id = \'{0}\' and a_record_time = \'{1}\' \
						and a_action_type = \'{2}\''.format(a_material_id,a_record_time,a_action_type)
					cur.execute(sql2)
					row = cur.fetchone()
					if row:
						a_id = row[0]
						sql3 = 'update asset_material set a_action_id = \'{0}\' where \
							a_id = \'{1}\''.format(a_id,a_material_id)
						cur.execute(sql3)
						if cur.rowcount == 1:
							num += 1
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return num

#库房设备批量移动
def upload_instorage_move(a_action_type,a_record_time,a_opr_user,table_data):
	num = 0
	try:
		cur = connections[MODEL].cursor()
		with transaction.atomic(using="asset_nstd"):
			for data in table_data:
				a_cd,a_action_state,a_origin_loc,a_action_loc,a_material_id,a_action_depart = data
				#a_action_depart = '设备库房'
				sql = 'insert into asset_action(a_action_type,a_record_time,a_opr_user,a_cd, \
					a_action_state,a_action_depart,a_origin_loc,a_action_loc,a_material_id) \
					values({0},\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\',\'{8}\') returning a_id \
				'.format(a_action_type,a_record_time,a_opr_user,a_cd,a_action_state,a_action_depart,a_origin_loc,a_action_loc,a_material_id)
				cur.execute(sql)
				if cur.rowcount == 1:
					#sql2 = 'select a_id from asset_action where a_material_id = \'{0}\' and a_record_time = \'{1}\' \
					#	and a_action_type = \'{2}\''.format(a_material_id,a_record_time,a_action_type)
					#cur.execute(sql2)
					#row = cur.fetchone()
					#if row:
					a_id = cur.fetchone()[0]
					sql3 = 'update asset_material set a_action_id = \'{0}\' where a_id = \'{1}\''.format(a_id,a_material_id)
					cur.execute(sql3)
					if cur.rowcount == 1:
						num += 1
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return num

#库房设备批量移动
def upload_online_move(a_action_type,a_record_time,a_opr_user,table_data):
	num = 0
	try:
		cur = connections[MODEL].cursor()
		with transaction.atomic(using="asset_nstd"):
			for data in table_data:
				a_cd,a_action_state,a_origin_depart,a_action_depart,a_origin_loc,a_action_loc,a_action_category,a_action_user,a_action_charge,a_action_model,a_action_remark,a_material_id = data
				sql = 'insert into asset_action(a_action_type,a_record_time,a_opr_user,a_cd,a_action_state, \
					a_origin_depart,a_action_depart,a_origin_loc,a_action_loc,a_action_category, \
					a_action_user,a_action_charge,a_action_model,a_action_remark,a_material_id) values \
					({0},\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\',\'{8}\',\'{9}\',\'{10}\',\'{11}\',\'{12}\',\'{13}\',\'{14}\') \
				'.format(a_action_type,a_record_time,a_opr_user,a_cd,a_action_state,a_origin_depart,a_action_depart,a_origin_loc,
					a_action_loc,a_action_category,a_action_user,a_action_charge,a_action_model,a_action_remark,a_material_id)
				cur.execute(sql)
				if cur.rowcount == 1:
					sql2 = 'select a_id from asset_action where a_material_id = \'{0}\' and a_record_time = \'{1}\' \
						and a_action_type = \'{2}\''.format(a_material_id,a_record_time,a_action_type)
					cur.execute(sql2)
					row = cur.fetchone()
					if row:
						a_id = row[0]
						sql3 = 'update asset_material set a_action_id = \'{0}\' where a_id = \'{1}\''.format(a_id,a_material_id)
						cur.execute(sql3)
						if cur.rowcount == 1:
							num += 1
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return num

def upload_add_out(a_record_time,a_action_type,a_opr_user,table_data):
	add_out_data = {'result':True,'num':0}
	cur = connections[MODEL].cursor()
	try:
		with transaction.atomic(using="asset_nstd"):
			for data in table_data:
				sql1 = 'insert into asset_material(a_cd,a_self_cd,a_name,a_type_cd,a_fuselage_cd,a_amount,a_price,a_currency, \
					a_out_time,a_purchase_time,a_brand,a_supplier,a_status,a_category,a_project_cd,a_funds_type,a_record_time) \
					values(\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\',\'{8}\',\'{9}\',\'{10}\',\'{11}\', \
						\'{12}\',\'{13}\',\'{14}\',\'{15}\',\'{16}\') \
					'.format(data['a_cd'],data['a_self_cd'],data['a_name'],data['a_type_cd'],data['a_fuselage_cd'],
					data['a_amount'],data['a_price'],data['a_currency'],data['a_out_time'],data['a_purchase_time'],
					data['a_brand'],data['a_supplier'],data['a_status'],data['a_category'],data['a_project_cd'],
					data['a_funds_type'],a_record_time)
				cur.execute(sql1)
				if cur.rowcount == 1:
					sql2 = 'select a_id from asset_material where a_cd = \'{0}\''.format(data['a_cd'])
					cur.execute(sql2)
					row = cur.fetchone()
					if row:
						a_material_id = row[0]
						#资产出库
						sql3 = 'insert into asset_action(a_material_id,a_record_time,a_action_type,a_opr_user,a_cd, \
							a_action_depart,a_action_user,a_action_loc,a_action_model,a_action_charge,a_action_remark) \
							values(\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\',\'{8}\',\'{9}\',\'{10}\') \
							'.format(a_material_id,a_record_time,a_action_type,a_opr_user,data['a_cd'],data['a_action_depart'],
							data['a_action_user'],data['a_action_loc'],data['a_action_model'],data['a_action_charge'],data['a_action_remark'])
						cur.execute(sql3)
						if cur.rowcount == 1:
							sql4 = 'select a_id from asset_action where a_material_id = \'{0}\' and a_record_time = \'{1}\' \
								and a_action_type = \'{2}\''.format(a_material_id,a_record_time,a_action_type)
							cur.execute(sql4)
							row = cur.fetchone()
							if row:
								a_id = row[0]
								sql5 = 'update asset_material set a_action_id = \'{0}\' where a_id = \'{1}\''.format(a_id,a_material_id)
								cur.execute(sql5)
								if cur.rowcount == 1:
									add_out_data['num'] += 1
				else:
					print(data)
	except Exception as e:
		add_out_data['result'] = False
		print(data)
		print(e)
	finally:
		connections[MODEL].close()
	return add_out_data

def upload_add_instorage(table_data,a_record_time):
	data = {'result':False}
	try:
		sql = 'insert into asset_material(a_cd,a_self_cd,a_name,a_type_cd,a_fuselage_cd, \
			a_amount,a_price,a_currency,a_out_time,a_purchase_time,a_depart,a_loc_cd, \
			a_brand,a_supplier,a_po_cd,a_status,a_category,a_model,a_project_cd, \
			a_funds_type,a_b_nstd,a_record_time) \
			values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, \
			%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,\'{0}\')'.format(a_record_time)
		with transaction.atomic(using="asset_nstd"):
			cur = connections[MODEL].cursor()
			cur.executemany(sql,table_data)
			if cur.rowcount == len(table_data):
				data['result'] = True
				data['num'] = cur.rowcount
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	return data

#资产内部移动
def asset_instorage_move(a_opr_user,a_action_type,a_record_time,asset_list):
	num = 0
	try:
		with transaction.atomic(using="asset_nstd"):
			cur = connections[MODEL].cursor()
			for asset in asset_list:
				a_material_id = asset['a_material_id']
				sql = 'insert into asset_action(a_cd,a_material_id,a_action_state, \
					a_action_depart,a_origin_loc,a_action_loc,a_action_type,a_opr_user,a_record_time) \
					values(\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\',\'{8}\') \
					'.format(asset['a_cd'],a_material_id,asset['a_action_state'],asset['a_origin_depart'],
						asset['a_origin_loc'],asset['a_action_loc'],a_action_type,a_opr_user,a_record_time)
				cur.execute(sql)
				if cur.rowcount == 1:
					sql2 = 'select a_id from asset_action where a_material_id = \'{0}\' and a_action_type = \'{1}\' \
						and a_record_time = \'{2}\''.format(a_material_id,a_action_type,a_record_time)
					cur.execute(sql2)
					row = cur.fetchone()
					if row:
						a_id = row[0]
						sql3 = 'update asset_material set a_action_id = \'{0}\' where a_id = \'{1}\''.format(a_id,a_material_id)
						cur.execute(sql3)
						if cur.rowcount == 1:
							num += 1
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return num