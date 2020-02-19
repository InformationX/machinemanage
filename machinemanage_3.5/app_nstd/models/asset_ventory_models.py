# -*- coding:utf-8 -*-
from django.db import connections,transaction
import datetime

global MODEL
MODEL = 'asset_nstd'

#在线盘点批次查询
def getVenBat(beginDate,endDate,b_inven_type):
	data = []
	try:
		cur = connections[MODEL].cursor()
		if beginDate and endDate:
			sql = 'select b_id,b_location,b_match,b_noscanned,b_surplus,b_datetime,b_user_name \
				from asset_inven_batch where b_datetime >= \'{0}\' and b_datetime <= \'{1}\' \
				and b_inven_type = \'{2}\''.format(beginDate,endDate,b_inven_type)
		else:
			sql = 'select b_id,b_location,b_match,b_noscanned,b_surplus,b_datetime,b_user_name \
				from asset_inven_batch where b_inven_type = \'{0}\''.format(b_inven_type)
		cur.execute(sql)
		rows = cur.fetchall()
		if rows:
			for row in rows:
				b_total = row[2] + row[3]				
				data.append({
					'b_id':row[0],'b_location':row[1],'b_total':b_total,'b_match':row[2],
					'b_noscanned':row[3],'b_surplus':row[4],'b_datetime':str(row[5]),'b_user_name':row[6]
				});
	except Exception as e:
		raise e
	finally:
		connections[MODEL].cursor()
	return data

#导出在线盘点数据
def VenExport(b_id):
	data = []
	try:
		sql = 'select aib.b_location,ai.i_cd,am.a_name,am.a_type_cd,ai.i_status,aib.b_user_name,aib.b_datetime \
			from asset_inven_batch aib,asset_inventory ai,asset_material am where \
			aib.b_id = ai.b_id and ai.i_cd = am.a_cd and aib.b_id = \'{0}\''.format(b_id)
		cur = connections[MODEL].cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		if rows:
			for row in rows:
				i_status = row[4]
				if i_status == '0':
					i_status = '匹配资产'
				elif i_status == '1':
					i_status = '未扫描资产'
				elif i_status == '2':
					i_status = '多余资产'
				data.append({
					'b_location':row[0],'i_cd':row[1],'i_status':i_status,'a_name':row[2],
					'a_type_cd':row[3],'b_user_name':row[5],'b_datetime':row[6]
				});
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return data

#删除在线盘点数据
def delVen(b_id):
	result = False
	try:
		cur = connections[MODEL].cursor()
		with transaction.atomic(using=MODEL):
			sql1 = 'delete from asset_inven_batch where b_id = {0}'.format(b_id)
			cur.execute(sql1)
			if cur.rowcount == 1:
				sql2 = 'delete from asset_inventory where b_id = {0}'.format(b_id)
				cur.execute(sql2)
				if cur.rowcount > 0:
					result = True
	except Exception as e:
		raise e
	finally:
		connections[MODEL].close()
	return result