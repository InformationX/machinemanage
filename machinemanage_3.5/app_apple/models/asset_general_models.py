# -*- coding:utf-8 -*-
from django.db import connections, transaction
from config.models import common
import json,datetime

global MODEL
MODEL = 'asset_b'

#查询在库数据
def get_storage_data(beginDate,endDate,page,limit):
	count = 0

	sql_0 = 'select a_cd,a_type_cd,a_fuselage_cd,a_main_cd,a_main_serial,a_loc_cd, \
		a_state, a_remark, a_add_time from asset_material where a_action_type = 0'
	sql_count_0 = 'select count(a_cd) from asset_material where a_action_type = 0'

	if beginDate:
		sql_0 += ' and a_add_time >= \'{0}\''.format(beginDate)
		sql_count_0 += ' and a_add_time >= \'{0}\''.format(beginDate)
	if endDate:
		sql_0 += ' and a_add_time <= \'{0}\''.format(endDate)
		sql_count_0 += ' and a_add_time <= \'{0}\''.format(endDate)

	sql_2 = 'select a_m.a_cd,a_m.a_type_cd,a_m.a_fuselage_cd,aob.a_main_cd,aob.a_main_serial, \
		aob.a_action_loc,aob.a_action_state,aob.a_action_remark,aob.a_add_time from asset_material a_m, \
		asset_out_back aob where a_m.a_action_id = aob.id and a_m.a_action_type = 2'
	sql_count_2 = 'select count(a_m.a_cd) from asset_material a_m, asset_out_back aob \
		where a_m.a_action_id = aob.id and a_m.a_action_type = 2'

	if beginDate:
		sql_2 += ' and aob.a_add_time >= \'{0}\''.format(beginDate)
		sql_count_2 += ' and aob.a_add_time >= \'{0}\''.format(beginDate)
	if endDate:
		sql_2 += ' and aob.a_add_time <= \'{0}\''.format(endDate)
		sql_count_2 += ' and aob.a_add_time <= \'{0}\''.format(endDate)

	sql_4 = 'select a_m.a_cd,a_m.a_type_cd,a_m.a_fuselage_cd,azb.a_main_cd,azb.a_main_serial, \
		azb.a_action_loc,azb.a_action_state,azb.a_action_remark,azb.a_add_time from asset_material a_m, \
		asset_zj_back azb where a_m.a_action_id = azb.id and a_m.a_action_type = 4'
	sql_count_4 = 'select count(a_m.a_cd) from asset_material a_m, asset_zj_back azb \
		where a_m.a_action_id = azb.id and a_m.a_action_type = 4'

	if beginDate:
		sql_4 += ' and azb.a_add_time >= \'{0}\''.format(beginDate)
		sql_count_4 += ' and azb.a_add_time >= \'{0}\''.format(beginDate)
	if endDate:
		sql_4 += ' and azb.a_add_time <= \'{0}\''.format(endDate)
		sql_count_4 += ' and azb.a_add_time <= \'{0}\''.format(endDate)

	sql = sql_0 + ' union all ' + sql_2 + ' union all ' + sql_4
	sql += ' limit {0} offset {1}'.format(limit,limit*(page-1))

	sql_count = sql_count_0 + ' union all ' + sql_count_2 + ' union all ' + sql_count_4

	data = []
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for row in rows:
			data.append({
				'a_cd':row[0],'a_type_cd':row[1],'a_fuselage_cd':row[2],'a_main_cd':row[3],
				'a_main_serial':row[4],'a_action_loc':row[5],'a_action_state':row[6],
				'a_action_remark':row[7],'a_add_time':str(row[8])
			});
		
		cur.execute(sql_count)
		rows = cur.fetchall()
		for row in rows:
			count += int(row[0])
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data,count

