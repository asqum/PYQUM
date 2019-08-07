# import os
# cwd = os.getcwd()

from pyqum.instrument.logger import set_status
from pyqum.instrument.logger import clocker

from subprocess import Popen, PIPE, STDOUT
from numpy import array
import json

# cwd = "e:\\NCHUQ\\PYQUM\\TEST"
cwd = "C:\\Users\\ASQUM\\Documents\\GitHub\\PYQUM\\TEST\\FACE\\pyqum\\directive"

choose_A, choose_B = True, True

if choose_A:
    # CMD = ["ECHO", "HELLO", "&DIR", "&python", "-c", "import INITAWG; INITAWG.run(); import CLOSAWG; CLOSAWG.run()"]
    CMD = ["python", "-c", "print(10*10)"]
    proc = Popen(CMD, cwd=cwd, stdout=PIPE, shell=True)
    output = proc.stdout.read().decode("utf-8")
    print(output)

if choose_B:
    p = Popen(['python'], stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True)
    # p_stdout = p.communicate(input=b'import INITAWG\nINITAWG.run()\nimport CLOSAWG\nCLOSAWG.run()')
    p_stdout = p.communicate(input=b'print(list(range(100)))')
    p.wait()
    output = p_stdout[0]
    print(output)
    # print("\n", [x for x in map(bin, output)])
    print("Output of type (%s): %s" %(type(output), output.decode("utf-8")))

    with Popen(['python'], cwd=cwd, stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True) as p:
        # p_stdout = p.communicate(input=b'import CLOSAWG\nCLOSAWG.run()')
        p_stdout = p.communicate(input=('print(list(range(%s)))'%10000000).encode())
        output = p_stdout[0]
        A = array(output.decode("utf-8")[1:-3].split(", "), dtype="int").reshape(1000,10000)
        print(A[101,101] + A[10,10])
        # p.stdin.write(('print(%s)'%([1,1,1,1,100])).encode())
        # output = p.stdout.read()
        # A = array(output.decode("utf-8")[1:-3].split(", "), dtype="int")
        # print(A[0] + A[-1])

    # with Popen(["ifconfig"], stdout=PIPE) as proc:
    #     print(proc.stdout.read())

# p = Popen(["echo", "hello world"], stdout=PIPE)
# print(p.communicate())

# from subprocess import call
# call(["ping", "www.cyberciti.biz"])

# p = Popen("date", stdout=PIPE, shell=True)
# (output, err) = p.communicate()
# # p_status = p.wait()
# print("Command output : ", output)

# p = Popen("python", stdout=PIPE, shell=True)
# (output, err) = p.communicate(input=b'10*10')
# # p_status = p.wait()
# print("Command output : ", output)



with Popen(['python'], cwd=cwd, stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True) as p:
    p_stdout = p.communicate(input='print({"a":[[0,1,2,3,4,5],[5,4,3,2,1,0]], "b":[1,2,3,4,5,6]})'.encode())
    output = p_stdout[0]
    A = json.loads(output.decode("utf-8").replace("\'", "\""))
    print(A['a'][0])
    print(A['a'])

CMD = ["python", "-c", "print({'a':[[0,1,2,3,4,5],[5,4,3,2,1,0]], 'b':[1,2,3,4,5,6]})"]
with Popen(CMD, stdout=PIPE, shell=True) as proc:
    output = json.loads(proc.stdout.read().decode("utf-8").replace("\'", "\""))
    print(output['a'])