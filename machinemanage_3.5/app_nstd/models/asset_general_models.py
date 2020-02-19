# -*- coding:utf-8 -*-
from django.db import connections
import datetime

global MODEL
MODEL = 'asset_nstd'

#入库信息查询
def get_add_data(a_cd,startDate,endDate,page,limit):
	data = []
	count = 0
	sql = 'select a_cd,a_self_cd,a_name,a_type_cd,a_fuselage_cd,a_amount,a_price,a_currency, \
		a_out_time,a_purchase_time,a_brand,a_supplier,a_status,a_loc_cd,a_record_time, \
		a_user_id,a_model,a_budget,a_referendum,a_po_cd,a_sap_cd,a_project_cd,a_funds_type, \
		a_remark from asset_material where 1 = 1'
	sql_count = 'select count(a_id) from asset_material where 1 = 1'

	if a_cd:
		sql += ' and a_cd = \'{0}\''.format(a_cd)
		sql_count += ' and a_cd = \'{0}\''.format(a_cd)
	if startDate:
		sql += ' and a_record_time >= \'{0}\''.format(startDate)
		sql_count += ' and a_record_time >= \'{0}\''.format(startDate)
	if endDate:
		sql += ' and a_record_time <= \'{0}\''.format(endDate)
		sql_count += ' and a_record_time <= \'{0}\''.format(endDate)
	if page != 0 and limit != 0:
		sql += ' order by a_record_time desc limit {0} offset {1}'.format(limit,(page - 1) * limit)
	else:
		sql += ' order by a_record_time desc'
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for row in rows:
			data.append({
				'a_cd':row[0],'a_self_cd':row[1],'a_name':row[2],'a_type_cd':row[3],
				'a_fuselage_cd':row[4],'a_amount':row[5],'a_price':row[6],'a_currency':row[7],
				'a_out_time':str(row[8])[0:10],'a_purchase_time':str(row[9])[0:10],'a_brand':row[10],
				'a_supplier':row[11],'a_status':row[12],'a_loc_cd':row[13],'a_record_time':str(row[14]),
				'a_user_id':row[15],'a_model':row[16],'a_budget':row[17],'a_referendum':row[18],
				'a_po_cd':row[19],'a_sap_cd':row[20],'a_project_cd':row[21],'a_funds_type':row[22],
				'a_remark':row[23]
			})
		cur.execute(sql_count)
		row = cur.fetchone()
		if row:
			count = row[0]
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	return data,count

#获取入库导出数据
def get_add_export_data(a_cd,startDate,endDate,page,limit):
	data = []
	count = 0
	sql = 'select a_cd,a_self_cd,a_name,a_type_cd,a_fuselage_cd,a_amount, \
		a_price,a_currency,a_out_time,a_purchase_time,a_brand,a_supplier, \
		a_status,a_loc_cd,a_record_time,a_user_id,a_model,a_budget,a_referendum, \
		a_po_cd,a_sap_cd,a_project_cd,a_funds_type,a_remark from asset_material where 1 = 1'
	if a_cd:
		sql += ' and a_cd = \'{0}\''.format(a_cd)
	if startDate:
		sql += ' and a_record_time >= \'{0}\''.format(startDate)
	if endDate:
		sql += ' and a_record_time <= \'{0}\''.format(endDate)
	sql += ' order by a_record_time desc'
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for row in rows:
			a_record_time = str(row[14])
			if a_record_time and len(a_record_time) > 10:
				a_record_time = a_record_time[:10]
			data.append({
				'a_cd':row[0],'a_self_cd':row[1],'a_name':row[2],'a_type_cd':row[3],
				'a_fuselage_cd':row[4],'a_amount':row[5],'a_price':row[6],'a_currency':row[7],
				'a_out_time':str(row[8])[0:10],'a_purchase_time':str(row[9])[0:10],'a_brand':row[10],
				'a_supplier':row[11],'a_status':row[12],'a_loc_cd':row[13],'a_record_time':a_record_time,
				'a_user_id':row[15],'a_model':row[16],'a_budget':row[17],'a_referendum':row[18],
				'a_po_cd':row[19],'a_sap_cd':row[20],'a_project_cd':row[21],'a_funds_type':row[22],
				'a_remark':row[23]
			})
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	return data

#支给信息查询
def get_zj_data(a_cd,startDate,endDate,page,limit):
	data = []
	count = 0
	sql = 'select a_m.a_cd,a_m.a_self_cd,a_m.a_name,a_m.a_type_cd,a_m.a_fuselage_cd,a_m.a_amount, \
		a_m.a_price,a_m.a_currency,a_m.a_price,a_m.a_out_time,a_m.a_purchase_time,a_m.a_brand, \
		a_m.a_supplier,a_a.a_action_supplier,a_a.a_action_state,a_a.a_action_loc,a_a.a_record_time, \
		a_a.a_opr_user,a_m.a_model,a_m.a_budget,a_m.a_referendum,a_m.a_po_cd,a_m.a_sap_cd, \
		a_m.a_project_cd,a_m.a_funds_type,a_a.a_action_remark from asset_material a_m,asset_action a_a \
		where a_m.a_action_id = a_a.a_id and a_a.a_action_type in (1)'

	sql2 = 'select count(a_m.a_id) from asset_material a_m,asset_action a_a \
		where a_m.a_action_id = a_a.a_id and a_a.a_action_type in (1)'
	if a_cd:
		sql += ' and a_m.a_cd = \'{0}\''.format(a_cd)
		sql2 += ' and a_m.a_cd = \'{0}\''.format(a_cd)
	if startDate:
		sql += ' and a_a.a_record_time >= \'{0}\''.format(startDate)
		sql2 += ' and a_a.a_record_time >= \'{0}\''.format(startDate)
	if endDate:
		sql += ' and a_a.a_record_time <= \'{0}\''.format(endDate)
		sql2 += ' and a_a.a_record_time <= \'{0}\''.format(endDate)

	sql += ' order by a_a.a_record_time desc'
	if page != 0 and limit != 0:
		sql += ' limit {0} offset {1}'.format(limit,limit * (page - 1))

	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for row in rows:
			data.append({
				'a_cd':row[0],'a_self_cd':row[1],'a_name':row[2],'a_type_cd':row[3],'a_fuselage_cd':row[4],
				'a_amount':row[5],'a_price':row[6],'a_currency':row[7],'a_price':row[8],'a_out_time':str(row[9]),
				'a_purchase_time':str(row[10]),'a_brand':row[11],'a_supplier':row[12],'a_action_supplier':row[13],
				'a_action_state':row[14],'a_action_loc':row[15],'a_record_time':str(row[16]),'a_opr_user':row[17],
				'a_model':row[18],'a_budget':row[19],'a_referendum':row[20],'a_po_cd':row[21],'a_sap_cd':row[22],
				'a_project_cd':row[23],'a_funds_type':row[24],'a_action_remark':row[25]
			})
		cur.execute(sql2)
		row = cur.fetchone()
		if row:
			count = row[0]
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	return data,count

#支给信息查询
def get_zj_export_data(a_cd,startDate,endDate):
	data = []
	sql = 'select a_m.a_cd,a_m.a_self_cd,a_m.a_name,a_m.a_type_cd,a_m.a_fuselage_cd,a_m.a_amount, \
		a_m.a_currency,a_m.a_price,a_m.a_out_time,a_m.a_purchase_time,a_m.a_brand,a_m.a_supplier, \
		a_a.a_action_supplier,a_a.a_action_state,a_a.a_action_loc,a_a.a_record_time,a_a.a_opr_user, \
		a_m.a_model,a_m.a_budget,a_m.a_referendum,a_m.a_po_cd,a_m.a_sap_cd,a_m.a_project_cd,\
		a_m.a_funds_type,a_a.a_action_remark from asset_material a_m,asset_action a_a where \
		a_m.a_action_id = a_a.a_id and a_a.a_action_type in (1)'
	if a_cd:
		sql += ' and a_m.a_cd = \'{0}\''.format(a_cd)
	if startDate:
		sql += ' and a_a.a_record_time >= \'{0}\''.format(startDate)
	if endDate:
		sql += ' and a_a.a_record_time <= \'{0}\''.format(endDate)

	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for row in rows:
			a_record_time = str(row[15])
			if a_record_time and len(a_record_time) > 10:
				a_record_time = a_record_time[:10]
			data.append({
				'a_cd':row[0],'a_self_cd':row[1],'a_name':row[2],'a_type_cd':row[3],'a_fuselage_cd':row[4],
				'a_amount':row[5],'a_currency':row[6],'a_price':row[7],'a_out_time':str(row[8])[0:10],
				'a_purchase_time':str(row[9])[0:10],'a_brand':row[10],'a_supplier':row[11],'a_action_supplier':row[12],
				'a_action_state':row[13],'a_action_loc':row[14],'a_record_time':a_record_time,'a_opr_user':row[16],
				'a_model':row[17],'a_budget':row[18],'a_referendum':row[19],'a_po_cd':row[20],'a_sap_cd':row[21],
				'a_project_cd':row[22],'a_funds_type':row[23],'a_action_remark':row[24]
			});
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	return data

