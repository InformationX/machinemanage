# -*- coding:utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,StreamingHttpResponse
from wsgiref.util import FileWrapper
from urllib import parse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from machinemanage.settings import MEDIA_ROOT
from app_apple.models import asset_tools
import json,os,datetime,mimetypes,xlrd

#添加资产模板下载
def download_template(request):
    param = request.GET.get('param')
    if param == 'add':
        param = '小苹果录入模板'
    elif param == 'zj':
        param = '小苹果支给模板'
    elif param == 'out':
        param = '小苹果出库模板'
    elif param == 'zj_revert':
        param = '小苹果支给归还模板'
    elif param == 'out_back':
        param = '小苹果退库模板'
    elif param == 'edit_loc':
        param = '小苹果修改资产位置模板'
    the_file = 'app_apple/templatefolder/{0}.xlsm'.format(param)
    chunk_size = 8192
    response = StreamingHttpResponse(FileWrapper(open(the_file, 'rb'), chunk_size),
            content_type=mimetypes.guess_type(the_file)[0])
    response['Content-Length'] = os.path.getsize(the_file)
    response['Content-Disposition'] = "attachment; filename="+parse.quote(param)+".xlsm"
    return response

#保存上传文件
def uploadfile(request):
    result = False
    try:
        file = request.FILES.get('file')
        save_path = os.path.join(MEDIA_ROOT,'tmp_folder')
        file_path = os.path.join(save_path,file.name).replace('\\','/')
        path = default_storage.save(file_path, ContentFile(file.read()))
        tmp_file = os.path.join(MEDIA_ROOT, path)   #存储临时文件目录及文件名
        result = True
    except Exception as e:
        print(e)
    return HttpResponse(json.dumps({'result':result,'tmp_file':tmp_file}))

#跳转上传数据页
def upload_table_page(request):
    opr_type = request.GET.get('opr_type')
    tmp_file = request.GET.get('tmp_file')
    if opr_type == 'add':
        return render(request,'apple/uploadtable/upload_add.html',{'tmp_file':tmp_file})
    elif opr_type == 'zj':
        return render(request,'apple/uploadtable/upload_zj.html',{'tmp_file':tmp_file})
    elif opr_type == 'out':
        return render(request,'apple/uploadtable/upload_out.html',{'tmp_file':tmp_file})
    elif opr_type == 'zj_revert':
        return render(request,'apple/uploadtable/upload_zj_revert.html',{'tmp_file':tmp_file})
    elif opr_type == 'out_back':
        return render(request,'apple/uploadtable/upload_out_back.html',{'tmp_file':tmp_file})
    elif opr_type == 'edit_loc':
        return render(request,'apple/uploadtable/upload_edit_loc.html',{'tmp_file':tmp_file})

#读取上传的Excel文件中的数据
def get_add_csv_data(request):
    tmp_file = request.GET.get('tmp_file')
    data = {"code":0,"msg":"","count":0,'data':[]}
    if tmp_file:
        workbook = xlrd.open_workbook(tmp_file)
        allsheets = workbook.sheets()
        if allsheets:
            sheet = allsheets[0]
            row_number = sheet.nrows
            for i in range(row_number):
                if i > 1:
                    row_dict = {}
                    row_dict['index'] = i - 1
                    a_cd = str(sheet.cell(i,0).value).split('.')[0]
                    if a_cd:
                        row_dict['a_cd'] = a_cd
                        row_dict['a_type_cd'] = str(sheet.cell(i,1).value).split('.')[0]
                        row_dict['a_fuselage_cd'] = str(sheet.cell(i,2).value).split('.')[0]
                        row_dict['a_main_cd'] = str(sheet.cell(i,3).value).split('.')[0]      #主体资产号
                        row_dict['a_main_serial'] = str(sheet.cell(i,4).value).split('.')[0]  #主体序列号
                        row_dict['a_dept_cd'] = str(sheet.cell(i,5).value).split('.')[0]
                        row_dict['a_loc_cd'] = str(sheet.cell(i,6).value).split('.')[0]
                        row_dict['a_state'] = str(sheet.cell(i,7).value).split('.')[0]
                        row_dict['a_remark'] = str(sheet.cell(i,8).value).split('.')[0]
                        row_dict['a_action_type'] = asset_tools.get_detail(a_cd)
                        data['data'].append(row_dict)
        if os.path.exists(tmp_file):
            os.remove(tmp_file)
    return HttpResponse(json.dumps(data))