#获取在库导出数据
def get_storage_export(beginDate,endDate):
	sql_0 = 'select a_cd,a_type_cd,a_fuselage_cd,a_main_cd,a_main_serial,a_loc_cd, \
		a_state, a_remark, a_add_time from asset_material where a_action_type = 0'
	if beginDate:
		sql_0 += ' and a_add_time >= \'{0}\''.format(beginDate)
	if endDate:
		sql_0 += ' and a_add_time <= \'{0}\''.format(endDate)

	sql_2 = 'select a_m.a_cd,a_m.a_type_cd,a_m.a_fuselage_cd,aob.a_main_cd,aob.a_main_serial, \
		aob.a_action_loc,aob.a_action_state,aob.a_action_remark,aob.a_add_time from asset_material a_m, \
		asset_out_back aob where a_m.a_action_id = aob.id and a_m.a_action_type = 2'
	if beginDate:
		sql_2 += ' and aob.a_add_time >= \'{0}\''.format(beginDate)
	if endDate:
		sql_2 += ' and aob.a_add_time <= \'{0}\''.format(endDate)

	sql_4 = 'select a_m.a_cd,a_m.a_type_cd,a_m.a_fuselage_cd,azb.a_main_cd,azb.a_main_serial, \
		azb.a_action_loc,azb.a_action_state,azb.a_action_remark,azb.a_add_time from asset_material a_m, \
		asset_zj_back azb where a_m.a_action_id = azb.id and a_m.a_action_type = 4'

	if beginDate:
		sql_4 += ' and azb.a_add_time >= \'{0}\''.format(beginDate)
	if endDate:
		sql_4 += ' and azb.a_add_time <= \'{0}\''.format(endDate)

	sql = sql_0 + ' union all ' + sql_2 + ' union all ' + sql_4

	data = []
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for row in rows:
			data.append({
				'a_cd':row[0],'a_type_cd':row[1],'a_fuselage_cd':row[2],'a_main_cd':row[3],
				'a_main_serial':row[4],'a_action_loc':row[5],'a_action_state':row[6],
				'a_action_remark':row[7],'a_add_time':str(row[8])
			});
		
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

#查询总账数据
def get_total_data(startDate, endTime):
	data = []
	sql_0 = 'select a_cd,a_type_cd,a_fuselage_cd,a_main_cd,a_main_serial,a_loc_cd,a_state, \
		a_dept_cd,a_remark,a_action_type,null,a_add_time,a_opr_user from asset_material where a_action_type = 0'
	if startDate:
		sql_0 += ' and a_add_time >= \'{0}\''.format(startDate)
	if endTime:
		sql_0 += ' and a_add_time <= \'{0}\''.format(endTime)

	sql_1 = 'select a_m.a_cd,a_m.a_type_cd,a_m.a_fuselage_cd,a_o.a_main_cd,a_o.a_main_serial,a_o.a_action_loc,a_o.a_action_state, \
		a_o.a_action_dept,a_o.a_action_remark,a_m.a_action_type,a_o.a_action_model,a_o.a_add_time,a_o.a_opr_user \
		from asset_material a_m, asset_out a_o where a_m.a_action_id = a_o.id and a_m.a_action_type = 1'
	if startDate:
		sql_1 += ' and a_o.a_add_time >= \'{0}\''.format(startDate)
	if endTime:
		sql_1 += ' and a_o.a_add_time <= \'{0}\''.format(endTime)

	sql_2 = 'select a_m.a_cd,a_m.a_type_cd,a_m.a_fuselage_cd,aob.a_main_cd,aob.a_main_serial,aob.a_action_loc, \
		aob.a_action_state,aob.a_action_dept,aob.a_action_remark,a_m.a_action_type,null,aob.a_add_time,aob.a_opr_user \
		from asset_material a_m, asset_out_back aob where a_m.a_action_id = aob.id and a_m.a_action_type = 2'
	if startDate:
		sql_2 += ' and aob.a_add_time >= \'{0}\''.format(startDate)
	if endTime:
		sql_2 += ' and aob.a_add_time <= \'{0}\''.format(endTime)

	sql_3 = 'select a_m.a_cd,a_m.a_type_cd,a_m.a_fuselage_cd,a_z.a_main_cd,a_z.a_main_serial,a_z.a_zj_object, \
		a_z.a_action_state,a_z.a_zj_dept,a_z.a_action_remark,a_m.a_action_type,null,a_z.a_add_time,a_z.a_opr_user \
		from asset_material a_m, asset_zj a_z where a_m.a_action_id = a_z.id and a_m.a_action_type = 3'
	if startDate:
		sql_3 += ' and a_z.a_add_time >= \'{0}\''.format(startDate)
	if endTime:
		sql_3 += ' and a_z.a_add_time <= \'{0}\''.format(endTime)

	sql_4 = 'select a_m.a_cd,a_m.a_type_cd,a_m.a_fuselage_cd,azb.a_main_cd,azb.a_main_serial,azb.a_action_loc, \
		azb.a_action_state,a_action_dept,azb.a_action_remark,a_m.a_action_type,null,azb.a_add_time,azb.a_opr_user \
		from asset_material a_m, asset_zj_back azb where a_m.a_action_id = azb.id and a_m.a_action_type = 4'
	if startDate:
		sql_4 += ' and azb.a_add_time >= \'{0}\''.format(startDate)
	if endTime:
		sql_4 += ' and azb.a_add_time <= \'{0}\''.format(endTime)

	sql = '{0} union all {1} union all {2} union all {3} union all {4}'.format(sql_0,sql_1,sql_2,sql_3,sql_4)

	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		if rows:
			for row in rows:
				a_action_type = common.getAppleActionType(row[9])
				data.append({
					'a_cd':row[0],'a_type_cd':row[1],'a_fuselage_cd':row[2],'a_main_cd':row[3],
					'a_main_serial':row[4],'a_action_loc':row[5],'a_action_state':row[6],
					'a_action_dept':row[7],'a_action_remark':row[8],'a_action_type': a_action_type,
					'a_action_model':row[10],'a_add_time':str(row[11]),'a_opr_user':row[12]
				});
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