#支给归还查询
def get_zj_revert_data(beginDate,endDate,a_cd,a_type_cd,a_self_cd,a_action_loc,a_action_state,page,limit):
	sql = 'select a_m.a_cd,a_m.a_self_cd,a_m.a_name,a_m.a_type_cd,a_m.a_fuselage_cd,a_m.a_amount, \
		a_m.a_currency,a_m.a_price,a_m.a_out_time,a_m.a_purchase_time,a_m.a_brand,a_m.a_supplier, \
		a_a.a_action_state,a_a.a_action_loc,a_a.a_record_time,a_a.a_opr_user,a_m.a_model, \
		a_m.a_budget,a_m.a_referendum,a_m.a_po_cd,a_m.a_sap_cd,a_m.a_project_cd, \
		a_m.a_funds_type,a_a.a_action_remark from asset_material a_m,asset_action a_a \
		where a_m.a_action_id = a_a.a_id and a_a.a_action_type = 2 \
		and a_a.a_record_time >= \'{0}\' and a_a.a_record_time <= \'{1}\''.format(beginDate,endDate)
	sql2 = 'select count(a_m.a_cd) from asset_material a_m,asset_action a_a \
		where a_m.a_action_id = a_a.a_id and a_a.a_action_type = 2 \
		and a_a.a_record_time >= \'{0}\' and a_a.a_record_time <= \'{1}\''.format(beginDate,endDate)

	count = 0
	if a_cd:
		sql += ' and a_m.a_cd = \'{0}\''.format(a_cd)
	if a_self_cd:
		sql += ' and a_m.a_self_cd = \'{0}\''.format(a_self_cd)
	if a_type_cd:
		sql += ' and a_m.a_type_cd = \'{0}\''.format(a_type_cd)
	if a_action_loc:
		sql += ' and a_a.a_action_loc = \'{0}\''.format(a_action_loc)
	if a_action_state:
		sql += ' and a_a.a_action_state = \'{0}\''.format(a_action_state)
	sql += ' limit {0} offset {1}'.format(limit,limit*(page-1))
	data = []
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for row in rows:
			data.append({
				'a_cd':row[0],'a_self_cd':row[1],'a_name':row[2],'a_type_cd':row[3],
				'a_fuselage_cd':row[4],'a_amount':row[5],'a_currency':row[6],'a_price':row[7],
				'a_out_time':str(row[8])[0:10],'a_purchase_time':str(row[9])[0:10],'a_brand':row[10],'a_supplier':row[11],
				'a_action_state':row[12],'a_action_loc':row[13],'a_record_time':str(row[14]),'a_opr_user':row[15],
				'a_model':row[16],'a_budget':row[17],'a_referendum':row[18],'a_po_cd':row[19],'a_sap_cd':row[20],
				'a_project_cd':row[21],'a_funds_type':row[22],'a_action_remark':row[23]
			})

		cur.execute(sql2)
		row = cur.fetchone()
		if row:
			count = row[0]
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	return data,count

#支给归还查询
def zj_revert_export_data():
	sql = 'select a_m.a_cd,a_m.a_self_cd,a_m.a_name,a_m.a_type_cd,a_m.a_fuselage_cd, \
		a_m.a_amount,a_m.a_currency,a_m.a_price,a_m.a_out_time,a_m.a_purchase_time, \
		a_m.a_brand,a_m.a_supplier,a_a.a_action_state,a_a.a_action_loc, \
		a_a.a_record_time,a_a.a_opr_user,a_m.a_model,a_m.a_budget, \
		a_m.a_referendum,a_m.a_po_cd,a_m.a_sap_cd,a_m.a_project_cd, \
		a_m.a_funds_type,a_a.a_action_remark from asset_material a_m, \
		asset_action a_a where a_m.a_action_id = a_a.a_id and a_a.a_action_type = 2'
	data = []
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for row in rows:
			data.append({
				'a_cd':row[0],'a_self_cd':row[1],'a_name':row[2],'a_type_cd':row[3],
				'a_fuselage_cd':row[4],'a_amount':row[5],'a_currency':row[6],
				'a_price':row[7],'a_out_time':str(row[8])[0:10],'a_purchase_time':str(row[9])[0:10],
				'a_brand':row[10],'a_supplier':row[11],'a_action_state':row[12],
				'a_action_loc':row[13],'a_record_time':str(row[14]),'a_opr_user':row[15],
				'a_model':row[16],'a_budget':row[17],'a_referendum':row[18],
				'a_po_cd':row[19],'a_sap_cd':row[20],'a_project_cd':row[21],
				'a_funds_type':row[22],'a_action_remark':row[23]
			})
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	return data

#出库信息查询
def get_out_storage_data(a_cd,a_action_loc,startDate,endDate,page,limit):
	data = []
	count = 0
	sql = 'select a_m.a_cd,a_m.a_self_cd,a_m.a_name,a_m.a_type_cd,a_m.a_fuselage_cd,a_m.a_amount, \
		a_m.a_price,a_m.a_currency,a_m.a_out_time,a_m.a_purchase_time,a_m.a_model, \
		a_m.a_brand,a_m.a_supplier,a_a.a_action_state,a_a.a_action_depart,a_a.a_action_user,\
		a_a.a_action_model,a_a.a_origin_loc,a_a.a_action_loc,a_a.a_action_charge,a_a.a_record_time,a_a.a_opr_user, \
		a_m.a_budget,a_m.a_referendum,a_m.a_po_cd,a_m.a_sap_cd,a_m.a_project_cd,a_m.a_funds_type, \
		a_a.a_opr_user,a_a.a_action_remark from asset_material a_m,asset_action a_a \
		where a_m.a_action_id = a_a.a_id and a_a.a_action_type = 5'

	sql2 = 'select count(a_m.a_id) from asset_material a_m,asset_action a_a \
		where a_m.a_action_id = a_a.a_id and a_a.a_action_type = 5'

	if a_cd:
		sql += ' and a_m.a_cd = \'{0}\''.format(a_cd)
		sql2 += ' and a_m.a_cd = \'{0}\''.format(a_cd)
	if a_action_loc:
		sql += ' and a_a.a_action_loc = \'{0}\''.format(a_action_loc)
		sql2 += ' and a_a.a_action_loc = \'{0}\''.format(a_action_loc)
	if startDate:
		sql += ' and a_a.a_record_time >= \'{0}\''.format(startDate)
		sql2 += ' and a_a.a_record_time >= \'{0}\''.format(startDate)
	if endDate:
		sql += ' and a_a.a_record_time <= \'{0}\''.format(endDate)
		sql2 += ' and a_a.a_record_time <= \'{0}\''.format(endDate)
	sql += ' limit {0} offset {1}'.format(limit,limit * (page - 1))
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for row in rows:
			data.append({
				'a_cd':row[0],'a_self_cd':row[1],'a_name':row[2],'a_type_cd':row[3],'a_fuselage_cd':row[4],
				'a_amount':row[5],'a_price':row[6],'a_currency':row[7],'a_out_time':str(row[8])[0:10],
				'a_purchase_time':str(row[9])[0:10],'a_model':row[10],'a_brand':row[11],'a_supplier':row[12],
				'a_action_state':row[13],'a_action_depart':row[14],'a_action_user':row[15],'a_action_model':row[16],
				'a_origin_loc':row[17],'a_action_loc':row[18],'a_action_charge':row[19],'a_record_time':str(row[20]),
				'a_opr_user':row[21],'a_budget':row[22],'a_referendum':row[23],'a_po_cd':row[24],'a_sap_cd':row[25],
				'a_project_cd':row[26],'a_funds_type':row[27],'a_opr_user':row[28],'a_action_remark':row[29]
			})
		cur.execute(sql2)
		row = cur.fetchone()
		if row:
			count = row[0]
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	print(count)
	return data,count

