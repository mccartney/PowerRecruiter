#Power Recruiter - a browser-based FSM-centered database application profiled for IT recruiters
#Copyright (C) 2015 Krzysztof Fudali, Andrzej Jackowski, Cezary Kosko, Filip Ochnik
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

rm -rf qunit/
rm -rf djangoIntegration*
rm -rf summary/
phantomjs run-jscover-qunit.js http://localhost:8081/jsTesting/testView.html > qunit-report.xml
REMOTE_DJANGO_STATIC=1 python ./systemTests/runSystemTests.py
java -cp JSCover-all.jar jscover.report.Main --merge qunit djangoIntegration* summary
java -cp JSCover-all.jar jscover.report.Main --format=COBERTURAXML summary summary
head -n -3 qunit-report.xml > qunit-report2.xml
sed 's/<source>\/root\/.jenkins\/workspace\/ZPP\/power_recruiter\/power_recruiter\/basic_site\/static\/js\/jsTesting\/summary<\/source>/<source>\/root\/.jenkins\/workspace\/ZPP\/power_recruiter\/power_recruiter\/basic_site\/static\/js\/<\/source>/g' summary/cobertura-coverage.xml > summary/cobertura-coverage2.xml
