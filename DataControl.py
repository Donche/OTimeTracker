from datetime import datetime
from TrackData import TrackData

class DataControl():
    def __init__(self):
        self.data = TrackData()
        self.working_project = ""
        self.working_id = 0
        self.start_time = 0

        log_file = '{}-{}.log'.format(datetime.now().year, datetime.now().month)
        self.data.loadHistory(log_file)

    # ******** project **********
    def has_project(self, name):
        return self.data.has_project(name)

    def try_add_project(self, name):
        return self.data.try_add_project(name)

    def archive_project(self, name):
        return self.data.archive_project(name)

    def rename_project(self, old_name, new_name):
        return self.data.rename_project(old_name, new_name)


    # ******** times **********
    def get_total(self, name):
        if name in self.data.record_projects():
            return self.data.total_duration(name)
        else:
            return 0

    def get_today_total(self, name):
        if name in self.data.record_projects():
            return self.data.total_duration_at_day(name, datetime.now())
        else:
            return 0

    def start_working(self, name):
        self.working_project = name
        self.start_time= datetime.now()
        self.working_id = self.data.get_id_with_name(name)

    def get_working_time(self):
        return datetime.now()-self.start_time


    def stop_working(self):
        end_time = datetime.now() 
        log_file = '{}-{}.log'.format(self.start_time.year, self.start_time.month)
        self.data.add_entry(self.working_id, self.start_time, end_time, log_file)