#导出出库数据
def get_out_export_data(a_cd,a_action_loc,startDate,endDate):
	data = []
	sql = 'select a_m.a_cd,a_m.a_self_cd,a_m.a_name,a_m.a_type_cd,a_m.a_fuselage_cd, \
		a_m.a_amount,a_m.a_currency,a_m.a_price,a_m.a_out_time,a_m.a_purchase_time, \
		a_m.a_model,a_m.a_brand,a_m.a_supplier,a_a.a_action_state,a_a.a_action_depart, \
		a_a.a_action_user,a_a.a_action_model,a_a.a_action_loc,a_a.a_action_charge, \
		a_a.a_record_time,a_a.a_opr_user,a_m.a_budget,a_m.a_referendum,a_m.a_po_cd, \
		a_m.a_sap_cd,a_m.a_project_cd,a_m.a_funds_type,a_a.a_opr_user, \
		a_a.a_action_remark from asset_material a_m,asset_action a_a \
		where a_m.a_action_id = a_a.a_id and a_a.a_action_type in (5,8)'
	if a_cd:
		sql += ' and a_m.a_cd = \'{0}\''.format(a_cd)
	if a_action_loc:
		sql += ' and a_a.a_action_loc = \'{0}\''.format(a_action_loc)
	if startDate:
		sql += ' and a_a.a_record_time >= \'{0}\''.format(startDate)
	if endDate:
		sql += ' and a_a.a_record_time <= \'{0}\''.format(endDate)

	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for row in rows:
			a_record_time = str(row[19])
			if a_record_time and len(a_record_time) > 10:
				a_record_time = a_record_time[:10]
			data.append({
				'a_cd':row[0],'a_self_cd':row[1],'a_name':row[2],'a_type_cd':row[3],'a_fuselage_cd':row[4],
				'a_amount':row[5],'a_currency':row[6],'a_price':row[7],'a_out_time':str(row[8])[0:10],
				'a_purchase_time':str(row[9])[0:10],'a_model':row[10],'a_brand':row[11],'a_supplier':row[12],
				'a_action_state':row[13],'a_action_depart':row[14],'a_action_user':row[15],'a_action_model':row[16],
				'a_action_loc':row[17],'a_action_charge':row[18],'a_record_time':a_record_time,'a_opr_user':row[20],
				'a_budget':row[21],'a_referendum':row[22],'a_po_cd':row[23],'a_sap_cd':row[24],'a_project_cd':row[25],
				'a_funds_type':row[26],'a_opr_user':row[27],'a_action_remark':row[28]
			});
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	return data

#资产退库数据
def get_back_storage_data(a_cd,a_action_loc,startDate,endDate,page,limit):
	sql = 'select a_m.a_cd,a_m.a_self_cd,a_m.a_name,a_m.a_type_cd,a_m.a_fuselage_cd,a_m.a_amount, \
		a_m.a_currency,a_m.a_price,a_m.a_out_time,a_m.a_purchase_time,a_m.a_brand,a_m.a_supplier, \
		a_a.a_action_state,a_a.a_action_loc,a_a.a_record_time,a_a.a_opr_user,a_m.a_model,a_m.a_budget, \
		a_m.a_referendum,a_m.a_po_cd,a_m.a_sap_cd,a_m.a_project_cd,a_m.a_funds_type,a_a.a_action_depart, \
		a_a.a_action_user,a_a.a_action_charge,a_a.a_action_remark from asset_material a_m,asset_action a_a \
		where a_m.a_id = a_a.a_material_id and a_a.a_action_type = 4'
	sql2 = 'select count(a_m.a_cd) from asset_material a_m,asset_action a_a \
		where a_m.a_id = a_a.a_material_id and a_a.a_action_type = 4'

	
	if a_cd:
		sql += ' and a_m.a_cd = \'{0}\''.format(a_cd)
		sql2 += ' and a_m.a_cd = \'{0}\''.format(a_cd)
	if a_action_loc:
		sql += ' and a_a.a_action_loc = \'{0}\''.format(a_action_loc)
		sql2 += ' and a_a.a_action_loc = \'{0}\''.format(a_action_loc)
	if startDate:
		sql += ' and a_a.a_record_time >= \'{0}\''.format(startDate)
		sql2 += ' and a_a.a_record_time >= \'{0}\''.format(startDate)
	if endDate:
		sql += ' and a_a.a_record_time <= \'{0}\''.format(endDate)
		sql2 += ' and a_a.a_record_time <= \'{0}\''.format(endDate)

	sql += 'order by a_a.a_record_time desc limit {0} offset {1}'.format(limit, limit * (page - 1))
	data = []
	count = 0
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for row in rows:
			data.append({
				'a_cd':row[0],'a_self_cd':row[1],'a_name':row[2],'a_type_cd':row[3],'a_fuselage_cd':row[4],
				'a_amount':row[5],'a_currency':row[6],'a_price':row[7],'a_out_time':str(row[8])[0:10],
				'a_purchase_time':str(row[9])[0:10],'a_brand':row[10],'a_supplier':row[11],'a_action_state':row[12],
				'a_action_loc':row[13],'a_record_time':str(row[14]),'a_opr_user':row[15],'a_model':row[16],
				'a_budget':row[17],'a_referendum':row[18],'a_po_cd':row[19],'a_sap_cd':row[20],'a_project_cd':row[21],
				'a_funds_type':row[22],'a_action_depart':row[23],'a_action_user':row[24],'a_action_charge':row[25],
				'a_action_remark':row[26]
			})

		cur.execute(sql2)
		row = cur.fetchone()
		if row:
			count = row[0]
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	return data,count

def get_back_export_data(a_cd,a_action_loc,startDate,endDate):
	sql = 'select a_m.a_cd,a_m.a_self_cd,a_m.a_name,a_m.a_type_cd,a_m.a_fuselage_cd, \
		a_m.a_amount,a_m.a_price,a_m.a_currency,a_m.a_out_time,a_m.a_purchase_time, \
		a_m.a_brand,a_m.a_supplier,a_a.a_action_state,a_a.a_action_loc,a_a.a_record_time, \
		a_a.a_opr_user,a_m.a_model,a_m.a_budget,a_m.a_referendum,a_m.a_po_cd,a_m.a_sap_cd, \
		a_m.a_project_cd,a_m.a_funds_type,a_a.a_action_depart,a_a.a_action_user, \
		a_a.a_action_charge,a_a.a_action_remark from asset_material a_m,asset_action a_a \
		where a_m.a_id = a_a.a_material_id and a_a.a_action_type = 4'
	if a_cd:
		sql += ' and a_m.a_cd = \'{0}\''.format(a_cd)
	if a_action_loc:
		sql += ' and a_a.a_action_loc = \'{0}\''.format(a_action_loc)
	if startDate:
		sql += ' and a_a.a_record_time >= \'{0}\''.format(startDate)
	if endDate:
		sql += ' and a_a.a_record_time <= \'{0}\''.format(endDate)
	sql += ' order by a_a.a_record_time desc'
	data = []
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for row in rows:
			a_record_time = str(row[14])
			if a_record_time and len(a_record_time) > 10:
				a_record_time = a_record_time[:10]
			data.append({
				'a_cd':row[0],'a_self_cd':row[1],'a_name':row[2],'a_type_cd':row[3],
				'a_fuselage_cd':row[4],'a_amount':row[5],'a_price':row[6],'a_currency':row[7],
				'a_out_time':str(row[8])[0:10],'a_purchase_time':str(row[9])[0:10],
				'a_brand':row[10],'a_supplier':row[11],'a_action_state':row[12],
				'a_action_loc':row[13],'a_record_time':a_record_time,'a_opr_user':row[15],
				'a_model':row[16],'a_budget':row[17],'a_referendum':row[18],'a_po_cd':row[19],
				'a_sap_cd':row[20],'a_project_cd':row[21],'a_funds_type':row[22],
				'a_action_depart':row[23],'a_action_user':row[24],
				'a_action_charge':row[25],'a_action_remark':row[26]
			});
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	return data

