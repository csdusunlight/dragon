#coding:utf-8
from .models import Project
from project_admin.serializers import ProjectSerializer,\
    ProjectInvestDataSerializer, ProjectBalanceSerializer
# Create your views here.

from rest_framework import generics, permissions
from project_admin.permissions import IsAdminOrReadOnly,\
    CsrfExemptSessionAuthentication
import django_filters
from project_admin.Filters import ProjectFilter, ProjectInvestDateFilter,\
    ProjectBalanceFilter
from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse
from django.http.response import Http404
from project_admin.Paginations import ProjectPageNumberPagination
from project_admin.models import ProjectInvestData, ProjectBalance
class BaseViewMixin(object):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,IsAdminOrReadOnly)
    
class ProjectList(BaseViewMixin,generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = ProjectFilter
    pagination_class = ProjectPageNumberPagination
#     search_fields = ('=name', '=contact')


class ProjectDetail(BaseViewMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectInvestDataList(BaseViewMixin,generics.ListCreateAPIView):
    queryset = ProjectInvestData.objects.all()
    serializer_class = ProjectInvestDataSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
#     filter_fields = ('__all__')
    filter_class = ProjectInvestDateFilter
    pagination_class = ProjectPageNumberPagination
#     search_fields = ('=name', '=contact')


class ProjectInvestDataDetail(BaseViewMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = ProjectInvestData.objects.all()
    serializer_class = ProjectInvestDataSerializer 

class ProjectBalanceList(BaseViewMixin,generics.ListCreateAPIView):
    queryset = ProjectBalance.objects.all()
    serializer_class = ProjectBalanceSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
#     filter_fields = ('__all__')
    filter_class = ProjectBalanceFilter
    pagination_class = ProjectPageNumberPagination
#     search_fields = ('=name', '=contact')


class ProjectBalanceDetail(BaseViewMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = ProjectBalance.objects.all()
    serializer_class = ProjectBalanceSerializer 
# 立项部分增加
def project_index(request):
    admin_user = request.user
    if request.method == "GET":
        if not ( admin_user.is_authenticated() and admin_user.is_staff):
            return redirect(reverse('admin:login') + "?next=" + reverse('admin_finance'))
        return render(request,"project.html")
 


def project_data(request):
    admin_user = request.user
    if request.method == "GET":
        if not ( admin_user.is_authenticated() and admin_user.is_staff):
            return redirect(reverse('admin:login') + "?next=" + reverse('admin_finance'))
        return render(request,"project_data.html")
    
def project_finance(request):
    admin_user = request.user
    if request.method == "GET":
        if not ( admin_user.is_authenticated() and admin_user.is_staff):
            return redirect(reverse('admin:login') + "?next=" + reverse('admin_finance'))
        return render(request,"project_finance.html")



def project_settle(request):
    admin_user = request.user
    if request.method == "GET":
        if not ( admin_user.is_authenticated() and admin_user.is_staff):
            return redirect(reverse('admin:login') + "?next=" + reverse('admin_finance'))
        return render(request,"project_settle.html")

# 立项部分---end
 