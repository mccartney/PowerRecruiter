rm -rf qunit/
rm -rf djangoIntegration/
rm -rf summary/
phantomjs run-jscover-qunit.js http://localhost:8081/jsTesting/testView.html > qunit-report.xml
python ./systemTests/runSystemTests.py
java -cp JSCover-all.jar jscover.report.Main --merge qunit djangoIntegration summary
java -cp JSCover-all.jar jscover.report.Main --format=COBERTURAXML summary summary
head -n -3 qunit-report.xml > qunit-report2.xml
sed 's/<source>\/root\/.jenkins\/workspace\/ZPP\/power_recruiter\/power_recruiter\/basic_site\/static\/js\/jsTesting\/summary<\/source>/<source>\/root\/.jenkins\/workspace\/ZPP\/power_recruiter\/power_recruiter\/basic_site\/static\/js\/<\/source>/g' summary/cobertura-coverage.xml > summary/cobertura-coverage2.xml
