# -*- coding:utf-8 -*-

from django.urls import path
from app_nstd.views import asset_nstd_views
from app_nstd.views import asset_basefunc_views
from app_nstd.views import asset_general_views
from app_nstd.views import asset_baseinfo_views
from app_nstd.views import asset_calculate_views
from app_nstd.views import asset_manage_views
from app_nstd.views import asset_ventory_views
from app_nstd.views import asset_edit_views
#from app_nstd.views import asset_print_views

urlpatterns = [
    path('', asset_nstd_views.index),                                   #主界面
    path('logout', asset_nstd_views.logout),                            #资产注销
    path('login', asset_nstd_views.login),                              #登录
    path('login_page', asset_nstd_views.login_page),                    #登录页面
    path('user_manage', asset_nstd_views.user_manage),                  #用户管理
    path('upd_passwd_page', asset_nstd_views.upd_passwd_page),          #修改密码页面
    path('upd_passwd', asset_nstd_views.upd_passwd),                    #修改密码
    path('authority_page', asset_nstd_views.authority_page),            #权限修改

    path('manage/getUser', asset_manage_views.getUser),                 #用户查询
    path('manage/userUpdate', asset_manage_views.userUpdate),           #更新用户
    path('manage/userDelete', asset_manage_views.userDelete),           #用户删除
    path('manage/userAdd', asset_manage_views.userAdd),                 #添加用户
    path('manage/updateAuthority', asset_manage_views.updateAuthority), #修改权限
    path('manage/getAuthority', asset_manage_views.getAuthority),       #查询权限

    #基本功能
    path('basefunc/asset_add_page', asset_nstd_views.asset_add_page),
    path('basefunc/asset_out_page', asset_nstd_views.asset_out_page),
    path('basefunc/asset_zj_page', asset_nstd_views.asset_zj_page),
    path('basefunc/asset_zj_revert_page', asset_nstd_views.asset_zj_revert_page),
    path('basefunc/asset_loan_revert_page', asset_nstd_views.asset_loan_revert_page),
    path('basefunc/asset_back_page', asset_nstd_views.asset_back_page),
    path('basefunc/asset_sale_page', asset_nstd_views.asset_sale_page),
    path('basefunc/asset_scrap_page', asset_nstd_views.asset_scrap_page),
    path('basefunc/asset_online_move_page', asset_nstd_views.asset_online_move_page),
    path('basefunc/asset_instorage_move_page', asset_nstd_views.asset_instorage_move_page),

    path('basefunc/asset_add', asset_basefunc_views.asset_add),                     #设备添加
    path('basefunc/action_zj', asset_basefunc_views.action_zj),                     #支给设备
    path('basefunc/before_zj_detail', asset_basefunc_views.before_zj_detail),       #支给前搜索
    path('basefunc/before_action_vde', asset_basefunc_views.before_action_vde),     #验证资产状态
    path('basefunc/get_zj_detail', asset_basefunc_views.get_zj_detail),             #支给归还前搜索
    path('basefunc/revert_zj', asset_basefunc_views.revert_zj),                     #支给归还

    path('basefunc/get_out_detail', asset_basefunc_views.get_out_detail),           #出库记账前查询
    path('basefunc/before_out_vde', asset_basefunc_views.before_out_vde),           #资产出库前验证
    path('basefunc/asset_out', asset_basefunc_views.asset_out),                     #资产出库

    path('basefunc/get_back_detail', asset_basefunc_views.get_back_detail),         #退库记账前查询
    path('basefunc/before_back_vde', asset_basefunc_views.before_back_vde),         #资产退库前验证
    path('basefunc/asset_back', asset_basefunc_views.asset_back),                   #资产退库

    path('basefunc/loan_revert_detail', asset_basefunc_views.loan_revert_detail),   #借用归还前查看详情
    path('basefunc/loan_revert', asset_basefunc_views.loan_revert),                 #设备借用归还(还给供应商)

    path('basefunc/get_sale_detail', asset_basefunc_views.get_sale_detail),         #查询销售详情
    path('basefunc/asset_sale', asset_basefunc_views.asset_sale),                   #设备销售记账

    path('basefunc/asset_scrap', asset_basefunc_views.asset_scrap),                 #资产报废记账
    path('basefunc/asset_move_detail', asset_basefunc_views.asset_move_detail),     #移动前查看
    path('basefunc/asset_move', asset_basefunc_views.asset_move),                   #资产批量移动
    path('basefunc/asset_instorage_move', asset_basefunc_views.asset_instorage_move),#资产库房移动

    #综合查询
    path('general/add_search_page', asset_general_views.add_search_page),
    path('general/sale_search', asset_nstd_views.sale_search),                      #销售查询页面
    path('general/get_sale_data', asset_general_views.get_sale_data),               #获取销售数据
    path('general/move_search_page', asset_nstd_views.move_search_page),            #获取移动数据
    path('general/get_scrap_data', asset_general_views.get_scrap_data),             #获取报废数据
    
    path('general/total_search', asset_nstd_views.total_search),                    #总账信息查询
    path('general/in_storage_search', asset_nstd_views.in_storage_search),          #在库信息查询
    path('general/on_line_search', asset_nstd_views.on_line_search),                #在线信息查询
    path('general/zj_search_page', asset_general_views.zj_search_page),             #获取支给信息
    path('general/zj_revert_page', asset_nstd_views.zj_revert_page),                #支给归还页面
    path('general/scrap_search', asset_nstd_views.scrap_search),                    #资产报废页面
    path('general/out_storage_search', asset_nstd_views.out_storage_search),        #设备出库查询
    path('general/back_storage_search', asset_nstd_views.back_storage_search),      #设备退库查询
    path('general/loan_revert_search', asset_nstd_views.loan_revert_search),        #借用归还查询

    path('general/get_out_storage_data', asset_general_views.get_out_storage_data), #出库查询
    path('general/get_back_storage_data', asset_general_views.get_back_storage_data),#退库查询
    path('general/get_add_data', asset_general_views.get_add_data),                 #获取添加数据
    path('general/get_zj_data', asset_general_views.get_zj_data),                   #获取支给数据
    path('general/get_zj_revert_data', asset_general_views.get_zj_revert_data),     #支给归还数据
    path('general/get_loan_revert_data', asset_general_views.get_loan_revert_data), #借用归还数据
    path('general/get_move_data', asset_general_views.get_move_data),               #获取移动数据 
    path('general/get_in_storage_data', asset_general_views.get_in_storage_data),   #获取在库数据
    path('general/get_online_data', asset_general_views.get_online_data),           #获取在线数据
    path('general/get_history_data', asset_general_views.get_history_data),         #获取历史记录

    path('general/instorage_export', asset_general_views.instorage_export),         #导出在库数据
    path('general/online_export', asset_general_views.online_export),               #导出在线数据
    path('general/scrap_export', asset_general_views.scrap_export),                 #导出报废数据
    path('general/sale_export', asset_general_views.sale_export),                   #导出销售数据
    path('general/zj_export', asset_general_views.zj_export),                       #导出支给数据
    path('general/add_export', asset_general_views.add_export),                     #入库数据导出
    path('general/out_export', asset_general_views.out_export),                     #出库数据导出
    path('general/back_export', asset_general_views.back_export),                   #退库数据导出
    path('general/loan_revert_export', asset_general_views.loan_revert_export),     #借用归还导出
    path('general/zj_revert_export', asset_general_views.zj_revert_export),         #支给归还导出
    path('general/move_export', asset_general_views.move_export),                   #移动信息导出
    path('general/total_export', asset_general_views.total_export),                 #总账信息导出
    path('general/opr_his_search', asset_general_views.opr_his_search),             #操作记录查询
    path('general/history_export', asset_general_views.history_export),             #操作记录导出
    
    #基本信息设置
    path('baseinfo/asset_pos_page', asset_nstd_views.asset_pos_page),
    path('baseinfo/get_pos_data', asset_baseinfo_views.get_pos_data),            #位置数据(分页)
    path('baseinfo/get_all_pos_data', asset_baseinfo_views.get_all_pos_data),    #位置数据(不分页)
    path('baseinfo/add_pos', asset_baseinfo_views.add_pos),
    path('baseinfo/asset_pos_del', asset_baseinfo_views.asset_pos_del),          #位置删除
    path('baseinfo/depart_page/', asset_nstd_views.depart_page),                 #部门管理
    path('baseinfo/add_depart', asset_baseinfo_views.add_depart),                #添加部门
    path('baseinfo/search_depart', asset_baseinfo_views.search_depart),          #搜素部门
    path('baseinfo/edit_depart', asset_baseinfo_views.edit_depart),              #编辑部门
    path('baseinfo/del_depart', asset_baseinfo_views.del_depart),                #删除部门
    path('baseinfo/edit_pos', asset_baseinfo_views.edit_pos),                    #编辑位置
    path('baseinfo/add_supplier', asset_baseinfo_views.add_supplier),            #添加供应商
    path('baseinfo/search_supplier', asset_baseinfo_views.search_supplier),      #搜索供应商
    path('baseinfo/search_category', asset_baseinfo_views.search_category),      #搜索资产类别
    path('baseinfo/add_category', asset_baseinfo_views.add_category),            #添加资产类别
    path('baseinfo/add_action_user', asset_baseinfo_views.add_action_user),      #添加领用人员
    path('baseinfo/search_action_user', asset_baseinfo_views.search_action_user),#添加领用人员
    path('baseinfo/search_action_charge', asset_baseinfo_views.search_action_charge),#搜索主管
    path('baseinfo/add_action_charge', asset_baseinfo_views.add_action_charge),  #搜索主管
    path('baseinfo/search_client', asset_baseinfo_views.search_client),          #搜索客户
    path('baseinfo/add_client', asset_baseinfo_views.add_client),                #添加客户
    path('baseinfo/search_pos', asset_baseinfo_views.search_pos),                #搜索位置
    path('baseinfo/get_asset_detail', asset_baseinfo_views.get_asset_detail),    #查询资产详情
    path('baseinfo/asset_update_page', asset_nstd_views.asset_update_page),      #修改资产界面
    path('baseinfo/mobile_model_page', asset_nstd_views.mobile_model_page),      #手持移动机种
    path('baseinfo/asset_convert_page', asset_baseinfo_views.asset_convert_page),#资产转换页面
    path('baseinfo/asset_update', asset_baseinfo_views.asset_update),            #资产更新
    path('baseinfo/get_mobile_model', asset_baseinfo_views.get_mobile_model),    #获取使用机种
    path('baseinfo/add_action_model', asset_baseinfo_views.add_action_model),    #添加使用机种
    path('baseinfo/action_model_del', asset_baseinfo_views.action_model_del),    #删除使用机种

    path('baseinfo/edit_base_page', asset_baseinfo_views.edit_base_page),        #基础页面
    path('baseinfo/edit_out_page', asset_baseinfo_views.edit_out_page),          #出库页面
    path('baseinfo/edit_back_page', asset_baseinfo_views.edit_back_page),        #退库页面
    path('baseinfo/edit_zj_page', asset_baseinfo_views.edit_zj_page),            #支给页面
    path('baseinfo/edit_zj_back_page', asset_baseinfo_views.edit_zj_back_page),  #支给归还页面
    path('baseinfo/edit_loan_back_page', asset_baseinfo_views.edit_loan_back_page),#借用归还
    path('baseinfo/edit_storage_move_page', asset_baseinfo_views.edit_storage_move_page),#内部移动
    path('baseinfo/edit_online_move_page', asset_baseinfo_views.edit_online_move_page),#在线移动
    path('baseinfo/edit_pos_page', asset_baseinfo_views.edit_pos_page),          #位置代码
    path('baseinfo/edit_state_page', asset_baseinfo_views.edit_state_page),      #修改状态页面
    path('baseinfo/edit_category_page', asset_baseinfo_views.edit_category_page),#修改折旧类别
    path('baseinfo/edit_depart_page', asset_baseinfo_views.edit_depart_page),    #修改当前部门

    #资产转换前查询
    path('baseinfo/before_convert_detail', asset_baseinfo_views.before_convert_detail),
    path('baseinfo/is_a_cd_repeat', asset_baseinfo_views.is_a_cd_repeat),           #资产番号是否重复
    path('baseinfo/asset_convert', asset_baseinfo_views.asset_convert),             #资产转换
    path('baseinfo/get_modify_csv_data', asset_baseinfo_views.get_modify_csv_data), #获取资产修改数据
    path('baseinfo/upload_modify', asset_baseinfo_views.upload_modify),          #资产更新

    #批量修改资产位置前查询
    path('baseinfo/get_modify_1_csv_data', asset_baseinfo_views.get_modify_1_csv_data),
    path('baseinfo/upload_modify_1', asset_baseinfo_views.upload_modify_1),      #批量修改资产位置

    path('baseinfo/get_modify_2_csv_data', asset_baseinfo_views.get_modify_2_csv_data),#资产冲消
    path('baseinfo/upload_modify_2', asset_baseinfo_views.upload_modify_2),
    
    path('baseinfo/get_modify_3_csv_data', asset_baseinfo_views.get_modify_3_csv_data),
    path('baseinfo/upload_modify_3', asset_baseinfo_views.upload_modify_3),

    path('baseinfo/get_modify_4_csv_data', asset_baseinfo_views.get_modify_4_csv_data),#修改资产状态、折旧分类
    path('baseinfo/upload_modify_4', asset_baseinfo_views.upload_modify_4),

    path('basefunc/download_template', asset_basefunc_views.download_template),  #下载添加模板
    path('basefunc/upload_file', asset_basefunc_views.upload_file),              #上传文件保存
    path('basefunc/upload_table_page', asset_basefunc_views.upload_table_page),  #显示上传数据表格页面

    path('basefunc/get_add_csv_data', asset_basefunc_views.get_add_csv_data),    #读取添加csv数据
    path('basefunc/upload_add', asset_basefunc_views.upload_add),                #上传资产添加数据

    path('basefunc/get_out_csv_data',asset_basefunc_views.get_out_csv_data),     #添加资产出库数据
    path('basefunc/upload_out', asset_basefunc_views.upload_out),                #资产批量出库

    path('basefunc/get_back_csv_data', asset_basefunc_views.get_back_csv_data),  #添加资产退库数据
    path('basefunc/upload_back', asset_basefunc_views.upload_back),              #资产批量退库

    path('basefunc/get_zj_csv_data', asset_basefunc_views.get_zj_csv_data),      #读取支给CSV数据
    path('basefunc/upload_zj', asset_basefunc_views.upload_zj),                  #资产批量支给

    #读取转换CSV数据
    path('basefunc/get_convert_csv_data', asset_basefunc_views.get_convert_csv_data),
    path('baseinfo/upload_convert', asset_baseinfo_views.upload_convert),        #资产批量转换

    #读取在线资产设备数据
    path('basefunc/get_add_out_csv_data', asset_basefunc_views.get_add_out_csv_data),
    path('basefunc/upload_add_out', asset_basefunc_views.upload_add_out),        #在线设备导入

    #读取在库设备数据
    path('basefunc/get_add_instorage_csv_data', asset_basefunc_views.get_add_instorage_csv_data),
    path('basefunc/upload_add_instorage', asset_basefunc_views.upload_add_instorage),#导入在库数据

    #读取支给归还CSV数据
    path('basefunc/get_zj_revert_csv_data', asset_basefunc_views.get_zj_revert_csv_data),
    path('basefunc/upload_zj_revert', asset_basefunc_views.upload_zj_revert),    #支给资产批量归还

    #读取借用归还CSV数据
    path('basefunc/get_loan_revert_csv_data', asset_basefunc_views.get_loan_revert_csv_data),
    path('basefunc/upload_loan_revert', asset_basefunc_views.upload_loan_revert),#借用设备批量归还

    path('basefunc/get_sale_csv_data', asset_basefunc_views.get_sale_csv_data),  #读取销售CSV数据
    path('basefunc/upload_sale', asset_basefunc_views.upload_sale),              #资产批量销售

    path('basefunc/get_scrap_csv_data', asset_basefunc_views.get_scrap_csv_data),#读取报废CSV数据
    path('basefunc/upload_scrap', asset_basefunc_views.upload_scrap),            #资产批量报废

    #读取库房CSV移动数据
    path('basefunc/get_instorage_move_data', asset_basefunc_views.get_instorage_move_data),
    #库房设备批量移动
    path('basefunc/upload_instorage_move', asset_basefunc_views.upload_instorage_move),
    #读取移动CSV数据
    path('basefunc/get_online_move_data', asset_basefunc_views.get_online_move_data),
    #在线批量移动
    path('basefunc/upload_online_move', asset_basefunc_views.upload_online_move),

    path('calculate/cal_confirm_page', asset_nstd_views.cal_confirm_page),       #资产计量确认界面
    path('calculate/cal_search_page', asset_nstd_views.cal_search_page),         #资产计量查询页面
    path('calculate/cal_import_page', asset_nstd_views.cal_import_page),         #资产计量导入界面
    path('calculate/cal_record_page', asset_nstd_views.cal_record_page),         #计量记录查询界面
    path('calculate/cal_update_page', asset_nstd_views.cal_update_page),         #资产计量修改界面

    path('calculate/cal_upload_add', asset_calculate_views.cal_upload_add),      #批量添加计量数据
    path('calculate/get_is_need_cal', asset_calculate_views.get_is_need_cal),    #确认是否需要计量
    path('calculate/confirmToCal', asset_calculate_views.confirmToCal),          #资产计量确认

    path('calculate/get_cal_csv_data', asset_calculate_views.get_cal_csv_data),  #读取计量CSV数据
    path('calculate/get_cal_data', asset_calculate_views.get_cal_data),          #获取计量数据
    path('calculate/cal_export', asset_calculate_views.cal_export),              #计量信息导出
    path('calculate/get_cal_record', asset_calculate_views.get_cal_record),      #获取计量记录
    path('calculate/cal_update_detail', asset_calculate_views.cal_update_detail),#计量更改前查询
    path('calculate/cal_update', asset_calculate_views.cal_update),              #修改计量数据

    path('ventory/online_ventory', asset_nstd_views.online_ventory),             #在库盘点页
    path('ventory/instorage_ventory', asset_nstd_views.instorage_ventory),       #在库盘点页
    path('ventory/getVenBat', asset_ventory_views.getVenBat),                    #盘点批次数据
    path('ventory/VenExport', asset_ventory_views.VenExport),                    #在线盘点导出
    path('ventory/delVen', asset_ventory_views.delVen),                          #删除盘点数据

    #path('print/asset_print_page', asset_print_views.print_page),                #打印页
    #path('print/get_print_asset', asset_print_views.get_print_asset),            #获取打印资产信息

    path('edit/get_edit_base', asset_edit_views.get_edit_base),         #基础信息查询
    path('edit/edit_base', asset_edit_views.edit_base),                 #修改基础信息
    path('edit/get_edit_out', asset_edit_views.get_edit_out),           #出库信息查询
    path('edit/edit_out', asset_edit_views.edit_out),                   #修改出库信息
    path('edit/get_edit_back', asset_edit_views.get_edit_back),         #退库信息查询
    path('edit/edit_back', asset_edit_views.edit_back),                 #修改退库信息
    path('edit/get_edit_zj', asset_edit_views.get_edit_zj),             #支给信息查询
    path('edit/edit_zj', asset_edit_views.edit_zj),                     #修改支给信息
    path('edit/get_edit_zj_back', asset_edit_views.get_edit_zj_back),   #支给归还信息
    path('edit/edit_zj_back', asset_edit_views.edit_zj_back),           #修改支给归还
    path('edit/get_edit_loan_back', asset_edit_views.get_edit_loan_back),#借用归还查询
    path('edit/edit_loan_back', asset_edit_views.edit_loan_back),       #借用归还
    path('edit/get_edit_storage_move', asset_edit_views.get_edit_storage_move),#内部移动
    path('edit/edit_storage_move', asset_edit_views.edit_storage_move), #内部移动
    path('edit/get_edit_online_move', asset_edit_views.get_edit_online_move),#在线移动信息
    path('edit/edit_online_move', asset_edit_views.edit_online_move),   #修改在线移动
    path('edit/get_edit_loc', asset_edit_views.get_edit_loc),           #资产位置信息
    path('edit/edit_loc', asset_edit_views.edit_loc),                   #修改位置
    path('edit/get_edit_state', asset_edit_views.get_edit_state),       #资产状态信息
    path('edit/edit_state', asset_edit_views.edit_state),               #修改资产状态
    path('edit/get_edit_category', asset_edit_views.get_edit_category), #折旧类别信息
    path('edit/edit_category', asset_edit_views.edit_category),         #修改折旧类别
    path('edit/get_edit_depart', asset_edit_views.get_edit_depart),     #资产所在部门
    path('edit/edit_depart', asset_edit_views.edit_depart),             #编辑资产部门
]
