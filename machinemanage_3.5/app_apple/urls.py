# -*- coding:utf-8 -*-

from django.urls import path
from app_apple.views import asset_apple_views
from app_apple.views import asset_basefunc_views
from app_apple.views import asset_general_views
from app_apple.views import asset_file_views
from app_apple.views import asset_baseinfo_views

urlpatterns = [
	path('', asset_apple_views.index),
    path('index/', asset_apple_views.index),
    path('main/', asset_apple_views.main),

    #账户管理
    path('logout', asset_apple_views.logout),                                      #账户注销

    #基本功能
    path('login_page/', asset_apple_views.login_page),                             #跳转登陆页面
    path('login/', asset_apple_views.login),                                       #登陆操作
    path('basic/', asset_apple_views.basic),

    path('download_template', asset_file_views.download_template),                 #模板下载
    path('uploadfile', asset_file_views.uploadfile),                               #保存上传Excel文档
    path('upload_table_page', asset_file_views.upload_table_page),                 #跳转上传数据页
    path('get_add_csv_data', asset_file_views.get_add_csv_data),                   #读取上传文件数据
    path('get_zj_csv_data', asset_file_views.get_zj_csv_data),
    path('get_zj_revert_csv_data', asset_file_views.get_zj_revert_csv_data),
    path('get_out_csv_data', asset_file_views.get_out_csv_data),         
    path('get_out_back_csv_data', asset_file_views.get_out_back_csv_data),
    path('get_edit_loc_data', asset_file_views.get_edit_loc_data),               

    path('basefunc/asset_add_page/', asset_apple_views.asset_add_page),            #资产添加页面
    path('basefunc/asset_zj_page/', asset_apple_views.asset_zj_page),              #资产支给页面
    path('basefunc/zj_revert_page/', asset_apple_views.zj_revert_page),            #支给归还页面
    path('basefunc/asset_out_page/', asset_apple_views.asset_out_page),            #资产出库页面
    path('basefunc/asset_back_page/', asset_apple_views.asset_back_page),          #资产退库页面
    path('basefunc/asset_loan_page/', asset_apple_views.asset_loan_page),          #资产借出页面
    path('basefunc/asset_revert_page/', asset_apple_views.asset_revert_page),      #资产归还页面
    path('basefunc/asset_scrap_page/', asset_apple_views.asset_scrap_page),        #资产报废页面
    path('basefunc/asset_add', asset_basefunc_views.asset_add),                    #资产添加
    path('basefunc/upload_add', asset_basefunc_views.upload_add),                  #资产批量上传
    path('basefunc/upload_zj', asset_basefunc_views.upload_zj),                    #资产批量支给
    path('basefunc/get_detail', asset_basefunc_views.get_detail),                  #支给上传前查询
    #path('basefunc/get_out_data', asset_basefunc_views.get_out_data),             #出库数据
    path('basefunc/upload_out', asset_basefunc_views.upload_out),                  #批量出库
    path('basefunc/upload_excel_zj', asset_basefunc_views.upload_excel_zj),
    path('basefunc/upload_excel_out', asset_basefunc_views.upload_excel_out),      #批量出库（Excel）
    path('basefunc/upload_excel_zj_revert', asset_basefunc_views.upload_excel_zj_revert),
    path('basefunc/upload_excel_out_back', asset_basefunc_views.upload_excel_out_back),
    path('basefunc/upload_edit_loc', asset_basefunc_views.upload_edit_loc),

    path('basefunc/asset_out_detail', asset_basefunc_views.asset_out_detail),      #资产出库详情
    path('basefunc/asset_out_single', asset_basefunc_views.asset_out_single),      #资产单个退库

    path('basefunc/zj_revert_detail', asset_basefunc_views.zj_revert_detail),      #只给归还前查询
    path('basefunc/zj_back', asset_basefunc_views.zj_back),                        #支给归还

    path('basefunc/upload_out_back', asset_basefunc_views.upload_out_back),        #资产退库

    #综合查询
    path('general/total_search', asset_apple_views.total_search),                  #总账查询页面
    path('general/history_search', asset_apple_views.history_search),              
    path('general/in_storage_search', asset_apple_views.in_storage_search),        #在库查询页面
    path('general/zj_search', asset_apple_views.zj_search),                        #支给查询页面
    path('general/out_storage_search', asset_apple_views.out_storage_search),      #出库查询页面
    path('general/zj_back_search', asset_apple_views.zj_back_search),              #支给归还页面
    path('general/add_search', asset_apple_views.add_search),                      #添加查询页面
    path('general/online_search', asset_apple_views.online_search),                #在线查询页面
    path('general/revert_search', asset_apple_views.revert_search),                #归还信息页面
    path('general/back_search', asset_apple_views.back_search),                    #退库信息页面
    
    path('general/total_export', asset_general_views.total_export),                #总账信息导出
    path('general/get_history_data', asset_general_views.get_history_data),        #历史记录查询
    path('general/get_storage_data', asset_general_views.get_storage_data),        #获取在库数据
    path('general/get_zj_data', asset_general_views.get_zj_data),                  #获取支给数据
    path('general/get_zj_back', asset_general_views.get_zj_back),                  #获取借出数据
    path('general/get_add_data', asset_general_views.get_add_data),                #获取添加数据
    path('general/get_online_data', asset_general_views.get_online_data),          #获取在线数据
    path('general/get_out_data', asset_general_views.get_out_data),                #获取出库数据
    path('general/get_back_data', asset_general_views.get_back_data),              #获取退库数据

    path('general/storage_export', asset_general_views.storage_export),            #在库批量导出
    path('general/zj_export', asset_general_views.zj_export),                      #支给导出

    path('general/zj_back_export', asset_general_views.zj_back_export),            #支给归还导出

    path('general/out_export', asset_general_views.out_export),                    #出库导出
    path('general/out_back_export', asset_general_views.out_back_export),          #退库导出

    #基本信息设置
    path('baseinfo/department/', asset_apple_views.department),                    #部门管理
    path('baseinfo/add_depart', asset_apple_views.add_depart),                     #添加部门
    path('baseinfo/search_depart', asset_apple_views.search_depart),               #搜素部门
    path('baseinfo/edit_depart', asset_apple_views.edit_depart),                   #编辑部门
    path('baseinfo/del_depart', asset_apple_views.del_depart),                     #删除部门

    path('baseinfo/asset_pos_page', asset_apple_views.asset_pos_page),             #存放位置管理
    path('baseinfo/get_all_pos_data', asset_apple_views.get_all_pos_data),         #获取所有存放数据
    path('baseinfo/add_pos', asset_apple_views.add_pos),                           #添加资产存放位置
    path('baseinfo/del_pos', asset_apple_views.del_pos),                           #删除存放位置
    path('baseinfo/update_pos', asset_apple_views.update_pos),                     #修改存储位置

    path('baseinfo/asset_edit_page/', asset_apple_views.asset_edit_page),          #资产变更页面
    path('baseinfo/edit', asset_apple_views.edit_detail),                          #编辑页面详情

    path('baseinfo/get_base_detail', asset_baseinfo_views.get_base_detail),        #查询基础信息
    path('baseinfo/edit_base', asset_baseinfo_views.edit_base),                    #编辑基础信息
    path('baseinfo/get_out_detail', asset_baseinfo_views.get_out_detail),          #查询出库详情
    path('baseinfo/edit_out', asset_baseinfo_views.edit_out),                      #编辑出库信息
    path('baseinfo/get_out_back', asset_baseinfo_views.get_out_back),              #资产退库详情
    path('baseinfo/edit_out_back', asset_baseinfo_views.edit_out_back),            #编辑退库信息
    path('baseinfo/get_zj_detail', asset_baseinfo_views.get_zj_detail),            #查询支给详情
    path('baseinfo/edit_zj', asset_baseinfo_views.edit_zj),                        #查询支给详情
    path('baseinfo/get_zj_back', asset_baseinfo_views.get_zj_back),                #查询支给归还
    path('baseinfo/edit_zj_back', asset_baseinfo_views.edit_zj_back),              #编辑支给归还
]
