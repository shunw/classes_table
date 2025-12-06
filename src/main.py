import pandas as pd
import time
from datetime import datetime

class SingleSub:
  def __init__(self, one_s:pd.Series):
    self.start_time = one_s.start_time
    self.class_name = one_s.class_name
    self.class_loc = one_s.location
    self.class_category = one_s.category
    self.class_dis = one_s.home_dis
    self.class_priority = one_s.priority
    self.day = one_s.day

    self.start_time_r = None
  
  def dict_form(self):
    return (self.__dict__)

  def __str__(self):
    # return f'class:{self.class_name}; day:{self.day}; start_time:{self.start_time}; loc:{self.class_loc}; category:{self.class_category}'
    return f'{self.__dict__}'



class Subject:
  def __init__(self):
    pass

  def inf_list_create(self):
    loc_df = pd.read_csv('db/loc_inf.csv')
    class_inf_df = pd.read_csv('db/class_inf.csv')
    class_all_df = pd.read_csv('db/class_all.csv')
    df = pd.merge(class_all_df,class_inf_df, on = 'class_id', how = 'left')
    self.df = pd.merge(df, loc_df, on = 'loc_id', how = 'left')

    self.inf_ls = list()
    for ind in self.df.index:
      self.inf_ls.append(SingleSub(self.df.loc[ind])) 
      self.inf_ls[0].dict_form()
      
    return self.inf_ls
    
  
  def _refine_new_time(self,time_str):
    h, m = time_str.split(':')
    if int(m) - 30 > 15: 
      return f'{int(h)+1}:00'
    elif (int(m) - 30 <= 15) and (int(m) - 30 > -15):
      return f'{int(h)}:30'
    elif int(m) - 30 <= -15:
      return f'{int(h)}:00'
    else:
      return 'something wrong'
    
  def deal_time_slot_4df(self):
    '''
    this is to make the time into the block, like (11:25,11:40) -> 11:30; (11:05, 10:50)-> 11:00; 
    
    :param self: Description
    '''
    st = 'start_time'
    stn = 'start_time_r'
    self.df[stn] = None
    
    for i in self.df.index:
      self.df.loc[i, stn] = self._refine_new_time(self.df.loc[i, st])
    self.df[stn] = pd.to_datetime(self.df[stn], format = '%H:%M').dt.time
    self.min_p = min(list(self.df[stn].unique()))
    self.max_p = max(list(self.df[stn].unique()))
    return self.df

  def deal_time_slot(self):
    '''
    this is for the information list, this is to make the time into the block, like (11:25,11:40) -> 11:30; (11:05, 10:50)-> 11:00; 
    
    :param self: Description
    '''
    st = 'start_time'
    # stn = 'start_time_r'
 
    self.min_p, self.max_p = None, None
    for i in self.inf_ls:
      i.start_time_r = datetime.strptime(self._refine_new_time(i.start_time), '%H:%M').time()
      if self.min_p is None: 
        self.min_p = i.start_time_r
      elif self.min_p > i.start_time_r:
        self.min_p = i.start_time_r
      
      if self.max_p is None:
        self.max_p = i.start_time_r
      elif self.max_p < i.start_time_r:
        self.max_p = i.start_time_r

  def convert_inflist_to_df(self):
    data = []
    for i in self.inf_ls:
      data.append(i.dict_form())
    df = pd.DataFrame(data)
    return df
    # pass

  def __str__(self):
    pass

class Timetable:
  def __init__(self):
    pass

  def add_subject(self, day, period, subject):
    if day not in self.schedule:
        self.schedule[day] = {}
        self.schedule[day][period] = subject

  def get_subject(self, day, period):
    return self.schedule[day][period]


if __name__ == '__main__':
  s = Subject()

  s.inf_list_create()

  s.deal_time_slot()
  s.convert_inflist_to_df()
  
  
  