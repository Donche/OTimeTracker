from hashlib import new
import pandas as pd
from datetime import datetime, date
from os.path import exists
import uuid
import csv

class TrackData():
    def __init__(self):
        self.project_id_names = {}
        self.archived_project_id_names = {}
        self.track_records = pd.DataFrame()
        self.track_records_group = pd.DataFrame()

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
        if not exists(log_file):
            print("no log file")
            return
        with open(log_file, 'r') as f:
            track_record = []
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
                track_record.append([name, datetime.fromisoformat(row[1].strip()), 
                        datetime.fromisoformat(row[2].strip()), int(row[3])])
        self.track_records = pd.concat([self.track_records, pd.DataFrame(
                track_record, columns=['name', 'start', 'end', 'duration'])])
        self.track_records = self.track_records.set_index('start')
        self.track_records_group = self.track_records.groupby(['name'])

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


    # ******** records **********
    def add_entry(self, id, start_time, end_time, log_file):
        new_df = pd.DataFrame(
            [[self.project_id_names[id], start_time, end_time, 
            (end_time-start_time).seconds]], 
            columns=['name', 'start', 'end', 'duration']).set_index('start') 
        self.track_records = pd.concat([self.track_records, new_df])
        self.track_records_group = self.track_records.groupby(['name'])
        with open(log_file, 'a') as f:
            f.write(str(id) + ", "+ str(start_time) + ", " + str(end_time) 
            + ", " + str((end_time-start_time).seconds)+"\n")


    # ******** data **********
    def record_projects(self):
        return self.track_records_group.groups.keys()

    def proj_duration_at_day(self, name, day):
        if str(day.date()) in self.track_records.index:
            return self.track_records_group.get_group(name).loc[str(day.date())]['duration'].sum()
        else:
            return 0

    def total_duration_at_day(self, day, name):
        if str(day.date()) in self.track_records.index:
            return self.track_records_group.get_group(name).loc[str(day.date())]['duration'].sum()
        else:
            return 0

    def total_duration(self, name):
        return self.track_records_group.get_group(name)['duration'].sum()
