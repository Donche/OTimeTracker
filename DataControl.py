from os.path import exists
from datetime import datetime
import uuid
import csv

class DataControl():
    def __init__(self):
        self.projectIdNames = {}
        self.archivedProjectIdNames = {}
        self.trackRecord = {}
        self.workingProject = ""
        self.workingId = 0
        self.startTime = 0

        if exists('OTT_projects.txt'):
            with open('OTT_projects.txt','r') as f:
                lines = [i.strip() for i in f.readlines()]
                for l in lines:
                    if l[:2] == "--":
                        name, id = l[2:].split(", ")
                        self.archivedProjectIdNames[uuid.UUID(id.strip())] = name
                    else:
                        name, id = l.split(", ")
                        self.projectIdNames[uuid.UUID(id.strip())] = name
            print("projects: ", self.projectIdNames)
            print("archived projects: ", self.archivedProjectIdNames)


        log_file = '{}-{}.log'.format(datetime.now().year, datetime.now().month)
        if exists(log_file):
            with open(log_file, 'r') as f:
                r = csv.reader(f, delimiter=',')
                for row in r:
                    id = uuid.UUID(row[0].strip())
                    try:
                        if id in self.projectIdNames:
                            name = self.projectIdNames[id]
                        else:
                            name = self.archivedProjectIdNames[id]
                    except:
                        print("project id ", id, " not recognized")
                        continue
                    if name in self.trackRecord:
                        self.trackRecord[name].append((row[1], row[2], int(row[3])))
                    else:
                        self.trackRecord[name] = [(row[1], row[2], int(row[3]))]


    # ******** project **********
    def __getIdWithName(self, name):
        for id in self.projectIdNames:
            if name == self.projectIdNames[id]:
                return id

    def hasProject(self, name):
        for id in self.projectIdNames:
            if name == self.projectIdNames[id]:
                return True
        return False

    def tryAddProject(self, name):
        if self.hasProject(name):
            return False
        else:
            id = uuid.uuid1()
            self.projectIdNames[id] = name
            with open('OTT_projects.txt','a') as f:
                f.write(name+", "+str(id)+"\n")
            return True

    def archiveProject(self, name):
        print('archive ', name)
        id = self.__getIdWithName(name)
        self.archivedProjectIdNames[id] = self.projectIdNames.pop(id, None)

        with open('OTT_projects.txt','w') as f:
            for id in self.projectIdNames:
                f.write(self.projectIdNames[id]+", "+str(id)+"\n")
            for id in self.archivedProjectIdNames:
                f.write("--"+self.archivedProjectIdNames[id]+", "+str(id)+"\n")

    def renameProject(self, oldName, newName):
        print('rename ', oldName, " to ", newName)
        id = self.__getIdWithName(oldName)
        self.projectIdNames[id] = newName

        with open('OTT_projects.txt','w') as f:
            for id in self.projectIdNames:
                f.write(self.projectIdNames[id]+", "+str(id)+"\n")
            for id in self.archivedProjectIdNames:
                f.write("--"+self.archivedProjectIdNames[id]+", "+str(id)+"\n")


    # ******** times **********
    def getTodayTotal(self, name):
        if name in self.trackRecord:
            return sum([i[2] for i in self.trackRecord[name]])
        else:
            return 0


    def startWorking(self, name):
        self.workingProject = name
        self.startTime= datetime.now()
        for id in self.projectIdNames:
            if self.workingProject == self.projectIdNames[id]:
                self.workingId = id
                break

    def getWorkingTime(self):
        return datetime.now()-self.startTime


    def stopWorking(self):
        endTime = datetime.now() 
        if self.workingProject in self.trackRecord:
            self.trackRecord[self.workingProject].append((str(self.startTime), str(endTime), (endTime-self.startTime).seconds))
        else:
            self.trackRecord[self.workingProject] = [(str(self.startTime), str(endTime), (endTime-self.startTime).seconds)]
        log_file = '{}-{}.log'.format(self.startTime.year, self.startTime.month)
        with open(log_file, 'a') as f:
            f.write(str(self.workingId) + ", "+ str(self.startTime) + ", " + str(endTime) + ", " + str((endTime-self.startTime).seconds)+"\n")




