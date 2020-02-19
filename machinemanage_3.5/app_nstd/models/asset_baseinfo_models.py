# -*- coding:utf-8 -*-
from django.db import connections,transaction
from config.models import common
import datetime

global MODEL
MODEL = 'asset_nstd'

#添加资产位置
def add_pos(p_building,p_floor,p_area,p_column,p_position,p_code):
	sql = 'insert into asset_pos(p_building,p_floor,p_area,p_column,p_position,p_code) values(\'{0}\', \
		\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\')'.format(p_building,p_floor,p_area,p_column,p_position,p_code)
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

#获取所有资产位置(分页情况)
def get_pos_data(page,limit):
	offset = limit * (page - 1)
	sql = 'select p_id,p_building,p_floor,p_area,p_column,p_position,p_code \
		from asset_pos order by p_id desc limit {0} offset {1}'.format(limit,offset)
	lenSql = 'select count(p_id) from asset_pos'
	data = []
	count = 0
	try:
		cur = connections[MODEL].cursor()

		cur.execute(lenSql)
		row = cur.fetchone()
		if row:
			count = row[0]

		cur.execute(sql)
		rows = cur.fetchall()
		for index,row in enumerate(rows):
			p_id,p_building,p_floor,p_area,p_column,p_position,p_code = row
			data.append({
				'index':index + 1,'p_id':p_id,'p_building':p_building,'p_floor':p_floor,
				'p_area':p_area,'p_column':p_column,'p_position':p_position,'p_code':p_code
			})
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	return data,count

#获取所有资产位置(不分页情况)
def get_all_pos_data():
	sql = 'select p_id,p_building,p_floor,p_area,p_column,p_position,p_code \
		from asset_pos order by p_id desc'
	data = []
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for index,row in enumerate(rows):
			p_id,p_building,p_floor,p_area,p_column,p_position,p_code = row
			data.append({
				'index':index + 1,'p_id':p_id,'p_building':p_building,'p_floor':p_floor,
				'p_area':p_area,'p_column':p_column,'p_position':p_position,'p_code':p_code
			})
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

#删除资产位置
def asset_pos_del(p_id):
	sql = 'delete from asset_pos where p_id = \'{0}\''.format(p_id)
	result = False
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		if cur.rowcount == 1:
			result = True
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return result

#添加部门
def add_depart(d_id,d_name):
	sql = 'insert into depart(d_pid,d_name) values(\'{0}\',\'{1}\')'.format(d_id,d_name)
	result = False
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		result = True
		connections[MODEL].commit()
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
			depart_list.append({'id':d_id,'pid':d_pid,'d_name':d_name,'name':d_name})
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

#编辑位置信息
def edit_pos(p_id,edit_p_building,edit_p_floor,edit_p_area,edit_p_column,edit_p_position,edit_p_code):
	sql = 'update asset_pos set p_building = \'{0}\',p_floor = \'{1}\',p_area = \'{2}\', \
		p_column = \'{3}\',p_position = \'{4}\',p_code = \'{5}\' where p_id = \'{6}\' \
		'.format(edit_p_building,edit_p_floor,edit_p_area,edit_p_column,edit_p_position,edit_p_code,p_id)
	result = False
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		if cur.rowcount == 1:
			result = True
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return result

#添加供应商
def add_supplier(a_supplier):
	sql = 'insert into asset_supplier(s_name) values(\'{0}\')'.format(a_supplier)
	result = False
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		if cur.rowcount:
			result = True
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return result

#搜索供应商
def search_supplier():
	sql = 'select s_id,s_name from asset_supplier'
	data_list = []
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for row in rows:
			s_id,s_name = row
			data_list.append({
				'id':s_id,'name':s_name
			})
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data_list

#添加资产类别
def add_category(a_category):
	sql = 'insert into asset_category(c_name) values(\'{0}\')'.format(a_category)
	result = False
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		if cur.rowcount == 1:
			result = True
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return result

#搜索资产类别
def search_category():
	sql = 'select c_id,c_name from asset_category'
	data_list = []
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for row in rows:
			c_id,c_name = row
			data_list.append({
				'id':c_id,'name':c_name
			})
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data_list

def add_action_user(u_name):
	sql = 'insert into asset_action_user(u_name) values(\'{0}\')'.format(u_name)
	result = False
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		if cur.rowcount == 1:
			result = True
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return result

#搜索领用人员
def search_action_user():
	sql = 'select u_id,u_name from asset_action_user'
	data_list = []
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for row in rows:
			u_id,u_name = row
			data_list.append({
				'id':u_id,'name':u_name
			})
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data_list

