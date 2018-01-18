import os
import datetime
from django.shortcuts import render
from django.http.response import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from dragon.settings import MEDIA_ROOT

# Create your views here.

@csrf_exempt
def upload(request):
    if request.POST.get('code') != 'Ijif4wjlsd2ijU*OJ':
        raise Http404
    today =datetime.date.today().strftime("%Y-%m-%d")
    todaydir = os.path.join(MEDIA_ROOT, 'QQmsgs', today).replace('\\','/')
    if not os.path.exists(todaydir):
        os.makedirs(todaydir)
    for name, file in request.FILES.items():
        with open( os.path.join(todaydir, file.name), 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
            
    return HttpResponse('ok')