#设备归还查询
def get_loan_revert_data(a_cd,startDate,endDate,page,limit):
	sql = 'select a_m.a_cd,a_m.a_self_cd,a_m.a_name,a_m.a_type_cd,a_m.a_fuselage_cd,a_m.a_amount,\
		a_m.a_currency,a_m.a_price,a_m.a_out_time,a_m.a_purchase_time,a_m.a_brand,a_m.a_supplier,\
		a_a.a_action_state,a_action_loc,a_a.a_record_time,a_a.a_opr_user,a_m.a_model,a_m.a_budget,\
		a_m.a_referendum,a_m.a_po_cd,a_m.a_sap_cd,a_m.a_project_cd,a_m.a_funds_type,a_action_remark \
		from asset_material a_m,asset_action a_a where a_m.a_action_id = a_a.a_id and a_a.a_action_type = 3'
	sql_count = 'select count(*) from asset_material a_m,asset_action a_a where a_m.a_action_id = a_a.a_id and a_a.a_action_type = 3'
	if a_cd:
		sql += ' and a_m.a_cd = \'{0}\''.format(a_cd)
		sql_count += ' and a_m.a_cd = \'{0}\''.format(a_cd)
	if startDate:
		sql += ' and a_a.a_record_time >= \'{0}\''.format(startDate)
		sql_count += ' and a_a.a_record_time >= \'{0}\''.format(startDate)
	if endDate:
		sql += ' and a_a.a_record_time <= \'{0}\''.format(endDate)
		sql += ' and a_a.a_record_time <= \'{0}\''.format(endDate)

	sql += ' order by a_a.a_record_time desc limit {0} offset {1}'.format(limit,int(limit) * (int(page) - 1))

	data = []
	count = 0
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for row in rows:
			data.append({
				'a_cd':row[0],'a_self_cd':row[1],'a_name':row[2],'a_type_cd':row[3],'a_fuselage_cd':row[4],
				'a_amount':row[5],'a_currency':row[6],'a_price':row[7],'a_out_time':str(row[8])[:10],
				'a_purchase_time':str(row[9])[:10],'a_brand':row[10],'a_supplier':row[11],'a_action_state':row[12],
				'a_action_loc':row[13],'a_record_time':str(row[14]),'a_opr_user':row[15],'a_model':row[16],
				'a_budget':row[17],'a_referendum':row[18],'a_po_cd':row[19],'a_sap_cd':row[20],
				'a_project_cd':row[21],'a_funds_type':row[22],'a_action_remark':row[23]
			})
		cur.execute(sql_count)
		row = cur.fetchone()
		count = row[0]
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	return data,count

#设备归还查询
def loan_revert_export_data(a_cd,startDate,endDate):
	sql = 'select a_m.a_cd,a_m.a_self_cd,a_m.a_name,a_m.a_type_cd,a_m.a_fuselage_cd, \
		a_m.a_amount,a_m.a_currency,a_m.a_price,a_m.a_out_time,a_m.a_purchase_time, \
		a_m.a_brand,a_m.a_supplier,a_a.a_action_state,a_action_loc,a_a.a_record_time, \
		a_a.a_opr_user,a_m.a_model,a_m.a_budget,a_m.a_referendum,a_m.a_po_cd,\
		a_m.a_sap_cd,a_m.a_project_cd,a_m.a_funds_type,a_action_remark from \
		asset_material a_m,asset_action a_a where a_m.a_action_id = a_a.a_id \
		and a_a.a_action_type = 3'
	if a_cd:
		sql += ' and a_m.a_cd = \'{0}\''.format(a_cd)
	if startDate:
		sql += ' and a_a.a_record_time >= \'{0}\''.format(startDate)
	if endDate:
		sql += ' and a_a.a_record_time <= \'{0}\''.format(endDate)

	sql += ' order by a_a.a_record_time desc'

	data = []
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for row in rows:
			a_record_time = str(row[14])
			if a_record_time and len(a_record_time) > 10:
				a_record_time = a_record_time[:10]
			data.append({
				'a_cd':row[0],'a_self_cd':row[1],'a_name':row[2],'a_type_cd':row[3],
				'a_fuselage_cd':row[4],'a_amount':row[5],'a_currency':row[6],
				'a_price':row[7],'a_out_time':str(row[8])[:10],'a_purchase_time':str(row[9])[:10],
				'a_brand':row[10],'a_supplier':row[11],'a_action_state':row[12],
				'a_action_loc':row[13],'a_record_time':a_record_time,'a_opr_user':row[15],
				'a_model':row[16],'a_budget':row[17],'a_referendum':row[18],
				'a_po_cd':row[19],'a_sap_cd':row[20],'a_project_cd':row[21],
				'a_funds_type':row[22],'a_action_remark':row[23]
			})
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	return data

#获取销售数据
def get_sale_data(a_cd,startDate,endDate,page,limit):
	sql = 'select a_m.a_cd,a_m.a_self_cd,a_m.a_name,a_m.a_type_cd,a_m.a_fuselage_cd,a_m.a_amount, \
		a_m.a_currency,a_m.a_out_time,a_m.a_purchase_time,a_m.a_brand,a_m.a_supplier,a_a.a_action_supplier, \
		a_a.a_action_state,a_a.a_action_loc,a_a.a_record_time,a_a.a_opr_user,a_m.a_model,a_m.a_budget, \
		a_m.a_referendum,a_m.a_po_cd,a_m.a_sap_cd,a_m.a_project_cd,a_m.a_funds_type,a_a.a_action_remark from \
		asset_material a_m,asset_action a_a where a_m.a_action_id = a_a.a_id and a_a.a_action_type = 6'
	sql_count = 'select count(*) from asset_material a_m,asset_action a_a where a_m.a_action_id = a_a.a_id and a_a.a_action_type = 6'
		
	if a_cd:
		sql += ' and a_m.a_cd = \'{0}\''.format(a_cd)
		sql_count += ' and a_m.a_cd = \'{0}\''.format(a_cd)
	if startDate:
		sql += ' and a_a.a_record_time >= \'{0}\''.format(startDate)
		sql_count += ' and a_a.a_record_time >= \'{0}\''.format(startDate)
	if endDate:
		sql += ' and a_a.a_record_time <= \'{0}\''.format(endDate)
		sql_count += ' and a_a.a_record_time <= \'{0}\''.format(endDate)
	sql += ' order by a_record_time desc limit {0} offset {1}'.format(int(limit), (int(page) - 1) * int(limit))
	data = []
	count = 0
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for row in rows:
			data.append({
				'a_cd':row[0],'a_self_cd':row[1],'a_name':row[2],'a_type_cd':row[3],'a_fuselage_cd':row[4],
				'a_amount':row[5],'a_currency':row[6],'a_out_time':str(row[7]),'a_purchase_time':str(row[8]),
				'a_brand':row[9],'a_supplier':row[10],'a_action_supplier':row[11],'a_action_state':row[12],
				'a_action_loc':row[13],'a_record_time':str(row[14]),'a_opr_user':row[15],'a_model':row[16],
				'a_budget':row[17],'a_referendum':row[18],'a_po_cd':row[19],'a_sap_cd':row[20],
				'a_project_cd':row[21],'a_funds_type':row[22],'a_action_remark':row[23]
			});
		cur.execute(sql_count)
		row = cur.fetchone()
		if row:
			count = row[0]
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data,count

#获取销售数据
def get_sale_export_data(a_cd,startDate,endDate):
	sql = 'select a_m.a_cd,a_m.a_self_cd,a_m.a_name,a_m.a_type_cd,a_m.a_fuselage_cd, \
		a_m.a_amount,a_m.a_currency,a_m.a_out_time,a_m.a_purchase_time,a_m.a_brand, \
		a_m.a_supplier,a_a.a_action_supplier,a_a.a_action_state,a_a.a_action_loc, \
		a_a.a_record_time,a_a.a_opr_user,a_m.a_model,a_m.a_budget,a_m.a_referendum, \
		a_m.a_po_cd,a_m.a_sap_cd,a_m.a_project_cd,a_m.a_funds_type,a_a.a_action_remark \
		from asset_material a_m,asset_action a_a where a_m.a_action_id = a_a.a_id \
		and a_a.a_action_type = 6'
	if a_cd:
		sql += ' and a_m.a_cd = \'{0}\''.format(a_cd)
	if startDate:
		sql += ' and a_a.a_record_time >= \'{0}\''.format(startDate)
	if endDate:
		sql += ' and a_a.a_record_time <= \'{0}\''.format(endDate)

	data = []
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for row in rows:
			a_record_time = str(row[14])
			if a_record_time and len(a_record_time) > 10:
				a_record_time = a_record_time[:10]
			data.append({
				'a_cd':row[0],'a_self_cd':row[1],'a_name':row[2],'a_type_cd':row[3],
				'a_fuselage_cd':row[4],'a_amount':row[5],'a_currency':row[6],
				'a_out_time':str(row[7])[0:10],'a_purchase_time':str(row[8])[0:10],
				'a_brand':row[9],'a_supplier':row[10],'a_action_supplier':row[11],
				'a_action_state':row[12],'a_action_loc':row[13],'a_record_time':a_record_time,
				'a_opr_user':row[15],'a_model':row[16],'a_budget':row[17],
				'a_referendum':row[18],'a_po_cd':row[19],'a_sap_cd':row[20],
				'a_project_cd':row[21],'a_funds_type':row[22],'a_action_remark':row[23]
			});
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

