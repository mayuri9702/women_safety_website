from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    context={
        'variable1':'this is sent',
        'variable2':'this is not sent'
    }
    return render(request,'index.html',context)         # send variable
    # return HttpResponse("this is home page")

def about(request):
    return HttpResponse("this is about page")

def contact(request):
    return HttpResponse("this is contact page")

def services(request):
    return HttpResponse("this is services page")