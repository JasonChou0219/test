import epicbox

epicbox.configure(profiles=[epicbox.Profile('python', 'user_script:latest')])
script = b"""
import sila2lib
import time
for i in range(20):
    print(f'hallo {i}')
    time.sleep(1)
"""
files = [{'name': 'experiment.py', 'content': script}]
limits = {'cputime': 10, 'memory': 100}
result = epicbox.run('python',
                     'python3 experiment.py',
                     files=files,
                     limits=limits)
print(result)