#获取报废数据
def get_scrap_data(a_cd, startDate, endDate, page, limit):
	sql = 'select a_m.a_cd,a_m.a_self_cd,a_m.a_name,a_m.a_type_cd,a_m.a_fuselage_cd,a_m.a_amount,a_m.a_price, \
		a_m.a_currency,a_m.a_out_time,a_m.a_purchase_time,a_m.a_brand,a_m.a_supplier,a_a.a_action_state,\
		a_a.a_action_loc,a_a.a_record_time,a_a.a_opr_user,a_m.a_model,a_m.a_budget,a_m.a_referendum, \
		a_m.a_po_cd,a_m.a_sap_cd,a_m.a_project_cd,a_m.a_funds_type,a_a.a_action_remark from \
		asset_material a_m,asset_action a_a where a_m.a_action_id = a_a.a_id and a_a.a_action_type = 7'
	sql2 = 'select count(*) from asset_material a_m,asset_action a_a where a_m.a_action_id = a_a.a_id and a_a.a_action_type = 7'
	if a_cd:
		sql += ' and a_m.a_cd = \'{0}\''.format(a_cd)
		sql2 += ' and a_m.a_cd = \'{0}\''.format(a_cd)
	if startDate:
		sql += ' and a_a.a_record_time >= \'{0}\''.format(startDate)
		sql2 += ' and a_a.a_record_time >= \'{0}\''.format(startDate)
	if endDate:
		sql += ' and a_a.a_record_time <= \'{0}\''.format(endDate)
		sql2 += ' and a_a.a_record_time <= \'{0}\''.format(endDate)
	sql += ' order by a_a.a_record_time desc limit {0} offset {1}'.format(int(limit),int(limit) * (int(page) - 1))

	data = []
	count = 0
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for row in rows:
			data.append({
				'a_cd':row[0],'a_self_cd':row[1],'a_name':row[2],'a_type_cd':row[3],'a_fuselage_cd':row[4],
				'a_amount':row[5],'a_price':row[6],'a_currency':row[7],'a_out_time':str(row[8])[0:10],
				'a_purchase_time':str(row[9])[0:10],'a_brand':row[10],'a_supplier':row[11],
				'a_action_state':row[12],'a_action_loc':row[13],'a_record_time':str(row[14]),
				'a_user_id':row[15],'a_model':row[16],'a_budget':row[17],'a_referendum':row[18],
				'a_po_cd':row[19],'a_sap_cd':row[20],'a_project_cd':row[21],
				'a_funds_type':row[22],'a_remark':row[23]
			});
		cur.execute(sql2)
		row = cur.fetchone()
		if row:
			count = int(row[0])
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data, count

#获取报废数据
def get_scrap_export_data(a_cd,startDate,endDate):
	sql = 'select a_m.a_cd,a_m.a_self_cd,a_m.a_name,a_m.a_type_cd,a_m.a_fuselage_cd,a_m.a_amount, \
		a_m.a_currency,a_m.a_out_time,a_m.a_purchase_time,a_m.a_brand,a_m.a_supplier,a_a.a_action_state,\
		a_a.a_action_loc,a_a.a_record_time,a_a.a_opr_user,a_m.a_model,a_m.a_budget,a_m.a_referendum, \
		a_m.a_po_cd,a_m.a_sap_cd,a_m.a_project_cd,a_m.a_funds_type,a_a.a_action_remark from \
		asset_material a_m,asset_action a_a where a_m.a_action_id = a_a.a_id and a_a.a_action_type = 7'
	if a_cd:
		sql += ' and a_m.a_cd = \'{0}\''.format(a_cd)
	if startDate:
		sql += ' and a_a.a_record_time >= \'{0}\''.format(startDate)
	if endDate:
		sql += ' and a_a.a_record_time <= \'{0}\''.format(endDate)
	data = []
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for row in rows:
			a_record_time = str(row[13])
			if a_record_time and len(a_record_time) > 10:
				a_record_time = a_record_time[:10]
			data.append({
				'a_cd':row[0],'a_self_cd':row[1],'a_name':row[2],'a_type_cd':row[3],'a_fuselage_cd':row[4],
				'a_amount':row[5],'a_currency':row[6],'a_out_time':str(row[7])[0:10],
				'a_purchase_time':str(row[8])[0:10],'a_brand':row[9],'a_supplier':row[10],'a_action_state':row[11],
				'a_action_loc':row[12],'a_record_time':a_record_time,'a_user_id':row[14],'a_model':row[15],
				'a_budget':row[16],'a_referendum':row[17],'a_po_cd':row[18],'a_sap_cd':row[19],
				'a_project_cd':row[20],'a_funds_type':row[21],'a_remark':row[22]
			});
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

#获取移动数据
def get_move_data(a_cd,startDate,endDate,page,limit):
	sql1 = 'select a_m.a_cd,a_m.a_self_cd,a_m.a_name,a_m.a_type_cd,a_m.a_fuselage_cd,a_m.a_amount,\
		a_m.a_currency,a_m.a_price,a_m.a_out_time,a_m.a_purchase_time,a_m.a_brand,a_m.a_supplier, \
		a_a.a_action_state,a_a.a_origin_loc,a_a.a_action_loc,a_a.a_record_time,a_a.a_opr_user, \
		a_m.a_model,a_m.a_budget,a_m.a_referendum,a_m.a_po_cd,a_m.a_sap_cd,a_m.a_project_cd, \
		a_m.a_funds_type,a_a.a_action_remark,a_a.a_action_user,a_a.a_action_charge from \
		asset_material a_m,asset_action a_a where a_m.a_action_id = a_a.a_id and a_a.a_action_type = 8'

	sql2 = 'select count(*) from asset_material a_m,asset_action a_a \
		where a_m.a_action_id = a_a.a_id and a_a.a_action_type = 8'

	if a_cd:
		sql1 += ' and a_m.a_cd = \'{0}\''.format(a_cd)
		sql2 += ' and a_m.a_cd = \'{0}\''.format(a_cd)
	if startDate:
		sql1 += ' and a_a.a_record_time >= \'{0}\''.format(startDate)
		sql2 += ' and a_a.a_record_time >= \'{0}\''.format(startDate)
	if endDate:
		sql1 += ' and a_a.a_record_time <= \'{0}\''.format(endDate)
		sql2 += ' and a_a.a_record_time <= \'{0}\''.format(endDate)

	sql1 += ' limit {0} offset {1}'.format(int(limit),int(limit) * (int(page) - 1))
	data = []
	count = 0
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql1)
		rows = cur.fetchall()
		for row in rows:
			data.append({
				'a_cd':row[0],'a_self_cd':row[1],'a_name':row[2],'a_type_cd':row[3],'a_fuselage_cd':row[4],
				'a_amount':row[5],'a_currency':row[6],'a_price':row[7],'a_out_time':str(row[8])[0:10],
				'a_purchase_time':str(row[9])[0:10],'a_brand':row[10],'a_supplier':row[11],'a_action_state':row[12],
				'a_origin_loc':row[13],'a_action_loc':row[14],'a_record_time':str(row[15]),'a_opr_user':row[16],
				'a_model':row[17],'a_budget':row[18],'a_referendum':row[19],'a_po_cd':row[20],'a_sap_cd':row[21],
				'a_project_cd':row[22],'a_funds_type':row[23],'a_action_remark':row[24],'a_action_user':row[25],
				'a_action_charge':row[26]
			})
		cur.execute(sql2)
		row = cur.fetchone()
		if row:
			count = row[0]
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data,count

