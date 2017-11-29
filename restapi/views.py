from django.shortcuts import render
from wafuli.models import TransList, UserEvent
from rest_framework import generics, permissions
from permissions import CsrfExemptSessionAuthentication
from restapi.permissions import IsOwnerOrStaff
from restapi.serializers import TransListSerializer
from restapi.Paginations import MyPageNumberPagination
import django_filters
from restapi.Filters import TranslistFilter

class BaseViewMixin(object):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    
class TranslistList(BaseViewMixin, generics.ListAPIView):
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return TransList.objects.all()
        else:
            return TransList.objects.filter(user=user)
    permission_classes = (IsOwnerOrStaff,)
    serializer_class = TransListSerializer
    pagination_class = MyPageNumberPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = TranslistFilter
    
