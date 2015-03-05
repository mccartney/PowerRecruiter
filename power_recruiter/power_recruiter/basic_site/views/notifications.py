__author__ = 'shadowsword'
from django.shortcuts import render

def notifications(request):
    context = None
    return render(request, "notifications.html", context)