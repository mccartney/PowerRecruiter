import urllib2

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# This workaround is used to save javascript coverage report
# while using both Django and jscoverage server
@csrf_exempt
def jscoverage(request):
    u = urllib2.urlopen('http://127.0.0.1:8081/jscoverage-store/djangoIntegration', request.read())
    return HttpResponse(status=200)

def static(request, file):
    urllibResponse = urllib2.urlopen('http://127.0.0.1:8081/' + file, request.read())
    response = HttpResponse(content=urllibResponse.read())
    return response