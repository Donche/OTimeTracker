from datetime import datetime
from TrackData import TrackData
import pandas as pd
import calmap

class DataControl():
    def __init__(self):
        self.data = TrackData()
        self.working_project = ""
        self.working_id = 0
        self.start_time = 0

        self.data.loadHistory()

    # ******** setting **********
    def set_data_path(self, data_path):
        self.data.set_data_path(data_path)
    

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
            return self.data.proj_duration_at_day(name, datetime.now())
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
        self.data.add_entry(self.working_id, self.start_time, end_time)


    # ******** times **********
    def init_plot(self):
        now = datetime.now()
        self.target_year = str(now.year)
        self.target_month = str(now.year) + "-" + str(now.month)
        self.target_week = int(now.strftime("%V"))
        self.tmp = self.data.track_records.groupby([self.data.track_records.index.date, 'name']).sum().reset_index(level=1).pivot(columns='name', values='duration')
        self.tmp.index = pd.to_datetime(self.tmp.index)
        self.tmp['week']  = self.tmp.index.strftime("%V")

    def all_proj_heatmap(self, fig):
        ax = fig.add_subplot(len(self.data.project_id_names)+1, 1, 1)
        axes = [ax]
        calmap.yearplot(self.data.track_records['duration'], cmap='YlGn', 
                fillcolor='lightgrey',daylabels='MTWTFSS',
                dayticks=[0,2,4,6], linewidth=0.3, year=2022, ax=ax)
        ax.set_title("all projects")
        i = 2
        for name in self.data.project_id_names.values():
            axes.append(self.proj_heatmap(name, fig, i))
            i += 1
        return axes


    def proj_heatmap(self, name, fig, index):
        ax = fig.add_subplot(len(self.data.project_id_names)+1, 1, index)
        if name in self.data.track_records_group.groups:
            calmap.yearplot(self.data.track_records_group.get_group(name)['duration'], cmap='YlGn', 
                    fillcolor='lightgrey',daylabels='MTWTFSS',
                    dayticks=[0,2,4,6], linewidth=0.3, year=2022, ax=ax)
        else:
            ax.text(0.5,0.5,"no data", horizontalalignment='center', verticalalignment='center')

        ax.set_title(name)
        return ax
    
    def bar_plot(self, fig, scale):
        ax = fig.add_subplot(111)
        res = pd.DataFrame()
        if scale == "week":
            if self.target_year in self.tmp.index :
                res = self.tmp.loc[self.target_year][self.tmp['week']==self.target_week]
        elif scale == "month":
            if self.target_month in self.tmp.index:
                res = self.tmp.loc[self.target_month]
        elif scale == "year":
            if self.target_year in self.tmp.index:
                res = self.tmp.loc[self.target_year]
        else:
            res = self.tmp
        if len(res.index) == 0:
            return [ax]
        res.plot.bar(stacked=True,  ylabel='Hours', xlabel='Date', title='yes', ax=ax, rot=40)
        return [ax]

    def pie_chart(self, fig, scale):
        ax = fig.add_subplot(111)
        print(scale)
        if scale == "week":
            if self.target_year in self.data.track_records.index:
                tmp = self.data.track_records.loc[self.target_year].groupby('week')
                if self.target_week in tmp.groups.keys():
                    tmp = tmp.get_group(self.target_week).groupby('name')['duration'].sum()
                else:
                    return [ax]
            else:
                return [ax]
        elif scale == "month":
            if self.target_month in self.data.track_records.index:
                tmp = self.data.track_records.loc[self.target_month].groupby('name')['duration'].sum()
            else:
                return [ax]
        elif scale == "year":
            if self.target_year in self.data.track_records.index:
                tmp = self.data.track_records.loc[self.target_year].groupby('name')['duration'].sum()
            else:
                return [ax]
        else:
            tmp = self.data.track_records_group['duration'].sum()
        tmp.plot.pie(y='duration', title='yes', ax=ax)
        return [ax]
    
    def reset_range(self):
        now = datetime.now()
        self.target_year = str(now.year)
        self.target_month = str(now.year) + "-" + str(now.month)
        self.target_week = int(now.strftime("%V"))

    def update_range(self, scale, prev):
        if prev == 0:
            self.reset_range()
        if scale == "week":
            self.target_week = str(int(self.target_week) + prev)
        elif scale == "month":
            self.target_month = self.target_year + "-" + str(int(self.target_month.split("-")[-1]) + prev)
        elif scale == "year":
            self.target_year = str(int(self.target_year) + prev)