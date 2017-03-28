#coding:utf-8
'''
Created on 2017年3月27日

@author: lch
'''

import xlrd
import xlwt
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

@csrf_exempt
def parse_excel(request):
    if request.method == 'GET':
        return render(request,'upload_excel.html')
    else:
        
        ret = []
        file = request.FILES.get('file')
        print file.name
        with open('./test.xlsx', 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        data = xlrd.open_workbook('test.xlsx')
        table = data.sheets()[0]
        nrows = table.nrows
        ncols = table.ncols
        print nrows,ncols
        for i in range(2):
            
            row =  table.row_values(i)
            for j in range(ncols):
                print table.cell(i,j).ctype
        style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on', num_format_str='#,##0.00')
        style1 = xlwt.easyxf(num_format_str='D-MMM-YY')
        
        wb = xlwt.Workbook()
        ws = wb.add_sheet('A Test Sheet')
        
        ws.write(0, 0, 1234.56, style0)
        ws.write(1, 0, datetime.now(), style1)
        ws.write(2, 0, 1)
        ws.write(2, 1, 1)
        ws.write(2, 2, xlwt.Formula("A3+B3"))
        
        wb.save('example.xls')
                
        return ret

