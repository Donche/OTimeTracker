from os.path import exists
from datetime import datetime
import uuid
import csv

class DataControl():
    def __init__(self):
        self.project_id_names = {}
        self.archived_project_id_names = {}
        self.track_record = {}
        self.working_project = ""
        self.working_id = 0
        self.start_time = 0

        if exists('OTT_projects.txt'):
            with open('OTT_projects.txt','r') as f:
                lines = [i.strip() for i in f.readlines()]
                for l in lines:
                    if l[:2] == "--":
                        name, id = l[2:].split(", ")
                        self.archived_project_id_names[uuid.UUID(id.strip())] = name
                    else:
                        name, id = l.split(", ")
                        self.project_id_names[uuid.UUID(id.strip())] = name
            print("projects: ", self.project_id_names)
            print("archived projects: ", self.archived_project_id_names)


        log_file = '{}-{}.log'.format(datetime.now().year, datetime.now().month)
        if exists(log_file):
            with open(log_file, 'r') as f:
                r = csv.reader(f, delimiter=',')
                for row in r:
                    id = uuid.UUID(row[0].strip())
                    try:
                        if id in self.project_id_names:
                            name = self.project_id_names[id]
                        else:
                            name = self.archived_project_id_names[id]
                    except:
                        print("project id ", id, " not recognized")
                        continue
                    if name in self.track_record:
                        self.track_record[name].append((row[1], row[2], int(row[3])))
                    else:
                        self.track_record[name] = [(row[1], row[2], int(row[3]))]


    # ******** project **********
    def __get_id_with_name(self, name):
        for id in self.project_id_names:
            if name == self.project_id_names[id]:
                return id

    def hasProject(self, name):
        for id in self.project_id_names:
            if name == self.project_id_names[id]:
                return True
        return False

    def try_add_project(self, name):
        if self.hasProject(name):
            return False
        else:
            id = uuid.uuid1()
            self.project_id_names[id] = name
            with open('OTT_projects.txt','a') as f:
                f.write(name+", "+str(id)+"\n")
            return True

    def archive_project(self, name):
        print('archive ', name)
        id = self.__get_id_with_name(name)
        self.archived_project_id_names[id] = self.project_id_names.pop(id, None)

        with open('OTT_projects.txt','w') as f:
            for id in self.project_id_names:
                f.write(self.project_id_names[id]+", "+str(id)+"\n")
            for id in self.archived_project_id_names:
                f.write("--"+self.archived_project_id_names[id]+", "+str(id)+"\n")

    def rename_project(self, oldName, newName):
        print('rename', oldName, "to", newName)
        id = self.__get_id_with_name(oldName)
        self.project_id_names[id] = newName

        with open('OTT_projects.txt','w') as f:
            for id in self.project_id_names:
                f.write(self.project_id_names[id]+", "+str(id)+"\n")
            for id in self.archived_project_id_names:
                f.write("--"+self.archived_project_id_names[id]+", "+str(id)+"\n")


    # ******** times **********
    def get_today_total(self, name):
        if name in self.track_record:
            return sum([i[2] for i in self.track_record[name]])
        else:
            return 0


    def start_working(self, name):
        self.working_project = name
        self.start_time= datetime.now()
        for id in self.project_id_names:
            if self.working_project == self.project_id_names[id]:
                self.working_id = id
                break

    def get_working_time(self):
        return datetime.now()-self.start_time


    def stop_working(self):
        endTime = datetime.now() 
        if self.working_project in self.track_record:
            self.track_record[self.working_project].append((str(self.start_time), str(endTime), (endTime-self.start_time).seconds))
        else:
            self.track_record[self.working_project] = [(str(self.start_time), str(endTime), (endTime-self.start_time).seconds)]
        log_file = '{}-{}.log'.format(self.start_time.year, self.start_time.month)
        with open(log_file, 'a') as f:
            f.write(str(self.working_id) + ", "+ str(self.start_time) + ", " + str(endTime) + ", " + str((endTime-self.start_time).seconds)+"\n")




