# -*- coding:utf-8 -*-
from django.db import connections,transaction
import datetime

global MODEL
MODEL = 'asset_nstd'

def get_is_need_cal(a_cd):
	data = {'result':False}
	try:
		sql = 'select a_id,a_type_cd,a_name,a_self_cd,a_fuselage_cd,a_need_cal \
			from asset_material where a_cd = \'{0}\''.format(a_cd)
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		row = cur.fetchone()
		if row:
			data = {
				'a_material_id':row[0],'a_type_cd':row[1],'a_name':row[2],
				'a_self_cd':row[3],'a_fuselage_cd':row[4],'a_need_cal':row[5],'result':True
			}
		else:
			data['msg'] = '资产番号:{0}未入库!'.format(a_cd)
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

def confirmToCal(a_material_id,a_need_cal):
	result = False
	try:
		sql = 'update asset_material set a_need_cal = {0} where a_id = \'{1}\''.format(a_need_cal,a_material_id)
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		if cur.rowcount == 1:
			result = True
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return result

#批量上传计量数据
def cal_upload__add(table_data,c_opr_user,c_record_time):
	num = 0
	try:
		with transaction.atomic(using="asset_nstd"):
			cur = connections[MODEL].cursor()
			for one in table_data:
				sql1 = 'insert into asset_calculate(c_method,c_date,c_end_date,c_material_id,c_use_depart, \
					c_status,c_certificate,c_opr_user,c_record_time) \
					values(\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\',\'{8}\') \
					'.format(one['c_method'],one['c_date'],one['c_end_date'],one['c_material_id'],
						one['c_use_depart'],one['c_status'],one['c_certificate'],c_opr_user,c_record_time)
				cur.execute(sql1)
				if cur.rowcount == 1:
					sql2 = 'select c_id from asset_calculate where c_material_id = \'{0}\' \
						and c_record_time = \'{1}\''.format(one['c_material_id'],c_record_time)
					cur.execute(sql2)
					row =cur.fetchone()
					if row:
						c_id = row[0]
						sql3 = 'update asset_material set a_cal_id = \'{0}\' where a_id = \'{1}\''.format(c_id,one['c_material_id'])
						cur.execute(sql3)
						if cur.rowcount == 1:
							num += 1
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return num

#计量信息查询
def get_cal_data(a_cd,a_type_cd,c_date,c_end_date,c_certificate):
	data = []
	count = 0
	sql1 = 'select a_m.a_cd,a_m.a_type_cd,a_m.a_name,a_m.a_self_cd,a_m.a_fuselage_cd, \
		a_c.c_method,a_c.c_date,a_c.c_end_date,a_c.c_record_time,\'IDLE\', \
		a_c.c_status,a_c.c_certificate from asset_material a_m,asset_calculate a_c \
		where a_m.a_cal_id = a_c.c_id and a_m.a_need_cal = 1 and a_m.a_action_id = 0 \
		and a_c.c_status <> \'NG\' '

	sql2 = 'select a_m.a_cd,a_m.a_type_cd,a_m.a_name,a_m.a_self_cd,a_m.a_fuselage_cd, \
		null,null,null,null,a_a.a_action_depart,null,null \
		from asset_material a_m,asset_action a_a \
		where a_m.a_cal_id = 0 and a_m.a_action_id = a_a.a_id \
		and a_m.a_need_cal = 1 and a_a.a_action_type not in (3,6,7)'

	sql3 = 'select a_m.a_cd,a_m.a_type_cd,a_m.a_name,a_m.a_self_cd,a_m.a_fuselage_cd, \
		a_c.c_method,a_c.c_date,a_c.c_end_date,a_c.c_record_time,a_a.a_action_depart, \
		a_c.c_status,a_c.c_certificate from asset_material a_m,asset_calculate a_c, \
		asset_action a_a where a_m.a_cal_id = a_c.c_id and a_m.a_action_id = a_a.a_id \
		and a_m.a_need_cal = 1 and a_c.c_status <> \'NG\' \
		and a_a.a_action_type not in (3,6,7)'

	if a_cd:
		sql1 += ' and a_m.a_cd = \'{0}\''.format(a_cd)
		sql2 += ' and a_m.a_cd = \'{0}\''.format(a_cd)
		sql3 += ' and a_m.a_cd = \'{0}\''.format(a_cd)
	if a_type_cd:
		sql1 += ' and a_m.a_type_cd = \'{0}\''.format(a_type_cd)
		sql2 += ' and a_m.a_type_cd = \'{0}\''.format(a_type_cd)
		sql3 += ' and a_m.a_type_cd = \'{0}\''.format(a_type_cd)
	if c_date:
		sql1 += ' and to_char(a_c.c_date,\'yyyy-MM\') = \'{0}\''.format(c_date)
		sql3 += ' and to_char(a_c.c_date,\'yyyy-MM\') = \'{0}\''.format(c_date)
	if c_end_date:
		sql1 += ' and to_char(a_c.c_end_date,\'yyyy-MM\') = \'{0}\''.format(c_end_date)
		sql3 += ' and to_char(a_c.c_end_date,\'yyyy-MM\') = \'{0}\''.format(c_end_date)
	if c_certificate:
		sql1 += ' and a_c.c_certificate = \'{0}\''.format(c_certificate)
		sql3 += ' and a_c.c_certificate = \'{0}\''.format(c_certificate)

	sql = '{0} union all {1} union all {2}'.format(sql1,sql2,sql3)

	with open('C:\\Users\\admin\\Desktop\\hehe.txt','w') as fp:
		fp.write(sql)

	try:
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()

		if rows:
			for row in rows:
				if row[6]:
					c_date = str(row[6])[0:10]
				else:
					c_date = ''
				if row[7]:
					c_end_date = str(row[7])[0:10]
				else:
					c_end_date = ''
				row_dict = {
					'a_cd':row[0],'a_type_cd':row[1],'a_name':row[2],'a_self_cd':row[3],
					'a_fuselage_cd':row[4].split('.')[0],'c_method':row[5],'c_date':c_date,
					'c_end_date':c_end_date,'c_record_time':str(row[8]),
					'a_action_depart':row[9],'c_status':row[10],'c_certificate':row[11]
				}
				data.append(row_dict)
			count = len(data)
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data,count

