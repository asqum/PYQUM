# import os
# cwd = os.getcwd()

from pyqum.instrument.logger import set_status
from pyqum.instrument.logger import clocker
from subprocess import Popen, PIPE, STDOUT

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
    p_stdout = p.communicate(input=b'print(10*10)')
    p.wait()
    output = p_stdout[0]
    print(output)
    # print("\n", [x for x in map(bin, output)])
    print("Output: %s" %(output.decode("utf-8")))

    with Popen(['python'], cwd=cwd, stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True) as p:
        # p_stdout = p.communicate(input=b'import CLOSAWG\nCLOSAWG.run()')
        p_stdout = p.communicate(input='import abc\n'.encode())
        output = p_stdout[0]
        print("\n", output)
        # print("\n", [x for x in map(bin, output)])
        print(output.decode("utf-8"))

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

stage, prev = clocker(0)
set_status("MPW", {"data": list(range(10000000*2))})
CMD = ["python", "-c", "from pyqum.directive import multiprocessor as mp; mp.worker_fresp(%s,%s)"%(10000,1000)]
proc = Popen(CMD, stdout=PIPE, shell=True)
output = proc.stdout.read().decode("utf-8")
print("result: %s" %output)
stage, prev = clocker(stage, prev) # Marking time