#添加主管人员
def add_action_charge(c_name):
	sql = 'insert into asset_action_charge(c_name) values(\'{0}\')'.format(c_name)
	result = False
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		if cur.rowcount == 1:
			result = True
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return result

#搜索主管人员
def search_action_charge():
	sql = 'select c_id,c_name from asset_action_charge'
	data_list = []
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for row in rows:
			u_id,u_name = row
			data_list.append({
				'id':u_id,'name':u_name
			})
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data_list

def search_pos(pos_type):
	if pos_type == 'instorage':	#库房移动
		sql = 'select p_id,p_code from asset_pos where p_code like \'W%\' or p_code like \'w%\''
	elif pos_type == 'online':	#在线移动
		sql = 'select p_id,p_code from asset_pos where p_code like \'F%\' or p_code like \'f%\''
	data_list = []
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for row in rows:
			p_id,p_name = row
			data_list.append({
				'id':p_id,'name':p_name	
			})
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data_list

#搜索销售客户
def search_client():
	sql = 'select c_id,c_name from asset_client'
	data_list = []
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for row in rows:
			u_id,u_name = row
			data_list.append({
				'id':u_id,'name':u_name
			})
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data_list

#添加销售客户
def add_client(c_name):
	sql = 'insert into asset_client(c_name) values(\'{0}\')'.format(c_name)
	result = False
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		if cur.rowcount == 1:
			result = True
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return result

#资产转换前详情查询
def before_convert_detail(a_origin_cd):
	sql = 'select a_action_id,a_id from asset_material where a_cd = \'{0}\''.format(a_origin_cd)
	data = {'result':False}
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		row = cur.fetchone()
		if row:
			a_action_id,a_id = row
			if a_action_id == 0:
				sql2 = 'select a_self_cd,a_name,a_type_cd,a_loc_cd,a_status,a_price,a_amount,a_currency, \
					a_brand,a_category,a_project_cd,a_out_time,a_purchase_time,a_model,a_budget, \
					a_referendum,a_po_cd,a_sap_cd,a_depart,a_action_id,a_fuselage_cd \
					from asset_material where a_id = \'{0}\''.format(a_id)
			else:
				sql2 = 'select a_m.a_self_cd,a_m.a_name,a_m.a_type_cd,a_a.a_action_loc,a_a.a_action_state, \
					a_m.a_price,a_m.a_amount,a_m.a_currency,a_m.a_brand,a_m.a_category,a_m.a_project_cd, \
					a_m.a_out_time,a_m.a_purchase_time,a_m.a_model,a_m.a_budget,a_m.a_referendum,a_m.a_po_cd, \
					a_m.a_sap_cd,a_m.a_depart,a_a.a_action_type,a_m.a_fuselage_cd from asset_material a_m, \
					asset_action a_a where a_m.a_action_id = a_a.a_id and a_m.a_id = \'{0}\''.format(a_id)
			cur.execute(sql2)
			row = cur.fetchone()
			if row:
				a_type_cd = row[19]
				if a_type_cd == 0 or a_type_cd == 2 or a_type_cd == 4 or a_type_cd == 9:
					a_type_cd = '在库'
				elif a_type_cd == 1:
					a_type_cd = '支给'
				elif a_type_cd == 3:
					a_type_cd = '已归还供应商'
				elif a_type_cd == 5 or a_type_cd == 8:
					a_type_cd = '已出库'
				elif a_type_cd == 6:
					a_type_cd = '已销售'
				elif a_type_cd == 7:
					a_type_cd = '已报废'

				data = {
					'a_self_cd':row[0],'a_name':row[1],'a_type_cd':row[2],'a_action_loc':row[3],'a_action_state':row[4],
					'a_price':row[5],'a_amount':row[6],'a_currency':row[7],'a_brand':row[8],'a_category':row[9],
					'a_project_cd':row[10],'a_out_time':str(row[11])[0:10],'a_purchase_time':str(row[12])[0:10],
					'a_model':row[13],'a_budget':row[14],'a_referendum':row[15],'a_po_cd':row[16],'a_sap_cd':row[17],
					'a_depart':row[18],'a_action_type':a_type_cd,'a_fuselage_cd':row[20],
					'a_material_id':a_id,'a_action_id':a_action_id,'result':True
				}
				print(a_action_id)
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

#验证资产番号是否重复
def is_a_cd_repeat(a_cd):
	result = True	#默认验证通过
	sql = 'select a_cd from asset_material where a_cd = \'{0}\' or a_origin_cd = \'{0}\''.format(a_cd)
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		row = cur.fetchone()
		if row:
			result = False
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return result