#获取移动数据
def get_move_export_data(a_cd,startDate,endDate):
	sql = 'select a_m.a_cd,a_m.a_self_cd,a_m.a_name,a_m.a_type_cd,a_m.a_fuselage_cd,a_m.a_amount,\
		a_m.a_currency,a_m.a_price,a_m.a_out_time,a_m.a_purchase_time,a_m.a_brand,a_m.a_supplier, \
		a_a.a_action_state,a_a.a_origin_loc,a_a.a_action_loc,a_a.a_record_time,a_a.a_opr_user, \
		a_m.a_model,a_m.a_budget,a_m.a_referendum,a_m.a_po_cd,a_m.a_sap_cd,a_m.a_project_cd, \
		a_m.a_funds_type,a_a.a_action_remark,a_a.a_action_user,a_a.a_action_charge from \
		asset_material a_m,asset_action a_a where a_m.a_action_id = a_a.a_id and a_a.a_action_type = 8'

	if a_cd:
		sql += ' and a_m.a_cd = \'{0}\''.format(a_cd)
	if startDate:
		sql += ' and a_a.a_record_time >= \'{0}\''.format(startDate)
	if endDate:
		sql += ' and a_a.a_record_time <= \'{0}\''.format(endDate)

	data = []
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for row in rows:
			data.append({
				'a_cd':row[0],'a_self_cd':row[1],'a_name':row[2],'a_type_cd':row[3],'a_fuselage_cd':row[4],
				'a_amount':row[5],'a_currency':row[6],'a_price':row[7],'a_out_time':str(row[8])[0:10],
				'a_purchase_time':str(row[9])[0:10],'a_brand':row[10],'a_supplier':row[11],'a_action_state':row[12],
				'a_origin_loc':row[13],'a_action_loc':row[14],'a_record_time':str(row[15]),'a_opr_user':row[16],
				'a_model':row[17],'a_budget':row[18],'a_referendum':row[19],'a_po_cd':row[20],'a_sap_cd':row[21],
				'a_project_cd':row[22],'a_funds_type':row[23],'a_action_remark':row[24],'a_action_user':row[25],
				'a_action_charge':row[26]
			});
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

#在库信息查询
def get_in_storage_data(a_cd,a_action_loc,startDate,endDate,page,limit):
	data = []
	count = 0
	sql1 = 'select a_cd,a_self_cd,a_name,a_type_cd,a_fuselage_cd,a_amount,a_currency,a_out_time, \
		a_purchase_time,a_brand,a_supplier,a_status,a_loc_cd,a_record_time,a_user_id,a_model, \
		a_budget,a_referendum,a_po_cd,a_sap_cd,a_project_cd,a_funds_type,a_remark \
		from asset_material where a_action_id = 0'
	sql1_count = 'select count(a_cd) from asset_material where a_action_id = 0'

	if a_cd:
		sql1 += ' and a_cd = \'{0}\''.format(a_cd)
		sql1_count += ' and a_cd = \'{0}\''.format(a_cd)
	if a_action_loc:
		sql1 += ' and a_loc_cd = \'{0}\''.format(a_action_loc)
		sql1_count += ' and a_loc_cd = \'{0}\''.format(a_action_loc)
	if startDate:
		sql1 += ' and a_record_time >= \'{0}\''.format(startDate)
		sql1_count += ' and a_record_time >= \'{0}\''.format(endDate)
	if endDate:
		sql1 += ' and a_record_time <= \'{0}\''.format(startDate)
		sql1_count += ' and a_record_time <= \'{0}\''.format(endDate)

	sql2 = 'select a_m.a_cd,a_m.a_self_cd,a_m.a_name,a_m.a_type_cd,a_m.a_fuselage_cd,a_m.a_amount, \
		a_m.a_currency,a_m.a_out_time,a_m.a_purchase_time,a_m.a_brand,a_m.a_supplier,a_a.a_action_state, \
		a_a.a_action_loc,a_a.a_record_time,a_m.a_user_id,a_m.a_model,a_m.a_budget,a_m.a_referendum, \
		a_m.a_po_cd,a_m.a_sap_cd,a_m.a_project_cd,a_m.a_funds_type,a_m.a_remark from asset_material a_m, \
		asset_action a_a where a_m.a_action_id = a_a.a_id and a_a.a_action_type in (2,4,9)'
	sql2_count = 'select count(*) from asset_material a_m,asset_action a_a \
		where a_m.a_action_id = a_a.a_id and a_a.a_action_type in (2,4,9)'

	if a_cd:
		sql2 += ' and a_m.a_cd = \'{0}\''.format(a_cd)
		sql2_count += ' and a_m.a_cd = \'{0}\''.format(a_cd)
	if a_action_loc:
		sql2 += ' and a_a.a_action_loc = \'{0}\''.format(a_action_loc)
		sql2_count += ' and a_a.a_action_loc = \'{0}\''.format(a_action_loc)
	if startDate:
		sql2 += ' and a_a.a_record_time >= \'{0}\''.format(startDate)
		sql2_count += ' and a_a.a_record_time >= \'{0}\''.format(startDate)
	if endDate:
		sql2 += ' and a_a.a_record_time <= \'{0}\''.format(endDate)
		sql2_count += ' and a_a.a_record_time <= \'{0}\''.format(endDate)

	sql = sql1 + ' union all ' + sql2
	if page != 0 and limit != 0:
		sql += ' order by a_record_time desc limit {0} offset {1}'.format(limit, limit * (page - 1))
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for row in rows:
			data.append({
				'a_cd':row[0],'a_self_cd':row[1],'a_name':row[2],'a_type_cd':row[3],'a_fuselage_cd':row[4],
				'a_amount':row[5],'a_currency':row[6],'a_out_time':str(row[7])[0:10],'a_purchase_time':str(row[8])[0:10],
				'a_brand':row[9],'a_supplier':row[10],'a_action_state':row[11],'a_action_loc':row[12],
				'a_record_time':str(row[13]),'a_user_id':row[14],'a_model':row[15],'a_budget':row[16],
				'a_referendum':row[17],'a_po_cd':row[18],'a_sap_cd':row[19],'a_project_cd':row[20],
				'a_funds_type':row[21],'a_remark':row[22]
			})

		cur.execute(sql1_count)
		row = cur.fetchone()
		if row:
			count += int(row[0])

		cur.execute(sql2_count)
		row = cur.fetchone()
		if row:
			count += int(row[0])
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data, count

#在库信息到处
def get_in_storage_export_data(a_cd,a_action_loc,startDate,endDate):
	data = []
	sql1 = 'select a_cd,a_self_cd,a_name,a_type_cd,a_fuselage_cd,a_amount,a_price,a_currency, \
		a_out_time,a_purchase_time,a_brand,a_supplier,a_status,a_loc_cd,a_record_time,a_user_id, \
		a_model,a_budget,a_referendum,a_po_cd,a_sap_cd,a_project_cd,a_funds_type,a_remark \
		from asset_material where a_action_id = 0'
	if a_cd:
		sql1 += ' and a_cd = \'{0}\''.format(a_cd)
	if a_action_loc:
		sql1 += ' and a_loc_cd = \'{0}\''.format(a_cd)
	if startDate:
		sql1 += ' and a_record_time >= \'{0}\''.format(startDate)
	if endDate:
		sql1 += ' and a_record_time <= \'{0}\''.format(endDate)

	sql2 = 'select a_m.a_cd,a_m.a_self_cd,a_m.a_name,a_m.a_type_cd,a_m.a_fuselage_cd, \
		a_m.a_amount,a_m.a_price,a_m.a_currency,a_m.a_out_time,a_m.a_purchase_time,a_m.a_brand, \
		a_m.a_supplier,a_a.a_action_state,a_a.a_action_loc,a_a.a_record_time, \
		a_m.a_user_id,a_m.a_model,a_m.a_budget,a_m.a_referendum,a_m.a_po_cd,a_m.a_sap_cd, \
		a_m.a_project_cd,a_m.a_funds_type,a_m.a_remark from asset_material a_m, \
		asset_action a_a where a_m.a_action_id = a_a.a_id and a_a.a_action_type in (2,4,9)'
	if a_cd:
		sql2 += ' and a_a.a_cd = \'{0}\''.format(a_cd)
	if a_action_loc:
		sql2 += ' and a_a.a_action_loc = \'{0}\''.format(a_action_loc)
	if startDate:
		sql2 += ' and a_a.a_record_time >= \'{0}\''.format(startDate)
	if endDate:
		sql2 += ' and a_a.a_record_time <= \'{0}\''.format(endDate)

	sql = sql1 + ' union all ' + sql2
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for row in rows:
			a_record_time = str(row[14])
			if a_record_time and len(a_record_time) > 10:
				a_record_time = a_record_time[:10]
			data.append({
				'a_cd':row[0],'a_self_cd':row[1],'a_name':row[2],'a_type_cd':row[3],'a_fuselage_cd':row[4],
				'a_amount':row[5],'a_price':row[6],'a_currency':row[7],'a_out_time':str(row[8])[0:10],
				'a_purchase_time':str(row[9])[0:10],'a_brand':row[10],'a_supplier':row[11],
				'a_action_state':row[12],'a_action_loc':row[13],'a_record_time':a_record_time,
				'a_user_id':row[15],'a_model':row[16],'a_budget':row[17],'a_referendum':row[18],
				'a_po_cd':row[19],'a_sap_cd':row[20],'a_project_cd':row[21],
				'a_funds_type':row[22],'a_remark':row[23]
			});
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

