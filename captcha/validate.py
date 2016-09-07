#coding:utf-8
'''
Created on 2016年9月7日

@author: lch
'''
from django.http.response import Http404, JsonResponse
from captcha.views import imageV, generateCap
def validate_randcode(request):
    result = {'code':-1}
    hashkey = request.GET.get('hashkey', None)
    response = request.GET.get('response', None)
    if not (hashkey and response):
        raise Http404
    ret = imageV(hashkey, response)
    if ret != 0:
        result['code'] = 1
        result.update(generateCap())
    else:
        result['code'] = 0
    return JsonResponse(result)