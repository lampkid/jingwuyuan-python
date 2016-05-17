# -*- coding=utf-8 -*-

import time
from datetime import datetime

class TaskManager(object):
    def __init__(self):
        self.taskList = []
        self.taskExecuted = False

    def addTask(self, task):
        self.taskList.append(task)

    def doTask(self):
        print self.taskList
        for task in self.taskList:
            if task:
                task()



    def startCron(self, seconds=84400, hour=None):
        while True:
            if hour:
                now = datetime.now()
                nowHour = now.hour

                if nowHour == hour and not self.taskExecuted:
                    self.taskExecuted = True
                    self.doTask()

                elif nowHour == hour - 1:
                    self.taskExecuted = False

                time.sleep(60)

            else:
                time.sleep(seconds)
                self.doTask()


# 后续可支持任务级别的定时,目前所有任务定时时间是一样的，统一的

# for test
def task():
    print datetime.now()

def execCmd(cmd):

    import subprocess

    subprocess.Popen(cmd)


if __name__ == '__main__':


    tm = TaskManager()
    tm.addTask(task)

    seconds = 1 * 24 * 3600

    tm.startCron(hour=2)


