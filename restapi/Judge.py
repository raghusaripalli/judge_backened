import sys, os
import subprocess
from time import sleep
from time import time

if sys.platform.startswith("win"):
    import ctypes
    SEM_NOGPFAULTERRORBOX = 0x0002 # From MSDN
    ctypes.windll.kernel32.SetErrorMode(SEM_NOGPFAULTERRORBOX);
    CREATE_NO_WINDOW = 0x08000000    # From Windows API
    subprocess_flags = CREATE_NO_WINDOW
else:
    subprocess_flags = 0

Trigger = False
Verdict = -1
ExecutionTime = -1
VerdictMsg = {-1:"DidNotProcess",0:"Accepted",1:"WrongAnswer",2:"CompileError",3:"RunTimeError",4:"TimeLimitExceeded"}

"""
    Verdict is a Global Variable with following states. 
    -1 = Did Not Process
    0  = Accepted
    1  = Wrong Answer
    2  = Compile Error
    3  = RunTime Error
    4  = TimeLimit Exceeded

    ExecutionTime is a Global Variable Holds Elapsed time of the Program for
    the given Input.
"""

# import threading
# class Command(object):
#     def __init__(self, cmd,timeout,inStream,outStream):
#         self.cmd = cmd
#         self.process = None
#         self.timeout = timeout
#         self.input = inStream
#         self.output = outStream
#     def run(self):
#         def target():
#             print ('Thread started')
#             self.process = subprocess.Popen(self.cmd,stdin=self.input,stdout=self.output,creationflags=subprocess_flags)
#             self.process.communicate()
#             print ('Thread finished')
#         try:
#             start = time()
#             thread = threading.Thread(target=target)
#             thread.start()
#
#             thread.join(self.timeout)
#             if thread.is_alive():
#                 print ('Terminating process')
#                 execTime = time() - start
#                 self.process.terminate()
#                 self.process.kill()
#                 thread.join()
#                 return 4,execTime
#         except subprocess.CalledProcessError as RE:
#             execTime = time()-start
#             return 3,execTime
#         execTime = time()-start
#         return -1,execTime

import psutil
def Execute(ExeFile,InputFile,ExpectedFile,ActualFile):
    #print("Judge")
    fr = open(InputFile, "r")
    fw = open(ActualFile, "w")

    global Verdict
    global ExecutionTime


    ExecProcess = subprocess.Popen(ExeFile, shell=Trigger,creationflags=subprocess_flags,stdin=fr, stdout=fw)
    ps = psutil.Process(ExecProcess.pid)
    print(ps.cpu_times)
    try:
        start = time()
        ExecProcess.communicate(timeout=1)
    except subprocess.TimeoutExpired as TLE:
        Verdict = 4
        elapsed = (time() - start)
        ExecutionTime = elapsed

        ExecProcess.terminate()
        ExecProcess.kill()

        fr.close()
        fw.close()

        print ("Verdict : TLE",ExecutionTime,"\n",TLE)
        return "TLE"
    except subprocess.CalledProcessError as RE:
        elapsed = (time() - start)
        ExecutionTime = elapsed

        ExecProcess.terminate()
        ExecProcess.kill()
        fr.close()
        fw.close()

        print ("Verdict : RE",ExecutionTime,"\n",RE)
        return "RE"
    finally:
        pass
        #print(ps.cpu_times)
        #print (ps.cpu_percent())

    elapsed = (time() - start)
    ExecutionTime = elapsed

    fr.close()
    fw.close()

    ok = subprocess.call(["fc", ExpectedFile,ActualFile],stdout=subprocess.PIPE)

    sleep(0.001)

    if(ok == 0):
        print("Verdict : AC", ExecutionTime)
        return "AC"
    else:
        print("Verdict : WA", ExecutionTime)
        return "WA"

    return True


def Compile(File):
    #print("Compile")
    Exe = File[:-4]+".exe"
    #cmd = "g++ "+File+" -o "+Exe
    cmd = "g++ -fomit-frame-pointer -fexpensive-optimizations -O3 "+File+" -o "+Exe
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    except Exception as ex:
        return False,"Compile Exception Raised"
    stdout, stderr = proc.communicate()
    if proc.returncode != 0:
        return False,stderr.decode("utf-8")
    else:
        return True,Exe