#读取批量支给数据
def get_zj_csv_data(request):
    tmp_file = request.GET.get('tmp_file')
    data = {"code":0,"msg":"","count":0,'data':[]}
    if tmp_file:
        workbook = xlrd.open_workbook(tmp_file)
        allsheets = workbook.sheets()
        if allsheets:
            sheet = allsheets[0]
            row_number = sheet.nrows
            for i in range(row_number):
                if i > 1:
                    row_dict = {}
                    a_cd = str(sheet.cell(i,0).value).split('.')[0]
                    detail = asset_tools.getDetailMsg(a_cd)
                    print(detail)
                    if a_cd and data:
                        row_dict['a_type_cd'] = detail['a_type_cd'] 
                        if detail['a_action_type'] != '未入库':
                            row_dict['a_action_type'] = asset_tools.trans_action_type(detail['a_action_type'])
                        else:
                            row_dict['a_action_type'] = '未入库'
                        row_dict['a_cd'] = a_cd
                        row_dict['a_main_cd'] = str(sheet.cell(i,1).value).split('.')[0]      #主体资产号
                        row_dict['a_main_serial'] = str(sheet.cell(i,2).value).split('.')[0]  #主体序列号
                        row_dict['a_zj_object'] = str(sheet.cell(i,3).value).split('.')[0]
                        row_dict['a_zj_dept'] = str(sheet.cell(i,4).value).split('.')[0]
                        row_dict['a_action_state'] = str(sheet.cell(i,5).value).split('.')[0]
                        row_dict['a_action_remark'] = str(sheet.cell(i,6).value).split('.')[0]
                        #row_dict['a_action_type'] = asset_tools.get_detail(a_cd)
                        data['data'].append(row_dict)
        if os.path.exists(tmp_file):
            os.remove(tmp_file)
    return HttpResponse(json.dumps(data))

#读取批量支给归还数据
def get_zj_revert_csv_data(request):
    tmp_file = request.GET.get('tmp_file')
    data = {"code":0,"msg":"","count":0,'data':[]}
    if tmp_file:
        workbook = xlrd.open_workbook(tmp_file)
        allsheets = workbook.sheets()
        if allsheets:
            sheet = allsheets[0]
            row_number = sheet.nrows
            for i in range(row_number):
                if i > 1:
                    row_dict = {}
                    a_cd = str(sheet.cell(i,0).value).split('.')[0]
                    detail = asset_tools.getDetailMsg(a_cd)
                    if a_cd and data:
                        row_dict['a_type_cd'] = detail['a_type_cd']
                        row_dict['a_action_type'] = asset_tools.trans_action_type(detail['a_action_type'])

                        row_dict['a_cd'] = a_cd
                        row_dict['a_main_cd'] = str(sheet.cell(i,1).value).split('.')[0]      #主体资产号
                        row_dict['a_main_serial'] = str(sheet.cell(i,2).value).split('.')[0]  #主体序列号
                        row_dict['a_action_state'] = str(sheet.cell(i,3).value).split('.')[0]
                        row_dict['a_action_loc'] = str(sheet.cell(i,4).value).split('.')[0]
                        row_dict['a_action_remark'] = str(sheet.cell(i,5).value).split('.')[0]
                        data['data'].append(row_dict)
        if os.path.exists(tmp_file):
            os.remove(tmp_file)
    return HttpResponse(json.dumps(data))


