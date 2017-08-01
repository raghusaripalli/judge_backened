from .views import *

from datetime import datetime
import os
from .import Judge
extensions = {"c++":".cpp","python":".py","java":".java","c":".c"}

def JudgeCode(File,contest,problem):
    ok,compileRes = Judge.Compile(File)
    actual = File[:-4]+"_actual.txt"
    if (ok == False):
        return compileRes

    inputFile = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Contest_Problems', contest, problem,"input1.txt")
    expectedFile = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Contest_Problems', contest, problem,"Expected1.txt")
    actualFile = os.path.join(os.path.dirname(os.path.dirname(__file__)),'Contest_submissions',contest,problem,actual)
    verdict = Judge.Execute(compileRes,inputFile,expectedFile,actualFile)
    #TaskKill = "Taskkill /IM " + actualFile + " /F"
    #os.system(TaskKill)
    #os.remove(actualFile)
    #TaskKill = "Taskkill /IM " + compileRes + " /F"
    #os.system(TaskKill)
    #os.remove(compileRes)
    return verdict


# import queue
# import threading
# from time import sleep
#
# num_worker_threads = 1
# q = queue.Queue()
# threads = []
#
# def do_work(job):
#     verdict = JudgeCode(job["filepath"], job["contest"],job["problem"])
#     job["verdict"] = verdict
#     job["evaluated"] = True
#
# def worker():
#     while True:
#         item = q.get()
#         if item is None:
#             break
#         do_work(item)
#         q.task_done()
#
# for i in range(num_worker_threads):
#     t = threading.Thread(target=worker)
#     t.start()
#     threads.append(t)

# lock = threading.Lock()
#
# class JobThread(threading.Thread):
#     def __init__(self, job):
#         threading.Thread.__init__(self)
#         self.name = job["filepath"]
#         self.job = job
#
#     def run(self):
#         print ("Starting " + self.name)
#         with lock:
#             verdict = JudgeCode(self.job["filepath"],self.job["contest"],self.job["problem"])
#             self.job["verdict"] = verdict
#             self.job["evaluated"] = True
#         print ("Ended "+self.name)
#


class SubmitCode(CSRFExemptMixin,APIView):
    authentication_classes = [JSONWebTokenAuthentication,SessionAuthentication,BasicAuthentication]
    permission_classes =  [IsAuthenticated]

    def post(self, request,format=None):
        try:
            data = request.data.copy()
            user = request.user
            contest = str(data["contest"])
            problem = str(data["problem"])
            language = str(data["language"]).lower()
            filename = str(user)+"_"+str(datetime.now().strftime("%B_%d_%Y_%H_%M_%S_%f"))
            filename += extensions[language]
            filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)),'Contest_submissions',contest,problem,filename)
            with open(filepath, 'w') as destination:
                destination.write(data["code"])

            job = {
                "filepath" : filepath,
                "contest" : contest,
                "problem" : problem,
                "verdict" : None,
                "evaluated" : False
            }

            #q.put(job)
            #
            # while job["evaluated"] == False:
            #     print ("..waiting...",job["filepath"])
            #     sleep(2.0)
            #
            # # verdict = job["verdict"]
            verdict = JudgeCode(filepath,contest,problem)

            # th = JobThread(job)
            # th.start()
            # th.join()

            ret = dict()
            ret["verdict"] = verdict
            return Response(ret,status=status.HTTP_201_CREATED)

        except Exception as ex:
            print (ex)
            return Response(Http404)