#在线信息查询
def get_online_data(a_cd,a_action_loc,startDate,endDate,page,limit):
	data = []
	count = 0
	sql = 'select a_m.a_cd,a_m.a_self_cd,a_m.a_name,a_m.a_type_cd,a_m.a_fuselage_cd,a_m.a_amount, \
		a_m.a_price,a_m.a_currency,a_m.a_out_time,a_m.a_purchase_time,a_m.a_brand,a_m.a_supplier, \
		a_a.a_action_state,a_a.a_action_depart,a_a.a_action_loc,a_a.a_action_category,a_a.a_record_time, \
		a_a.a_opr_user,a_m.a_model,a_m.a_budget,a_m.a_referendum,a_m.a_po_cd,a_m.a_project_cd,a_m.a_funds_type, \
		a_a.a_action_remark,a_a.a_action_model from asset_material a_m,asset_action a_a where a_m.a_action_id = a_a.a_id'
		
	sql2 = 'select count(a_m.a_id) from asset_material a_m,asset_action a_a \
		where a_m.a_action_id = a_a.a_id and a_a.a_action_type in (5,8)'

	if a_cd:
		sql += ' and a_m.a_cd = \'{0}\''.format(a_cd)
		sql2 += ' and a_m.a_cd = \'{0}\''.format(a_cd)
	if a_action_loc:
		sql += ' and a_a.a_action_loc = \'{0}\''.format(a_action_loc)
		sql2 += ' and a_a.a_action_loc = \'{0}\''.format(a_action_loc)
	if startDate:
		sql += ' and a_a.a_record_time >= \'{0}\''.format(startDate)
		sql2 += ' and a_a.a_record_time >= \'{0}\''.format(startDate)
	if endDate:
		sql += ' and a_a.a_record_time <= \'{0}\''.format(endDate)
		sql2 += ' and a_a.a_record_time <= \'{0}\''.format(endDate)

	sql += ' and a_a.a_action_type in (5,8) order by a_a.a_record_time desc'
	if page != 0 and limit != 0:
		sql += ' limit {0} offset {1}'.format(limit,limit * (page - 1))
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for row in rows:
			data.append({
				'a_cd':row[0],'a_self_cd':row[1],'a_name':row[2],'a_type_cd':row[3],
				'a_fuselage_cd':row[4],'a_amount':row[5],'a_price':row[6],'a_currency':row[7],
				'a_out_time':str(row[8])[0:10],'a_purchase_time':str(row[9])[0:10],'a_brand':row[10],
				'a_supplier':row[11],'a_action_state':row[12],'a_action_depart':row[13],
				'a_action_loc':row[14],'a_action_category':row[15],'a_record_time':str(row[16]),
				'a_opr_user':row[17],'a_model':row[18],'a_budget':row[19],'a_referendum':row[20],
				'a_po_cd':row[21],'a_project_cd':row[22],'a_funds_type':row[23],
				'a_action_remark':row[24],'a_action_model':row[25]
			})
		cur.execute(sql2)
		row = cur.fetchone()
		if row:
			count = row[0]
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data,count

#在线信息查询
def get_online_export_data(a_cd,a_action_loc,startDate,endDate):
	data = []
	sql = 'select a_m.a_cd,a_m.a_self_cd,a_m.a_name,a_m.a_type_cd,a_m.a_fuselage_cd,a_m.a_amount, \
		a_m.a_price,a_m.a_currency,a_m.a_out_time,a_m.a_purchase_time,a_m.a_brand,a_m.a_supplier, \
		a_a.a_action_state,a_a.a_action_depart,a_a.a_action_loc,a_a.a_record_time,a_a.a_opr_user, \
		a_a.a_action_model,a_m.a_budget,a_m.a_referendum,a_m.a_po_cd,a_m.a_project_cd,a_m.a_funds_type, \
		a_a.a_action_remark from asset_material a_m,asset_action a_a where a_m.a_action_id = a_a.a_id'
	if a_cd:
		sql += ' and a_m.a_cd = \'{0}\''.format(a_cd)
	if a_action_loc:
		sql += ' and a_a.a_action_loc = \'{0}\''.format(a_action_loc)
	if startDate:
		sql += ' and a_a.a_record_time >= \'{0}\''.format(startDate)
	if endDate:
		sql += ' and a_a.a_record_time <= \'{0}\''.format(endDate)
	sql += ' and a_a.a_action_type in (5,8) order by a_a.a_record_time desc'
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for row in rows:
			a_record_time = str(row[15])
			if a_record_time and len(a_record_time) > 10:
				a_record_time = a_record_time[:10]
			data.append({
				'a_cd':row[0],'a_self_cd':row[1],'a_name':row[2],'a_type_cd':row[3],
				'a_fuselage_cd':row[4],'a_amount':row[5],'a_price':row[6],'a_currency':row[7],
				'a_out_time':str(row[8])[0:10],'a_purchase_time':str(row[9])[0:10],'a_brand':row[10],
				'a_supplier':row[11],'a_action_state':row[12],'a_action_depart':row[13],
				'a_action_loc':row[14],'a_record_time':a_record_time,'a_opr_user':row[16],
				'a_action_model':row[17],'a_budget':row[18],'a_referendum':row[19],
				'a_po_cd':row[20],'a_project_cd':row[21],'a_funds_type':row[22],
				'a_action_remark':row[23]
			})
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

#获取总账信息
def total_export_data(startDate,endDate):
	sql1 = 'select a_cd,a_self_cd,a_name,a_type_cd,a_fuselage_cd,a_amount,a_price,a_currency,a_out_time, \
		a_purchase_time,a_brand,a_supplier,a_loc_cd,a_status,a_category,a_model,a_budget,a_referendum, \
		a_po_cd,a_sap_cd,a_project_cd,a_funds_type,null,a_record_time,a_user_id,a_remark,a_action_id, \
		a_need_cal,a_depart,null,a_remark from asset_material where a_action_id = 0'
	if startDate:
		sql1 += ' and a_record_time >= \'{0}\''.format(startDate)
	if endDate:
		sql1 += ' and a_record_time <= \'{0}\''.format(endDate)

	sql2 = 'select a_m.a_cd,a_m.a_self_cd,a_m.a_name,a_m.a_type_cd,a_m.a_fuselage_cd,a_m.a_amount, \
		a_m.a_price,a_m.a_currency,a_m.a_out_time,a_m.a_purchase_time,a_m.a_brand,a_m.a_supplier, \
		a_a.a_action_loc,a_a.a_action_state,a_a.a_action_category,a_m.a_model,a_m.a_budget,a_m.a_referendum, \
		a_m.a_po_cd,a_m.a_sap_cd,a_m.a_project_cd,a_m.a_funds_type,a_action_model,a_m.a_record_time, \
		a_a.a_opr_user,a_a.a_action_remark,a_action_type,a_m.a_need_cal,a_a.a_action_depart, \
		a_a.a_action_supplier,a_remark from asset_material a_m,asset_action a_a \
		where a_m.a_action_id = a_a.a_id'
	if startDate:
		sql2 += ' and a_a.a_record_time >= \'{0}\''.format(startDate)
	if endDate:
		sql2 += ' and a_a.a_record_time <= \'{0}\''.format(endDate)

	sql = '{0} union all {1}'.format(sql1,sql2)
	data = []
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for row in rows:
			a_action_type = row[26]
			if a_action_type == 0 or a_action_type == 2 or a_action_type == 4 or a_action_type == 9:
				a_action_type = '在库'
			elif a_action_type == 1:
				a_action_type = '支给'
			elif a_action_type == 3:
				a_action_type = '已归还供应商'
			elif a_action_type == 5 or a_action_type == 8:
				a_action_type = '在线'
			elif a_action_type == 6:
				a_action_type = '已销售'
			elif a_action_type == 7:
				a_action_type = '已报废'
			elif a_action_type == 10:
				a_action_type = '资产转换'
			elif a_action_type == 11:
				a_action_type = '修改位置'
			elif a_action_type == 12:
				a_action_type = '修改状态'
			elif a_action_type == 13:
				a_action_type = '修改折旧类别'
				
			a_need_cal = row[27]
			if a_need_cal == 0:
				a_need_cal = '不需要计量'
			elif a_need_cal == 1:
				a_need_cal = '需要计量'

			if a_action_type == '在库' or a_action_type == '在线' or a_action_type == '支给' or a_action_type == '资产转换' or a_action_type == '修改位置' or a_action_type == '修改状态' or a_action_type == '修改折旧类别':
				data.append({
					'a_cd':row[0],'a_self_cd':row[1],'a_name':row[2],'a_type_cd':row[3],'a_fuselage_cd':row[4],
					'a_amount':row[5],'a_price':row[6],'a_currency':row[7],'a_out_time':row[8],
					'a_purchase_time':row[9],'a_brand':row[10],'a_supplier':row[11],'a_action_loc':row[12],
					'a_action_state':row[13],'a_action_category':row[14],'a_model':row[15],'a_budget':row[16],
					'a_referendum':row[17],'a_po_cd':row[18],'a_sap_cd':row[19],'a_project_cd':row[20],
					'a_funds_type':row[21],'a_action_model':row[22],'a_record_time':row[23],'a_opr_user':row[24],
					'a_action_remark':row[25],'a_action_type':a_action_type,'a_need_cal':a_need_cal,
					'a_action_depart':row[28],'a_action_supplier':row[29],'a_remark':row[30]
				})
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