#资产转换
'''
def asset_convert(a_action_id,a_material_id,a_origin_cd,a_cd,a_opr_user,a_record_time):
	result = False
	a_action_type = 10
	try:
		with transaction.atomic(using=MODEL):
			cur = connections[MODEL].cursor()
			if a_action_id == '0':
				sql = 'select a_loc_cd,a_status,a_category from asset_material where a_cd = \'{0}\''.format(a_origin_cd)
				cur.execute(sql)
				row = cur.fetchone()
				if row:
					a_action_loc,a_action_state,a_action_category = row
					sql = 'insert into asset_action(a_cd,a_origin_cd,a_action_loc,a_action_state,a_action_category,a_material_id,a_action_type, \
						a_opr_user,a_record_time) values (\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\',\'{8}\') returning a_id \
						'.format(a_cd,a_origin_cd,a_action_loc,a_action_state,a_action_category,a_material_id,a_action_type,a_opr_user,a_record_time)
					cur.execute(sql)
					if cur.rowcount == 1:
						a_action_id = cur.fetchone()[0]
						sql = 'update asset_material set a_cd = \'{0}\',a_action_id = {1} where a_id = {2}'.format(a_cd,a_action_id,a_material_id)
						cur.execute(sql)
						if cur.rowcount == 1:
							result = True
			else:
				sql = 'select a_a.a_action_loc,a_a.a_action_state,a_a.a_action_category,a_a.a_origin_depart, \
					a_a.a_origin_loc,a_a.a_action_charge,a_a.a_action_model,a_a.a_action_user,a_a.a_action_depart, \
					a_a.a_action_remark,a_a.a_action_supplier from asset_material a_m,asset_action a_a \
					where a_m.a_action_id = a_a.a_id and a_m.a_cd = \'{0}\''.format(a_origin_cd)
				cur.execute(sql)
				row = cur.fetchone()
				if row:
					sql = 'insert into asset_action(a_cd,a_action_loc,a_action_state,a_action_category,a_origin_depart, \
						a_origin_loc,a_action_charge,a_action_model,a_action_user,a_action_depart,a_action_remark, \
						a_action_supplier,a_origin_cd,a_material_id,a_action_type,a_opr_user,a_record_time) values \
						(\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\',\'{8}\',\'{9}\',\'{10}\',\'{11}\',\'{12}\',\'{13}\',\'{14}\',\'{15}\',\'{16}\') returning a_id \
						'.format(a_cd,row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],a_origin_cd,a_material_id,a_action_type,a_opr_user,a_record_time)
					cur.execute(sql)
					if cur.rowcount == 1:
						a_action_id = cur.fetchone()[0]
						sql = 'update asset_material set a_cd = \'{0}\',a_action_id = {1} where a_id = {2}'.format(a_cd,a_action_id,a_material_id)
						cur.execute(sql)
						if cur.rowcount == 1:
							result = True
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return result
'''

#资产转换(插入asset_operation表)
#def asset_convert(a_action_id,a_material_id,a_origin_cd,a_cd,a_opr_user,a_record_time):
def asset_convert(a_material_id,a_origin_cd,a_cd,a_opr_user,a_record_time):
	result = False
	a_action_type = 10
	try:
		with transaction.atomic(using=MODEL):
			cur = connections[MODEL].cursor()
			sql = 'insert into asset_operation(a_action_type,a_material_id,a_origin_cd,a_cd,a_opr_user,a_record_time) \
				values ({0},{1},\'{2}\',\'{3}\',\'{4}\',\'{5}\') \
				'.format(a_action_type,a_material_id,a_origin_cd,a_cd,a_opr_user,a_record_time)
			cur.execute(sql)
			if cur.rowcount == 1:
				sql = 'update asset_material set a_cd = \'{0}\' where a_id = {1}'.format(a_cd,a_material_id)
				cur.execute(sql)
				if cur.rowcount == 1:
					result = True
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return result

