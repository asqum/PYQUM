# import os
# cwd = os.getcwd()

from subprocess import Popen, PIPE, STDOUT

cwd = "e:\\NCHUQ\\PYQUM\\TEST"

choose_A, choose_B = False, False

if choose_A:
    CMD = ["ECHO", "HELLO", "&DIR", "&python", "-c", "import INITAWG; INITAWG.run(); import CLOSAWG; CLOSAWG.run()"]
    proc = Popen(CMD, cwd=cwd, stdout=PIPE, shell=True)
    output = proc.stdout.read().decode("utf-8")
    print(output)

if choose_B:
    p = Popen(['python'], cwd=cwd, stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True)
    p_stdout = p.communicate(input=b'import INITAWG\nINITAWG.run()\nimport CLOSAWG\nCLOSAWG.run()')
    output = p_stdout[0]
    # print("\n", output)
    # print("\n", [x for x in map(bin, output)])
    print(output.decode("utf-8"))

    # p = Popen(['python'], cwd=cwd, stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True)
    # p_stdout = p.communicate(input=b'import CLOSAWG\nCLOSAWG.run()')
    # output = p_stdout[0]
    # # print("\n", output)
    # # print("\n", [x for x in map(bin, output)])
    # print(output.decode("utf-8"))