#获取操作历史记录
def get_history_data(a_cd):
	data = []
	a_origin_cd = ''	#资产转换前的资产番号
	try:
		sql1 = 'select a_cd,a_self_cd,a_name,a_type_cd,a_fuselage_cd,a_amount,a_currency,a_price, \
			a_funds_type,a_out_time,a_purchase_time,a_brand,a_supplier,a_po_cd,a_sap_cd,a_project_cd, \
			a_model,a_budget,a_referendum,a_depart,a_loc_cd,a_status,a_category,a_record_time, \
			a_user_id,a_remark from asset_material where a_cd = \'{0}\''.format(a_cd)
		cur = connections[MODEL].cursor()
		cur.execute(sql1)
		row = cur.fetchone()
		if row:
			data.append({
				'a_cd':row[0],'a_self_cd':row[1],'a_name':row[2],'a_type_cd':row[3],'a_fuselage_cd':row[4],
				'a_amount':row[5],'a_currency':row[6],'a_price':row[7],'a_funds_type':row[8],'a_out_time':str(row[9])[0:10],
				'a_purchase_time':str(row[10])[0:10],'a_brand':row[11],'a_supplier':row[12],'a_po_cd':row[13],
				'a_sap_cd':row[14],'a_project_cd':row[15],'a_model':row[16],'a_budget':row[17],'a_referendum':row[18],
				'a_depart':row[19],'a_action_loc':row[20],'a_action_state':row[21],'a_action_category':row[22],
				'a_record_time':str(row[23]),'a_opr_user':row[24],'a_action_remark':row[25],'a_action_type':'入库'
			})

		sql2 = 'select a_m.a_cd,a_m.a_self_cd,a_m.a_name,a_m.a_type_cd,a_m.a_fuselage_cd,a_m.a_amount,a_m.a_currency, \
			a_m.a_price,a_m.a_funds_type,a_m.a_out_time,a_m.a_purchase_time,a_m.a_brand,a_m.a_supplier, \
			a_m.a_po_cd,a_m.a_sap_cd,a_m.a_project_cd,a_m.a_model,a_m.a_budget,a_m.a_referendum,a_m.a_depart, \
			a_a.a_action_type,a_a.a_opr_user,a_a.a_action_state,a_a.a_action_loc,a_a.a_action_category, \
			a_a.a_action_supplier,a_a.a_action_charge,a_a.a_origin_loc,a_a.a_action_depart,a_a.a_action_user, \
			a_a.a_action_remark,a_a.a_record_time,a_a.a_origin_cd,a_a.a_origin_state,a_a.a_origin_category,a_a.a_origin_depart \
			from asset_material a_m,asset_action a_a \
			where a_m.a_id = a_a.a_material_id and a_m.a_cd = \'{0}\''.format(a_cd)

		sql3 = 'select a_o.a_cd,a_m.a_self_cd,a_m.a_name,a_m.a_type_cd,a_m.a_fuselage_cd,a_m.a_amount,a_m.a_currency, \
			a_m.a_price,a_m.a_funds_type,a_m.a_out_time,a_m.a_purchase_time,a_m.a_brand,a_m.a_supplier, \
			a_m.a_po_cd,a_m.a_sap_cd,a_m.a_project_cd,a_m.a_model,a_m.a_budget,a_m.a_referendum,a_m.a_depart, \
			a_o.a_action_type,a_o.a_opr_user,a_o.a_action_state,a_o.a_action_loc,null, \
			null,null,a_o.a_origin_loc,a_o.a_action_depart,null, \
			null,a_o.a_record_time,a_o.a_origin_cd,a_o.a_origin_state,null,a_o.a_origin_depart \
			from asset_material a_m, asset_operation a_o \
			where a_m.a_id = a_o.a_material_id and a_m.a_cd = \'{0}\''.format(a_cd)
		sql = '{0} union all {1} order by a_record_time'.format(sql2, sql3)
		cur.execute(sql)
		rows = cur.fetchall()
		if rows:
			for row in rows:
				tmp_dict = {
					'a_cd':row[0],'a_self_cd':row[1],'a_name':row[2],'a_type_cd':row[3],'a_fuselage_cd':row[4],
					'a_amount':row[5],'a_currency':row[6],'a_price':row[7],'a_funds_type':row[8],
					'a_out_time':str(row[9])[0:10],'a_purchase_time':str(row[10])[0:10],'a_brand':row[11],
					'a_supplier':row[12],'a_po_cd':row[13],'a_sap_cd':row[14],'a_project_cd':row[15],
					'a_model':row[16],'a_budget':row[17],'a_referendum':row[18],'a_depart':row[19],
					'a_opr_user':row[21],'a_action_state':row[22],'a_action_loc':row[23],'a_action_category':row[24],
					'a_action_charge':row[26],'a_action_remark':row[30],'a_record_time':str(row[31]),
					'a_origin_cd':row[32],'a_origin_state':row[33],'a_origin_category':row[34],'a_origin_depart':row[35]
				}
				action_type = row[20]
				if action_type != 10 and data and not a_origin_cd:
					a_origin_cd = row[0]
					data[0]['a_cd'] = a_origin_cd

				if action_type == 1:
					tmp_dict['a_action_type'] = '支给'
					tmp_dict['a_zj_supplier'] = row[25]
					tmp_dict['a_action_loc'] = row[25]		#支给后当前位置显示供应商
					tmp_dict['a_action_depart'] = 'CPSR'	#支给后当前部门显示CPSR
				elif action_type == 2:
					tmp_dict['a_action_type'] = '支给归还'
					tmp_dict['a_origin_loc'] = row[25]
				elif action_type == 3:
					tmp_dict['a_action_type'] = '归还供应商'
				elif action_type == 4:
					tmp_dict['a_action_type'] = '退库'
					tmp_dict['a_back_user'] = row[29]
				elif action_type == 5:
					tmp_dict['a_action_type'] = '出库'
					tmp_dict['a_take_depart'] = row[28]
					tmp_dict['a_take_user'] = row[29]
				elif action_type == 6:
					tmp_dict['a_action_type'] = '销售'
					tmp_dict['a_sale_supplier'] = row[25]
				elif action_type == 7:
					tmp_dict['a_action_type'] = '报废'
				elif action_type == 8:
					tmp_dict['a_action_type'] = '在线移动'
					tmp_dict['a_move_depart'] = row[28]
					tmp_dict['a_origin_loc'] = row[27]
				elif action_type == 9:
					tmp_dict['a_action_type'] = '库房移动'
					tmp_dict['a_origin_loc'] = row[27]
				elif action_type == 10:
					tmp_dict['a_action_type'] = '资产转换'
				elif action_type == 11:
					tmp_dict['a_action_type'] = '修改位置'
					tmp_dict['a_origin_loc'] = row[27]
				elif action_type == 12:
					tmp_dict['a_action_type'] = '修改状态'
				elif action_type == 13:
					tmp_dict['a_action_type'] = '修改折旧类别'
				elif action_type == 14:
					tmp_dict['a_action_type'] = '修改所在部门'

				data.append(tmp_dict)
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data