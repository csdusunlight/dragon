from django.shortcuts import render
from django.http.response import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def upload(request):
    if request.POST.get('code') != 'Ijif4wjlsd2ijU*OJ':
        raise Http404
    for name, file in request.FILES.items():
        print file.name
        with open(file.name, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
            
    return HttpResponse('ok')