#coding:utg-8
'''
Created on 2017年3月27日

@author: lch
'''
def parse_excel(request):
    ret = []
    file = request.FILES.get('file')
    with open('./name', 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    with open('./name', 'r') as file2:
        for line in file2:
            line = line.decode('gbk')
#             line = unicode(line, errors='ignore')
            
    return ret

