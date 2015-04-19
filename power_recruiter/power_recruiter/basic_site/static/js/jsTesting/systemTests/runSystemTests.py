import time
import subprocess
import os

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
my_env["REMOTE_DJANGO_STATIC"] = str(1)
test_process = subprocess.Popen(["phantomjs", "./systemTests/run-jscover-system-test.js", "http://localhost:8000", "tests/indexTest.js"], env=my_env)
test_process.wait()
print "Test complete"
django_process.kill()