def get_out_csv_data(request):
    tmp_file = request.GET.get('tmp_file')
    data = {"code":0,"msg":"","count":0,'data':[]}
    if tmp_file:
        workbook = xlrd.open_workbook(tmp_file)
        allsheets = workbook.sheets()
        if allsheets:
            sheet = allsheets[0]
            row_number = sheet.nrows
            for i in range(row_number):
                if i > 1:
                    row_dict = {}
                    a_cd = str(sheet.cell(i,0).value).split('.')[0]
                    detail = asset_tools.getDetailMsg(a_cd)
                    if a_cd and data:
                        row_dict['a_type_cd'] = detail['a_type_cd']
                        row_dict['a_action_type'] = asset_tools.trans_action_type(detail['a_action_type'])

                        row_dict['a_cd'] = a_cd
                        row_dict['a_main_cd'] = str(sheet.cell(i,1).value).split('.')[0]      #主体资产号
                        row_dict['a_main_serial'] = str(sheet.cell(i,2).value).split('.')[0]  #主体序列号
                        row_dict['a_action_dept'] = str(sheet.cell(i,3).value).split('.')[0]  #当前部门
                        row_dict['a_action_loc'] = str(sheet.cell(i,4).value).split('.')[0]
                        row_dict['a_action_state'] = str(sheet.cell(i,5).value).split('.')[0]
                        row_dict['a_action_model'] = str(sheet.cell(i,6).value).split('.')[0]
                        row_dict['a_take_user'] = str(sheet.cell(i,7).value).split('.')[0]
                        row_dict['a_confirm_user'] = str(sheet.cell(i,8).value).split('.')[0]
                        row_dict['a_action_remark'] = str(sheet.cell(i,9).value).split('.')[0]
                        #row_dict['a_action_type'] = asset_tools.get_detail(a_cd)
                        data['data'].append(row_dict)

        if os.path.exists(tmp_file):
            os.remove(tmp_file)
    return HttpResponse(json.dumps(data))

#资产退库前查询
def get_out_back_csv_data(request):
    tmp_file = request.GET.get('tmp_file')
    data = {"code":0,"msg":"","count":0,'data':[]}
    if tmp_file:
        workbook = xlrd.open_workbook(tmp_file)
        allsheets = workbook.sheets()
        if allsheets:
            sheet = allsheets[0]
            row_number = sheet.nrows
            for i in range(row_number):
                if i > 1:
                    row_dict = {}
                    a_cd = str(sheet.cell(i,0).value).split('.')[0]
                    detail = asset_tools.getDetailMsg(a_cd)
                    if a_cd and data:
                        row_dict['a_type_cd'] = detail['a_type_cd']
                        row_dict['a_origin_loc'] = detail['a_action_loc']
                        row_dict['a_action_type'] = asset_tools.trans_action_type(detail['a_action_type'])

                        row_dict['a_cd'] = a_cd
                        row_dict['a_main_cd'] = str(sheet.cell(i,1).value).split('.')[0]      #主体资产号
                        row_dict['a_main_serial'] = str(sheet.cell(i,2).value).split('.')[0]  #主体序列号
                        row_dict['a_action_state'] = str(sheet.cell(i,3).value).split('.')[0]
                        row_dict['a_action_loc'] = str(sheet.cell(i,4).value)
                        row_dict['a_back_user'] = str(sheet.cell(i,5).value)
                        row_dict['a_confirm_user'] = str(sheet.cell(i,6).value)
                        row_dict['a_action_remark'] = str(sheet.cell(i,7).value)
                        data['data'].append(row_dict)

        if os.path.exists(tmp_file):
            os.remove(tmp_file)
    return HttpResponse(json.dumps(data))

#批量修改资产位置查询
def get_edit_loc_data(request):
    tmp_file = request.GET.get('tmp_file')
    data = {"code":0,"msg":"","count":0,'data':[]}
    if tmp_file:
        workbook = xlrd.open_workbook(tmp_file)
        allsheets = workbook.sheets()
        if allsheets:
            sheet = allsheets[0]
            row_number = sheet.nrows
            for i in range(row_number):
                if i > 1:
                    row_dict = {}
                    a_cd = str(sheet.cell(i,0).value).split('.')[0]
                    detail = asset_tools.getDetailMsg(a_cd)
                    if a_cd and data:
                        row_dict['a_type_cd'] = detail['a_type_cd']
                        row_dict['a_action_type'] = asset_tools.trans_action_type(detail['a_action_type'])
                        row_dict['a_action_id'] = detail['a_action_id']
                        row_dict['a_cd'] = a_cd
                        row_dict['a_main_cd'] = str(sheet.cell(i,1).value).split('.')[0]      #主体资产号
                        row_dict['a_main_serial'] = str(sheet.cell(i,2).value).split('.')[0]  #主体序列号
                        row_dict['a_action_dept'] = str(sheet.cell(i,3).value)
                        row_dict['a_action_loc'] = str(sheet.cell(i,4).value)
                        data['data'].append(row_dict)

        if os.path.exists(tmp_file):
            os.remove(tmp_file)
    return HttpResponse(json.dumps(data))