#查询支给数据
def get_zj_data(beginDate,endDate,page,limit):
	count = 0
	data = []
	sql = 'select a_m.a_cd,a_m.a_type_cd,a_m.a_fuselage_cd,a_z.a_main_cd,a_z.a_main_serial, \
		a_z.a_action_state,a_z.a_zj_object,a_z.a_action_remark,a_z.a_opr_user,a_z.a_add_time from \
		asset_material a_m,asset_zj a_z where a_m.a_action_id = a_z.id and a_m.a_action_type = 3'
	sql_count = 'select count(a_m.a_cd) from asset_material a_m,asset_zj a_z \
		where a_m.a_action_id = a_z.id and a_m.a_action_type = 3'

	if beginDate:
		sql += ' and a_z.a_add_time >= \'{0}\''.format(beginDate)
		sql_count += ' and a_z.a_add_time >= \'{0}\''.format(beginDate)

	if endDate:
		sql += ' and a_z.a_add_time <= \'{0}\''.format(endDate)
		sql_count += ' and a_z.a_add_time <= \'{0}\''.format(endDate)

	sql += ' limit {0} offset {1}'.format(limit, limit * (page - 1))

	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		if rows:
			for row in rows:
				data.append({
					'a_cd':row[0],'a_type_cd':row[1],'a_fuselage_cd':row[2],'a_main_cd':row[3],
					'a_main_serial':row[4],'a_action_state':row[5],'a_zj_object':row[6],
					'a_action_remark':row[7],'a_opr_user':row[8],'a_add_time':str(row[9])
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

#获取支给导出数据
def get_zj_export(beginDate,endDate):
	data = []
	sql = 'select a_m.a_cd,a_m.a_type_cd,a_m.a_fuselage_cd,a_z.a_main_cd,a_z.a_main_serial, \
		a_z.a_action_state,a_z.a_zj_object,a_z.a_action_remark,a_z.a_opr_user,a_z.a_add_time from \
		asset_material a_m,asset_zj a_z where a_m.a_action_id = a_z.id and a_m.a_action_type = 3'

	if beginDate:
		sql += ' and a_z.a_add_time >= \'{0}\''.format(beginDate)

	if endDate:
		sql += ' and a_z.a_add_time <= \'{0}\''.format(endDate)

	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		if rows:
			for row in rows:
				data.append({
					'a_cd':row[0],'a_type_cd':row[1],'a_fuselage_cd':row[2],'a_main_cd':row[3],
					'a_main_serial':row[4],'a_action_state':row[5],'a_zj_object':row[6],
					'a_action_remark':row[7],'a_opr_user':row[8],'a_add_time':str(row[9])
				});
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

#退库数据
def get_back_data(beginDate,endDate,page,limit):
	count = 0
	data = []
	sql = 'select a_m.a_cd,a_m.a_type_cd,a_m.a_fuselage_cd,aob.a_main_cd,aob.a_main_serial, \
		aob.a_action_loc,aob.a_action_state,aob.a_back_user,aob.a_confirm_user, \
		aob.a_action_remark,aob.a_opr_user,aob.a_add_time from asset_material a_m, \
		asset_out_back aob where a_m.a_action_id = aob.id and a_m.a_action_type = 2'
	sql_count = 'select count(a_m.a_cd) from asset_material a_m, asset_out_back aob \
		where a_m.a_action_id = aob.id and a_m.a_action_type = 2'
	if beginDate:
		sql += ' and aob.a_add_time >= \'{0}\''.format(beginDate)
		sql_count += ' and aob.a_add_time >= \'{0}\''.format(beginDate)
	if endDate:
		sql += ' and aob.a_add_time <= \'{0}\''.format(endDate)
		sql_count += ' and aob.a_add_time <= \'{0}\''.format(endDate)
	sql += ' limit {0} offset {1}'.format(limit, limit * (page - 1))
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		if rows:
			for row in rows:
				data.append({
					'a_cd':row[0],'a_type_cd':row[1],'a_fuselage_cd':row[2],'a_main_cd':row[3],
					'a_main_serial':row[4],'a_action_loc':row[5],'a_action_state':row[6],
					'a_back_user':row[7],'a_confirm_user':row[8],'a_action_remark':row[9],
					'a_opr_user':row[10],'a_add_time':str(row[11])
				});
		cur.execute(sql_count)
		row = cur.fetchone()
		if row:
			count = row[0]
	except Exception as e:
		raise e
	finally:
		connections[MODEL].cursor()
	return data,count


#支给归还查询
def get_zj_back(beginDate,endDate,page,limit):
	data = []
	count = 0
	sql = 'select a_m.a_cd,a_m.a_type_cd,a_m.a_fuselage_cd,azb.a_main_cd,azb.a_main_serial, \
		azb.a_action_state,azb.a_action_loc,azb.a_action_remark,azb.a_opr_user,azb.a_add_time from \
		asset_material a_m,asset_zj_back azb where a_m.a_action_id = azb.id and a_m.a_action_type = 4 \
		and azb.a_add_time >= \'{0}\' and azb.a_add_time <= \'{1}\''.format(beginDate,endDate)
	sql_count = 'select count(a_m.a_cd) from asset_material a_m,asset_zj_back azb \
		where a_m.a_action_id = azb.id and a_m.a_action_type = 4'
	if beginDate:
		sql += ' and azb.a_add_time >= \'{0}\''.format(beginDate)
		sql_count += ' and azb.a_add_time >= \'{0}\''.format(beginDate)
	if endDate:
		sql += ' and azb.a_add_time <= \'{0}\''.format(endDate)
		sql_count += ' and azb.a_add_time <= \'{0}\''.format(endDate)
	sql += ' limit {0} offset {1}'.format(limit, limit * (page -1))
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		if rows:
			for row in rows:
				data.append({
					'a_cd':row[0],'a_type_cd':row[1],'a_fuselage_cd':row[2],'a_main_cd':row[3],
					'a_main_serial':row[4],'a_action_state':row[5],'a_action_loc':row[6],
					'a_action_remark':row[7],'a_opr_user':row[8],'a_add_time':str(row[9])
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

def zj_back_data(beginDate,endDate):
	sql = 'select a_m.a_cd,a_m.a_type_cd,a_m.a_fuselage_cd,azb.a_main_cd,azb.a_main_serial, \
		azb.a_action_state,azb.a_action_loc,azb.a_action_remark,azb.a_opr_user,azb.a_add_time from \
		asset_material a_m,asset_zj_back azb where a_m.a_action_id = azb.id and a_m.a_action_type = 4 \
		and azb.a_add_time >= \'{0}\' and azb.a_add_time <= \'{1}\''.format(beginDate,endDate)
	if beginDate:
		sql += ' and azb.a_add_time >= \'{0}\''.format(beginDate)
	if endDate:
		sql += ' and azb.a_add_time <= \'{0}\''.format(endDate)
	data = []
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for row in rows:
			data.append({
				'a_cd':row[0],'a_type_cd':row[1],'a_fuselage_cd':row[2],'a_main_cd':row[3],
				'a_main_serial':row[4],'a_action_state':row[5],'a_action_loc':row[6],
				'a_action_remark':row[7],'a_opr_user':row[8],'a_add_time':str(row[9])
			});
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

#查询出库数据
def get_out_data(beginDate,endDate,page,limit):
	data = []
	count = 0
	sql = 'select a_m.a_cd,a_m.a_type_cd,a_m.a_fuselage_cd,a_o.a_main_cd,a_o.a_main_serial, \
		a_o.a_action_state,a_o.a_action_loc,a_o.a_action_remark,a_o.a_take_line,a_o.a_take_user, \
		a_o.a_confirm_user,a_o.a_opr_user,a_o.a_add_time from asset_material a_m,asset_out a_o \
		where a_m.a_action_id = a_o.id and a_m.a_action_type = 1'
	sql_count = 'select count(a_m.a_cd) from asset_material a_m,asset_out a_o \
		where a_m.a_action_id = a_o.id and a_m.a_action_type = 1'
	if beginDate:
		sql += ' and a_o.a_add_time >= \'{0}\''.format(beginDate)
		sql_count += ' and a_o.a_add_time >= \'{0}\''.format(beginDate)
	if endDate:
		sql += ' and a_o.a_add_time <= \'{0}\''.format(endDate)
		sql_count += ' and a_o.a_add_time <= \'{0}\''.format(endDate)
	sql += ' limit {0} offset {1}'.format(limit, limit * (page - 1))
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		if rows:
			for row in rows:
				data.append({
					'a_cd':row[0],'a_type_cd':row[1],'a_fuselage_cd':row[2],'a_main_cd':row[3],
					'a_main_serial':row[4],'a_action_state':row[5],'a_action_loc':row[6],
					'a_action_remark':row[7],'a_take_line':row[8],'a_take_user':row[9],
					'a_confirm_user':row[10],'a_opr_user':row[11],'a_add_time':str(row[12])
				})
		cur.execute(sql_count)
		row = cur.fetchone()
		if row:
			count = row[0]
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data,count

#出库导出
def out_export(beginDate,endDate):
	data = []
	sql = 'select a_m.a_cd,a_m.a_type_cd,a_m.a_fuselage_cd,a_o.a_main_cd,a_o.a_main_serial, \
		a_o.a_action_state,a_o.a_action_loc,a_o.a_action_remark,a_o.a_take_line,a_o.a_take_user, \
		a_o.a_confirm_user,a_o.a_opr_user,a_o.a_add_time from asset_material a_m,asset_out a_o \
		where a_m.a_action_id = a_o.id and a_m.a_action_type = 1'
	if beginDate:
		sql += ' and a_o.a_add_time >= \'{0}\''.format(beginDate)
	if endDate:
		sql += ' and a_o.a_add_time <= \'{0}\''.format(endDate)
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		if rows:
			for row in rows:
				data.append({
					'a_cd':row[0],'a_type_cd':row[1],'a_fuselage_cd':row[2],'a_main_cd':row[3],
					'a_main_serial':row[4],'a_action_state':row[5],'a_action_loc':row[6],
					'a_action_remark':row[7],'a_take_line':row[8],'a_take_user':row[9],
					'a_confirm_user':row[10],'a_opr_user':row[11],'a_add_time':str(row[12])
				});
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

#退库导出
def out_back_export(beginDate,endDate):
	data = []
	sql = 'select a_m.a_cd,a_m.a_type_cd,a_m.a_fuselage_cd,aob.a_main_cd,aob.a_main_serial, \
		aob.a_action_loc,aob.a_action_state,aob.a_back_user,aob.a_confirm_user, \
		aob.a_action_remark,aob.a_opr_user,aob.a_add_time from asset_material a_m, \
		asset_out_back aob where a_m.a_action_id = aob.id and a_m.a_action_type = 2'

	if beginDate:
		sql += ' and aob.a_add_time >= \'{0}\''.format(beginDate)
	if endDate:
		sql += ' and aob.a_add_time <= \'{0}\''.format(endDate)
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for row in rows:
			data.append({
				'a_cd':row[0],'a_type_cd':row[1],'a_fuselage_cd':row[2],'a_main_cd':row[3],
				'a_main_serial':row[4],'a_action_loc':row[5],'a_action_state':row[6],
				'a_back_user':row[7],'a_confirm_user':row[8],'a_action_remark':row[9],
				'a_opr_user':row[10],'a_add_time':str(row[11])
			});
	except Exception as e:
		raise e
	finally:
		connections[MODEL].cursor()
	return data

#历史记录查询
def get_history_data(a_cd):
	data = []
	sql_0 = 'select a_cd,a_main_cd,a_main_serial,a_loc_cd,a_state,a_dept_cd,a_opr_user,a_add_time, \
		\'入库\',null from asset_material where a_cd = \'{0}\''.format(a_cd)

	sql_1 = 'select a_m.a_cd,a_o.a_main_cd,a_o.a_main_serial,a_o.a_action_loc,a_o.a_action_state,a_o.a_action_dept, \
		a_o.a_opr_user,a_o.a_add_time,\'出库\',null from asset_material a_m,asset_out a_o \
		where a_m.a_cd = \'{0}\' and a_m.a_action_type = {1} and a_m.a_cd = a_o.a_cd'.format(a_cd,1)

	sql_2 = 'select a_m.a_cd,aob.a_main_cd,aob.a_main_serial,aob.a_action_loc,aob.a_action_state,aob.a_action_dept, \
		aob.a_opr_user,aob.a_add_time,\'退库\',aob.a_origin_loc from asset_material a_m,asset_out_back aob \
		where a_m.a_cd = \'{0}\' and a_m.a_action_type = {1} and a_m.a_cd = aob.a_cd'.format(a_cd,2)

	sql_3 = 'select a_m.a_cd,zj.a_main_cd,zj.a_main_serial,zj.a_zj_object,zj.a_action_state, \
		zj.a_zj_dept,zj.a_opr_user,zj.a_add_time,\'支给\',null from asset_material a_m,asset_zj zj \
		where a_m.a_cd = \'{0}\' and a_m.a_action_type = {1} and a_m.a_cd = zj.a_cd'.format(a_cd,3)

	sql_4 = 'select a_m.a_cd,azb.a_main_cd,azb.a_main_serial,azb.a_action_loc,azb.a_action_state,azb.a_action_dept, \
		azb.a_opr_user,azb.a_add_time,\'支给归还\',null from asset_material a_m,asset_zj_back azb \
		where a_m.a_cd = \'{0}\' and a_m.a_action_type = {1} and a_m.a_cd = azb.a_cd'.format(a_cd,4)

	sql = '{0} union all {1} union all {2} union all {3} union all {4} order by a_add_time'.format(sql_0,sql_1,sql_2,sql_3,sql_4)

	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for row in rows:
			a_action_type = row[8]
			data.append({
				'a_cd':row[0],'a_main_cd':row[1],'a_main_serial':row[2],'a_action_loc':row[3],'a_action_state':row[4],
				'a_action_dept':row[5],'a_opr_user':row[6],'a_add_time':str(row[7]),'a_action_type':a_action_type,
				'a_origin_loc':row[9]
			})
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data