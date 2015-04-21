import time
import subprocess
import os
import psutil


FNULL = open(os.devnull, 'w')

print "Test started"

old_cwd = os.getcwd()
os.chdir("../../../../../")
django_process = subprocess.Popen(["./manage.py", "runserver"], stderr=FNULL, stdout=FNULL)
os.chdir(old_cwd)
print "Wait for django"
time.sleep(5)
print "Django started"

my_env = os.environ.copy()
test_process = subprocess.Popen(["phantomjs", "./systemTests/run-jscover-system-test.js", "http://localhost:8000", "tests/indexTest.js"], env=my_env)
test_process.wait()
test_process = subprocess.Popen(["phantomjs", "./systemTests/run-jscover-system-test.js", "http://127.0.0.1:8000/pieChart", "tests/pieChartTest.js"], env=my_env)
test_process.wait()
test_process = subprocess.Popen(["phantomjs", "./systemTests/run-jscover-system-test.js", "http://127.0.0.1:8000/lineChart", "tests/lineChartTest.js"], env=my_env)
test_process.wait()
print "Test complete"

parent = psutil.Process(django_process.pid)
for child in parent.children(recursive=True):  # or parent.children() for recursive=False
    child.kill()
parent.kill()