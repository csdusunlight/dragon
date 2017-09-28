#coding:utf-8
'''
Created on 2017年9月28日

@author: lch
'''
class SubdomainMiddleware(object):
    def process_request(self, request):
        domain_parts = request.get_host().split('.')
        if len(domain_parts) == 3 and domain_parts[0] != 'www':
            request.path_info = '/%s%s' % (domain_parts[0], request.path)