def get_asset_detail(a_cd):
	data = {'result':False}
	sql = 'select a_id,a_type_cd,a_name,a_self_cd,a_fuselage_cd,a_project_cd, \
		a_category,a_action_id,a_status,a_loc_cd,a_po_cd,a_referendum,a_funds_type,a_model, \
		a_supplier,a_depart,a_remark from asset_material where a_cd = \'{0}\''.format(a_cd)
	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		row = cur.fetchone()
		if row:
			data = {
				'a_material_id':row[0],'a_type_cd':row[1],'a_name':row[2],'a_self_cd':row[3],
				'a_fuselage_cd':row[4],'a_project_cd':row[5],'a_action_category':row[6],
				'a_action_id':row[7],'a_action_state':row[8],'a_action_loc':row[9],
				'a_po_cd':row[10],'a_referendum':row[11],'a_funds_type':row[12],'a_model':row[13],
				'a_supplier':row[14],'a_action_depart':row[15],'a_action_remark':row[16],'result':True
			}
			if row[7] == 0:
				data['a_action_type'] = '在库',
			else:
				sql = 'select a_a.a_action_type,a_a.a_action_state,a_a.a_action_loc,a_a.a_action_depart, \
					a_a.a_action_category,a_a.a_action_remark from asset_material a_m,asset_action a_a \
					where a_m.a_action_id = a_a.a_id and a_m.a_cd = \'{0}\''.format(a_cd)
				cur.execute(sql)
				row = cur.fetchone()
				if row:
					data['a_action_type'] = common.get_action_type(row[0])
					data['a_action_state'] = row[1]
					data['a_action_loc'] = row[2]
					data['a_action_depart'] = row[3]
					data['a_action_category'] = row[4]
					data['a_action_remark'] = row[5]
		else:
			data['msg'] = '未搜索到数据!'
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

#资产信息修改
def asset_update(a_material_id,a_action_id,a_type_cd,a_name,a_self_cd,a_fuselage_cd,
	a_project_cd,a_action_category,a_action_state,a_action_loc,a_po_cd,a_referendum,
		a_funds_type,a_model,a_supplier,a_action_depart,a_action_remark):
	result = False
	sql = 'update asset_material set a_type_cd = \'{0}\',a_name = \'{1}\',a_self_cd = \'{2}\', \
		a_fuselage_cd = \'{3}\',a_project_cd = \'{4}\',a_po_cd = \'{5}\',a_referendum=\'{6}\', \
		a_funds_type=\'{7}\',a_model=\'{8}\',a_supplier=\'{9}\' where a_id = \'{10}\' \
		'.format(a_type_cd,a_name,a_self_cd,a_fuselage_cd,a_project_cd,a_po_cd,a_referendum,a_funds_type,a_model,a_supplier,a_material_id)
	try:
		with transaction.atomic(using=MODEL):
			cur = connections[MODEL].cursor()
			cur.execute(sql)
			if cur.rowcount == 1:
				if int(a_action_id) == 0:
					sql1 = 'update asset_material set a_status = \'{0}\',a_loc_cd = \'{1}\', \
						a_depart = \'{2}\', a_category = \'{3}\', a_remark = \'{4}\' where a_id = \'{5}\' \
						'.format(a_action_state,a_action_loc,a_action_depart,a_action_category,a_action_remark,a_material_id)
				else:
					sql1 = 'update asset_action set a_action_state = \'{0}\', a_action_loc = \'{1}\', a_action_depart = \'{2}\' \
						,a_action_category = \'{3}\', a_action_remark = \'{4}\' where a_id = \'{5}\' \
						'.format(a_action_state,a_action_loc,a_action_depart,a_action_category,a_action_remark,a_action_id)
				cur.execute(sql1)
				if cur.rowcount == 1:
					result = True
	except Exception as e:
		print(e)
	finally:
		connections[MODEL].close()
	return result

#资产批量修改
def upload_modify(table_data):
	num = 0
	try:
		cur = connections[MODEL].cursor()
		with transaction.atomic(using=MODEL):
			for item in table_data:
				a_cd,a_category,a_action_state,a_action_loc,a_action_id = item
				if int(a_action_id) == 0:
					sql = 'update asset_material set a_category = \'{0}\',a_status = \'{1}\',a_loc_cd = \'{2}\' \
						where a_cd = \'{3}\''.format(a_category,a_action_state,a_action_loc,a_cd)
					cur.execute(sql)
					if cur.rowcount == 1:
						num += 1
				else:
					sql1 = 'update asset_material set a_category = \'{0}\' where a_cd = \'{1}\''.format(a_category,a_cd)
					cur.execute(sql1)
					if cur.rowcount == 1:
						sql2 = 'update asset_action set a_action_state = \'{0}\',a_action_loc = \'{1}\' \
							where a_id = \'{2}\''.format(a_action_state,a_action_loc,a_action_id)
						cur.execute(sql2)
						if cur.rowcount == 1:
							num += 1
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return num

