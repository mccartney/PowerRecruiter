from django.conf.urls import patterns, url
from power_recruiter.basic_site.views.index import index
from power_recruiter.basic_site.views.pie_chart import pie_chart
from power_recruiter.basic_site.views.line_chart import line_chart
from power_recruiter.basic_site.views.jscoverage import jscoverage

urlpatterns = patterns(
    '',
    url(r'^$', index, name='home'),
    url(r'^pieChart$', pie_chart, name='pieChart'),
    url(r'^lineChart$', line_chart, name='lineChart'),
    url(r'^jscoverage-store/djangoIntegration$', jscoverage, name='jscoverage')
)
