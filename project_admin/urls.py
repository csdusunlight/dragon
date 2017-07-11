#coding:utf-8
'''
Created on 20170703

@author: lch
'''

from django.conf.urls import url
from project_admin import views
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [
    url(r'^contacts/$', views.ContactList.as_view()),
    url(r'^contacts/(?P<pk>[0-9]+)/$', views.ContactDetail.as_view(), kwargs={'partial':True}),
    url(r'^platform/$', views.PlatformList.as_view()),
    url(r'^platform/(?P<pk>[0-9]+)/$', views.PlatformDetail.as_view(), kwargs={'partial':True}),
    url(r'^projects/$', views.ProjectList.as_view()),
    url(r'^projects/(?P<pk>[0-9]+)/$', views.ProjectDetail.as_view(), kwargs={'partial':True}),
    url(r'^investdata/$', views.ProjectInvestDataList.as_view()),
    url(r'^investdata/(?P<pk>[0-9]+)/$', views.ProjectInvestDataDetail.as_view()),
    url(r'^balance/$', views.CompanyBalanceList.as_view()),
    url(r'^balance/(?P<pk>[0-9]+)/$', views.CompanyBalanceDetail.as_view()),
    url(r'^projectstatis/$', views.ProjectStatisList.as_view()),
    url(r'^daystatis/$', views.DayStatisList.as_view()),
]
from django.conf.urls import include


urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',namespace='rest_framework')),
    url(r'^$', views.project_index, name='project_index'),
    url(r'^project_data/$', views.project_data, name='project_data'),
    url(r'^project_finance/$', views.project_finance, name='project_finance'),
    url(r'^project_settle/$', views.project_settle, name='project_settle'),
    url(r'^import_projectdata_excel/$', views.import_projectdata_excel, name='import_projectdata_excel'),
]