#根据资产番号查询计量详情
def get_cal_record(a_cd):
	data = []
	try:
		sql = 'select a_m.a_cd,a_m.a_type_cd,a_m.a_name,a_m.a_self_cd,a_m.a_fuselage_cd, \
			a_c.c_method,a_c.c_date,a_c.c_end_date,a_c.c_use_depart,a_c.c_status, \
			a_c.c_certificate,a_c.c_record_time from asset_material a_m,asset_calculate a_c \
			where a_m.a_id = a_c.c_material_id and a_m.a_cd = \'{0}\''.format(a_cd)
		sql += 'order by a_c.c_record_time desc'
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		if rows:
			for row in rows:
				data.append({
					'a_cd':row[0],'a_type_cd':row[1],'a_name':row[2],'a_self_cd':row[3],'a_fuselage_cd':row[4],
					'c_method':row[5],'c_date':str(row[6]),'c_end_date':str(row[7]),'c_use_depart':row[8],
					'c_status':row[9],'c_certificate':row[10],'c_record_time':str(row[11])
				})
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

#计量前搜索详情
def cal_update_detail(a_cd):
	data = {'result':False}
	try:
		sql = 'select a_m.a_type_cd,a_m.a_name,a_m.a_self_cd,a_m.a_fuselage_cd, \
			a_c.c_id,a_c.c_method,a_c.c_date,a_c.c_end_date,a_c.c_use_depart, \
			a_c.c_status,a_c.c_certificate from asset_material a_m,asset_calculate a_c \
			where a_m.a_cal_id = a_c.c_id and a_m.a_cd = \'{0}\''.format(a_cd)
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		row = cur.fetchone()
		if row:
			data = {
				'a_type_cd':row[0],'a_name':row[1],'a_self_cd':row[2],'a_fuselage_cd':row[3],
				'c_id':row[4],'c_method':row[5],'c_date':str(row[6]),'c_end_date':str(row[7]),
				'c_use_depart':row[8],'c_status':row[9],'c_certificate':row[10],'result':True
			}
		else:
			data['msg'] = '未搜索到数据'
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

#添加计量信息
def cal_update(c_id,c_method,c_date,c_end_date,c_use_depart,c_status,c_certificate,a_cd,a_fuselage_cd):
	result = False
	try:
		with transaction.atomic(using="asset_nstd"):
			cur = connections[MODEL].cursor()
			sql1 = 'update asset_material set a_fuselage_cd = \'{0}\' where a_cd = \'{1}\''.format(a_fuselage_cd,a_cd)
			cur.execute(sql1)
			if cur.rowcount == 1:
				sql = 'update asset_calculate set c_method = \'{0}\',c_date = \'{1}\',c_end_date = \'{2}\',\
					c_use_depart = \'{3}\',c_status = \'{4}\',c_certificate = \'{5}\' where c_id = \'{6}\' \
					'.format(c_method,c_date,c_end_date,c_use_depart,c_status,c_certificate,c_id)
				cur.execute(sql)
				if cur.rowcount == 1:
					result = True
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return result