#批量修改资产位置
def upload_modify_1(table_data):
	num = 0
	try:
		cur = connections[MODEL].cursor()
		with transaction.atomic(using=MODEL):
			for item in table_data:
				a_cd,a_action_depart,a_action_loc,a_action_model,a_action_remark,a_action_id = item
				if int(a_action_id) == 0:
					sql = 'update asset_material set a_depart=\'{0}\',a_loc_cd = \'{1}\',a_remark = \'{2}\' \
						where a_cd = \'{3}\''.format(a_action_depart,a_action_loc,a_action_remark,a_cd)
				else:
					sql = 'update asset_action set a_action_depart=\'{0}\',a_action_loc = \'{1}\', \
						a_action_model = \'{2}\',a_action_remark = \'{3}\' where a_id = \'{4}\' \
						'.format(a_action_depart,a_action_loc,a_action_model,a_action_remark,a_action_id)
				cur.execute(sql)
				if cur.rowcount == 1:
					num += 1
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return num

#资产批量冲消
def upload_modify_2(table_data):
	num = 0
	try:
		cur = connections[MODEL].cursor()
		with transaction.atomic(using=MODEL):
			for item in table_data:
				a_cd, = item
				sql1 = 'delete from asset_action where a_cd = \'{0}\''.format(a_cd)
				cur.execute(sql1)
				sql2 = 'delete from asset_material where a_cd = \'{0}\''.format(a_cd)
				cur.execute(sql2)
				num += 1
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return num

#资产批量修改价格、币种
def upload_modify_3(table_data):
	num = 0
	try:
		cur = connections[MODEL].cursor()
		with transaction.atomic(using=MODEL):
			for item in table_data:
				a_cd,a_price,a_currency = item
				sql = 'update asset_material set a_price=\'{0}\',a_currency=\'{1}\' \
					where a_cd = \'{2}\''.format(a_price,a_currency,a_cd)
				cur.execute(sql)
				print(cur.rowcount)
				if cur.rowcount != 0:
					num += 1
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return num

#资产批量修改资产状态、资产类别
def upload_modify_4(table_data):
	num = 0
	try:
		cur = connections[MODEL].cursor()
		with transaction.atomic(using=MODEL):
			for item in table_data:
				a_cd,a_action_state,a_action_category = item['a_cd'],item['a_action_state'],item['a_action_category']
				sql1 = 'select a_action_id from asset_material where a_cd = \'{0}\''.format(a_cd)
				cur.execute(sql1)
				row = cur.fetchone()
				if row:
					a_action_id = row[0]
					if a_action_id == 0:
						sql2 = 'update asset_material set a_status = \'{0}\', a_category = \'{1}\' \
							where a_cd = \'{2}\''.format(a_action_state,a_action_category,a_cd)
					else:
						sql2 = 'update asset_action set a_action_state = \'{0}\', a_action_category = \'{1}\' \
							where a_id = \'{2}\''.format(a_action_state,a_action_category,a_action_id)
					cur.execute(sql2)
					if cur.rowcount == 1:
						num += 1
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return num

#批量转换资产(修改资产番号)
def upload_convert(table_data,a_action_type,a_opr_user,a_record_time):
	num = 0
	try:
		cur = connections[MODEL].cursor()
		with transaction.atomic(using=MODEL):
			for item in table_data:
				a_origin_cd,a_cd,a_material_id = item
				sql = 'insert into asset_operation(a_action_type,a_material_id,a_origin_cd,a_cd,a_opr_user,a_record_time) \
					values ({0},{1},\'{2}\',\'{3}\',\'{4}\',\'{5}\') \
					'.format(a_action_type,a_material_id,a_origin_cd,a_cd,a_opr_user,a_record_time)
				cur.execute(sql)
				if cur.rowcount == 1:
					sql = 'update asset_material set a_cd = \'{0}\' where a_id = {1}'.format(a_cd,a_material_id)
					cur.execute(sql)
					if cur.rowcount == 1:
						num += 1
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return num

#获取所有使用机种
def get_mobile_model():
	data = []
	try:
		cur = connections[MODEL].cursor()
		sql = 'select m_id,m_model,opr_user,add_time from asset_model'
		cur.execute(sql)
		rows = cur.fetchall()
		if rows:
			for row in rows:
				data.append({
					'm_id':row[0],'m_model':row[1],'opr_user':row[2],'add_time':str(row[3])
				})
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

#添加机种
def add_action_model(a_action_model,opr_user,add_time):
	result = False
	try:
		cur = connections[MODEL].cursor()
		sql = 'insert into asset_model(m_model,opr_user,add_time) \
			values (\'{0}\',\'{1}\',\'{2}\')'.format(a_action_model,opr_user,add_time)
		cur.execute(sql)
		if cur.rowcount == 1:
			result = True
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return result

#删除使用机种
def action_model_del(m_id):
	result = False
	try:
		cur = connections[MODEL].cursor()
		sql = 'delete from asset_model where m_id = {0}'.format(m_id)
		cur.execute(sql)
		if cur.rowcount == 1:
			result = True
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return result