rm -rf phantom/
phantomjs run-jscover-qunit.js http://localhost:8081/jsTesting/testView.html > qunit-report.xml
java -cp JSCover-all.jar jscover.report.Main --format=COBERTURAXML phantom phantom
head -n -3 qunit-report.xml > qunit-report2.xml
sed 's/<source>\/root\/.jenkins\/workspace\/ZPP\/power_recruiter\/power_recruiter\/basic_site\/static\/js\/jsTesting\/phantom<\/source>/<source>\/root\/.jenkins\/workspace\/ZPP\/power_recruiter\/power_recruiter\/basic_site\/static\/js\/<\/source>/g' phantom/cobertura-coverage.xml > phantom/cobertura-coverage2.xml
