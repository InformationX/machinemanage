# -*- coding:utf-8 -*-
from django.db import connections
from app_apple.models import asset_tools
import json,datetime
from config.models import common

global MODEL
MODEL = 'asset_b'

#支给前查询
def get_detail(assetList):
	data = []
	try:
		cur = connections[MODEL].cursor()
		'''
		sql = 'select a_m.a_cd,a_m.a_type_cd,a_m.a_fuselage_cd,a_z.a_main_cd, \
			a_z.a_main_serial,a_z.a_zj_object, a_z.a_action_state,a_z.a_action_remark, \
			a_z.a_opr_user,a_z.a_add_time,a_m.a_action_type from asset_material a_m left join \
			asset_zj a_z on a_m.a_action_id = a_z.id where a_m.a_cd in ('
		for index,a_cd in enumerate(assetList):
			if index < len(assetList) - 1:
				sql += '\'{0}\','.format(a_cd)
			else:
				sql += '\'{0}\''.format(a_cd)
		sql += ')'
		cur.execute(sql)
		rows = cur.fetchall()
		for row in rows:
			data.append({
				'a_cd':row[0],'a_type_cd':row[1],'a_fuselage_cd':row[2],'a_main_cd':row[3],
				'a_main_serial':row[4],'a_zj_object':row[5],'a_action_state':row[6],
				'a_action_remark':row[7],'a_opr_user':row[8],'a_add_time':str(row[9]),
				'a_action_type': common.getAppleActionType(row[10])
			});
		'''

		str = '('
		for index,a_cd in enumerate(assetList):
			if index < len(assetList) - 1:
				str += '\'{0}\','.format(a_cd)
			else:
				str += '\'{0}\''.format(a_cd)
		str += ')'

		#在库
		sql_0 = 'select a_cd,a_type_cd,a_fuselage_cd,a_loc_cd,a_state,a_main_cd,a_main_serial, \
			a_action_type,a_remark from asset_material where a_cd in {0} and a_action_type = 0'.format(str)

		#出库
		sql_1 = 'select a_m.a_cd,a_m.a_type_cd,a_m.a_fuselage_cd,a_o.a_action_loc,a_o.a_action_state,\
			a_o.a_main_cd,a_o.a_main_serial,a_m.a_action_type,a_o.a_action_remark from asset_material a_m,asset_out a_o \
			where a_m.a_action_id = a_o.id and a_m.a_cd in {0} and a_m.a_action_type = 1'.format(str)

		#退库
		sql_2 = 'select a_m.a_cd,a_m.a_type_cd,a_m.a_fuselage_cd,aob.a_action_loc,aob.a_action_state,\
			aob.a_main_cd,aob.a_main_serial,a_m.a_action_type,aob.a_action_remark from asset_material a_m,asset_out_back aob \
			where a_m.a_action_id = aob.id and a_m.a_cd in {0} and a_m.a_action_type = 2'.format(str)

		#支给
		sql_3 = 'select a_m.a_cd,a_m.a_type_cd,a_m.a_fuselage_cd,a_z.a_zj_object,a_z.a_action_state,\
			a_z.a_main_cd,a_z.a_main_serial,a_m.a_action_type,a_z.a_action_remark from asset_material a_m,asset_zj a_z \
			where a_m.a_action_id = a_z.id and a_m.a_cd in {0} and a_m.a_action_type = 3'.format(str)

		#支给归还
		sql_4 = 'select a_m.a_cd,a_m.a_type_cd,a_m.a_fuselage_cd,azb.a_action_loc,azb.a_action_state,\
			azb.a_main_cd,azb.a_main_serial,a_m.a_action_type,azb.a_action_remark \
			from asset_material a_m, asset_zj_back azb \
			where a_m.a_action_id = azb.id and a_m.a_cd in {0} and a_m.a_action_type = 4'.format(str)

		sql = sql_0 + ' union all ' + sql_1 + ' union all ' + sql_2 + ' union all ' + sql_3 + ' union all ' + sql_4
		cur.execute(sql)
		rows = cur.fetchall()
		for row in rows:
			a_action_type = row[7]
			if a_action_type == 3:
				a_zj_object = row[3]
				a_action_loc = ''
			else:
				a_zj_object = ''
				a_action_loc = row[3]

			if a_action_type == 0 or a_action_type == 2 or a_action_type == 4:	#在库
				a_current_loc = a_action_loc
				a_action_loc = ''
			else:
				a_current_loc = ''
				
			data.append({
				'a_cd':row[0],'a_type_cd':row[1],'a_fuselage_cd':row[2],
				'a_current_loc':a_current_loc,'a_action_loc':a_action_loc,
				'a_action_state':row[4],'a_main_cd':row[5],'a_main_serial':row[6],
				'a_zj_object':a_zj_object,'a_action_type':common.getAppleActionType(row[7])
			});

		'''
		for a_cd in a_cd_list:
			sql = 'select a_type_cd,a_fuselage_cd,a_loc_cd,a_state,a_main_cd,a_main_serial, \
				a_action_type from asset_material where a_cd = \'{0}\''.format(a_cd)
			cur.execute(sql)
			row = cur.fetchone()
			if row:
				a_action_type = asset_tools.trans_action_type(row[6])
				tmp_dict = {
					'a_cd':a_cd,'a_type_cd':row[0],'a_fuselage_cd':row[1],'a_action_loc':row[2],
					'a_action_state':row[3],'a_main_cd':row[4],'a_main_serial':row[5],
					'a_action_type':a_action_type
				}
			else:
				tmp_dict = {
					'a_cd':a_cd,'a_type_cd':'','a_fuselage_cd':'','a_action_loc':'',
					'a_action_state':'','a_main_cd':'','a_main_serial':'','a_action_type':'未入库'
				}
			data.append(tmp_dict)
		'''

	except Exception as e:
		raise e
	finally:
		cur.close()
		connections[MODEL].close()
	return data