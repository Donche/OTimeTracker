from os.path import exists
import uuid
import csv

class TrackData():
    def __init__(self):
        self.project_id_names = {}
        self.archived_project_id_names = {}
        self.track_record = {}

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


    def loadHistory(self, log_file):
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
    def get_id_with_name(self, name):
        for id in self.project_id_names:
            if name == self.project_id_names[id]:
                return id

    def has_project(self, name):
        for id in self.project_id_names:
            if name == self.project_id_names[id]:
                return True
        return False

    def try_add_project(self, name):
        if self.has_project(name):
            return False
        else:
            id = uuid.uuid1()
            self.project_id_names[id] = name
            with open('OTT_projects.txt','a') as f:
                f.write(name+", "+str(id)+"\n")
            return True

    def archive_project(self, name):
        print('archive ', name)
        id = self.get_id_with_name(name)
        self.archived_project_id_names[id] = self.project_id_names.pop(id, None)

        with open('OTT_projects.txt','w') as f:
            for id in self.project_id_names:
                f.write(self.project_id_names[id]+", "+str(id)+"\n")
            for id in self.archived_project_id_names:
                f.write("--"+self.archived_project_id_names[id]+", "+str(id)+"\n")

    def rename_project(self, old_name, new_name):
        print('rename', old_name, "to", new_name)
        id = self.get_id_with_name(old_name)
        self.project_id_names[id] = new_name

        with open('OTT_projects.txt','w') as f:
            for id in self.project_id_names:
                f.write(self.project_id_names[id]+", "+str(id)+"\n")
            for id in self.archived_project_id_names:
                f.write("--"+self.archived_project_id_names[id]+", "+str(id)+"\n")


    # ******** project **********
    def add_entry(self, project_id, start_time, end_time, log_file):
        if self.project_id_names[project_id] in self.track_record:
            self.track_record[self.project_id_names[project_id]].append((str(start_time), str(end_time), (end_time-start_time).seconds))
        else:
            self.track_record[self.project_id_names[project_id]] = [(str(start_time), str(end_time), (end_time-start_time).seconds)]
        with open(log_file, 'a') as f:
            f.write(str(project_id) + ", "+ str(start_time) + ", " + str(end_time) + ", " + str((end_time-start_time).seconds)+"\n")


