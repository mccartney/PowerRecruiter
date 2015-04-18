import time
import subprocess
import os

print "Test started"
FNULL = open(os.devnull, 'w')
old_cwd = os.getcwd()
os.chdir("../../../../../../")
django_process = subprocess.Popen(["./manage.py", "runserver"], stderr=FNULL, stdout=FNULL)
os.chdir(old_cwd)
print "Wait for django"
time.sleep(5)
print "Django started"
test_process = subprocess.Popen(["phantomjs", "run-jscover-system-test.js", "http://localhost:8000", "tests/indexTest.js"])
test_process.wait()
print "Test complete"
django_process.kill()

