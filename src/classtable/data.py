from pydantic import BaseModel, Field, field_validator, model_validator, ValidationInfo
from enum import Enum
from typing import Optional
import csv
import pandas as pd
from datetime import datetime, timedelta

class ClassCategory(str, Enum):
    ballet = "ballet"
    dance = "dance"
    fat = "fat"
    muscle = "muscle"
    low_body = "low_body"
    mid_body = "mid_body"
    up_body = "up_body"
    yoga = "yoga"
    zumba = "zumba"
    
    @classmethod
    def list_all(cls):
        return list(cls._member_map_.keys())

class ClassInfo(BaseModel):
    """
    class info
    """
    class_id: Optional[int] = None
    class_name: str
    category: Optional[ClassCategory] = None
    priority: Optional[int] = None
    period_limit: Optional[bool] = None
    comment: Optional[str] = None
    
    def __eq__(self, value):
        if isinstance(value, ClassInfo):
            if value.class_name != self.class_name: return False
        return False
    
class LocationInfo(BaseModel):
    loc_id: Optional[int] = None
    location: str
    home_dis: float
    # https://docs.pydantic.dev/latest/concepts/alias/
    loc_close: Optional[str|None] = Field(description="the nearest city center", alias="close")
    
    def __eq__(self, value):
        if isinstance(value, LocationInfo):
            if value.location != self.location: return False
            return True
        return False
    
def refine_dt(timedata:datetime):
    '''
    Docstring for refine_dt
    this is to make the time data to 30 or 00
    
    :param timedata: Description
    :type timedata: datetime
    '''
    h = timedata.hour
    m = timedata.minute
    
    try:
        if m - 30 > 15: 
            new = timedata.replace(hour=h+1, minute= 0)
            
            
        elif (m - 30 <= 15) and (m - 30 > -15):
            new = timedata.replace(minute = 30)
            
        elif m - 30 <= -15:
            new = timedata.replace(minute = 0)
    
        return new
    except ValueError as e:
        raise ValueError(f'the input {timedata} is something wrong') from e
    
    
class ClassScheduleInfo(BaseModel):
    start_time_str: str = Field(alias = 'start_time')
    start_time_dt: Optional[datetime] = None
    class_id: int
    day: int
    loc_id: int
    preferred: bool
    
    @model_validator(mode = 'after')
    def parse_str_to_datatime(self):
        # 从values数据中获取已验证的字符串字段值
        t_str = self.start_time_str
        if t_str:
            # csv中的自定义格式
            
            custom_format = "%H:%M"
            try: 
                # 尝试解析字符串
                temp_dt = datetime.strptime(t_str, custom_format)
                self.start_time_dt = refine_dt(temp_dt)
                # print (self.start_time_dt.hour, self.start_time_dt.minute)
                
            except ValueError as e:
                
                raise ValueError(f"时间字符串 '{t_str}' 与预期格式 '%H/%M' 不匹配。") from e
        return self
    
    def __eq__(self, value):
        if isinstance(value, ClassScheduleInfo):
            if value.start_time_str != self.start_time_str: return False
            if value.class_id != self.class_id: return False
            if value.day != self.day: return False
            if value.loc_id != self.loc_id: return False
            return True
        return False
            
        # Sreturn super().__eq__(value)
    def __str__(self):
        return f'start_time: {self.start_time_str}\nclass_id: {self.class_id}\nday: {self.day}\nloc_id: {self.loc_id}'    
    
class ClassTable(BaseModel):
    start_time_str: str
    start_time_dt: datetime
    day: int
    preferred: bool
    class_name: str
    category: ClassCategory
    priority: int
    period_limit: bool
    comment: Optional[str] = None
    location: str
    home_dis: float
    loc_close: str

class BlockTable(BaseModel):
    '''
    Docstring for BlockTable
        for the event blocked, which will impact the class chosen
    '''    
    start_time_str: str = Field(alias='start_time')
    start_time_dt: Optional[datetime] = None
    end_time_str: str = Field(alias= 'end_time')
    end_time_dt: Optional[datetime] = None
    loc: str
    event: str
    day: int
    
    @model_validator(mode = 'after')
    def parse_str_to_datatime(self):
        # 从values数据中获取已验证的字符串字段值
        # t_str = self.start_time_str
        if self.start_time_str or self.end_time_str:
            # csv中的自定义格式
            
            custom_format = "%H:%M"
            try: 
                # 尝试解析字符串
                self.start_time_dt = datetime.strptime(self.start_time_str, custom_format)
                self.end_time_dt = datetime.strptime(self.end_time_str, custom_format)
                # self.start_time_dt = refine_dt(temp_dt)
                # print (self.start_time_dt.hour, self.start_time_dt.minute)
                
            except ValueError as e:
                
                raise ValueError(f"时间字符串 '{self.start_time_str} or {self.end_time_str}' 与预期格式 '%H/%M' 不匹配。") from e
        return self
    
    
    
def load_class_infos(csv_file: str) -> list[ClassInfo]:
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [ClassInfo.model_validate(row) for row in reader]
    
def load_location_infos(csv_file: str) -> list[LocationInfo]:
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [LocationInfo.model_validate(row) for row in reader]
    
def load_class_schedule_infos(csv_file: str) -> list[ClassScheduleInfo]:
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [ClassScheduleInfo.model_validate(row) for row in reader]

def load_block_schedule(csv_file: str) -> list[BlockTable]:
    with open(csv_file, 'r', encoding= 'utf-8') as f:
        reader = csv.DictReader(f)
        return [BlockTable.model_validate(row) for row in reader]
def be_blocked(cls_time:datetime, block_time_s:datetime, block_time_e:datetime) -> bool:
    '''
    block_time_s: start point of the block time
    block_time_e: end point of the block time
    cls_time: class time
    return True means: yes, this time is blocked; 
    return False means: no, this time is not blocked;
    
    先处理 block 时间的情况
    不能上的情况：
    如果课程的开始时间 在block的时间中间 
    如果课程的开始时间 +1h 比 block的开始 时间晚，那就说明这个课程不能上
    '''
    # print (cls_time, block_time_s, block_time_e)
    if (cls_time >= block_time_s) and (cls_time <= block_time_e):
        return True
    '''
    此处逻辑有问题!!!
    '''
    if (cls_time <= block_time_s) and cls_time + timedelta(hours=1) >= block_time_s:
        return True
    return False
    
def data_combine() -> list[ClassTable]:
    '''
    Docstring for data_create
    gather data from three csv / 将inf 组织到一起, 将几个table联系起来
        
    :return: Description
    :rtype: list
    '''
    class_schedule = load_class_schedule_infos('db/class_schedule.csv')
    class_info = load_class_infos('db/class_inf.csv')
    loc_info = load_location_infos('db/loc_inf.csv')
    final_schedule = list()
    block_schedule = load_block_schedule('db/block_schedule.csv')    
    
    for i in class_schedule:
        '''
        先处理 block 时间的情况
        不能上的情况：
        如果课程的开始时间 在block的时间中间 
        如果课程的开始时间 +1h 比 block的开始 时间晚，那就说明这个课程不能上
        '''
        flag = False # 没有block的时间
        block_ls = list(filter(lambda p: p.day == i.day, block_schedule)) # 做成list 是因为觉得可能 一天里可能会有两个block的时间
        # print (block_ls)
        for b in block_ls:
            flag = be_blocked(i.start_time_dt, b.start_time_dt, b.end_time_dt)
            # print (flag)
            if flag:
                break
        if flag:
            continue
                
            
        cc = next(filter(lambda p: p.class_id == i.class_id, class_info), None)
        ll = next(filter(lambda p: p.loc_id == i.loc_id, loc_info), None)
        d = {**i.model_dump(), **cc.model_dump(), **ll.model_dump()}

        final_schedule.append(ClassTable.model_validate(d))
    
    
    
    return final_schedule

def run():
    # class_schedule = load_block_schedule('db/block_schedule.csv')
    # dict_ls = [d.model_dump() for d in class_schedule]
    # print (pd.DataFrame(dict_ls))
    
    data_to_df()
    
def data_to_df() -> pd.DataFrame:
    data_ls = data_combine()
    data_ls = sorted(data_ls, key = lambda x: (x.day, x.start_time_dt))
    dict_ls = [d.model_dump() for d in data_ls]
    df = pd.DataFrame(dict_ls)
    print (df)
    
def get_last_id(csv_fl:str='db/test.csv', key_col:str='id')->int:
    '''
    Docstring for get_last_id
    拿到该文件中的最后一个 id
    :param csv_fl: csv 文件名 及其路径
    :key_col: 对应的文件的 主id
    :type csv_fl: str
    :return: 这个应该是这个文件中的最后一个 id
    :rtype: int
    '''    
    df = pd.read_csv(csv_fl)
    
    try: 
        return max(df[key_col])
    except KeyError as e:
        raise KeyError(f'there is no ID column in the file of {csv_fl}') from e

def show_id_n_content(csv_fl:str, key_id:str, key_name:str):
    '''
    Docstring for show_id_n_content
        这个def主要是为了 罗列 csv 表格中对应的id 及其 主要内容，
        如 如果是class inf csv 则罗列其 classid 和 class 名字
    :param csv_fl: Description
    :type csv_fl: str
    '''
    df = pd.read_csv(csv_fl)
    str_inf = ''
    for i in df.index:
        str_inf += f'{df.loc[i, key_name]} ({df.loc[i, key_id]}); '
        # print (i.class_id, i.class_name)
    print (str_inf)

def loc_inf_input_assist():
    loc_fl = 'db/loc_inf.csv'
    print('\nAssistant: Pls input your loc info: ')
    loc = input(f'\n{'='*20}\nnew location (in Chinese): ')
    home_dis = input(f'\n{'='*20}\ndistance to home (in float): ')
    close = input(f'\n{'='*20}\nclose to which area (in Chinese): ')
    comment = input (f'\n{'='*20}\nany other comments: ')
    
    cur_entry = LocationInfo(location=loc, home_dis=home_dis,close=close)
    datas = load_location_infos(loc_fl)
    if cur_entry in datas:
        print ('\nexist~~~')
    else: 
        print ('\nnew entry')
        new_line = [get_last_id(loc_fl, 'loc_id')+1, loc, home_dis,close,comment]
        
        with open(loc_fl,'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(new_line)
def class_inf_input_assist():
    clss_fl = 'db/class_inf.csv'        
    print ('\nAssistant: Pls input your class info: ')
    cls_name = input(f'\n{'='*20}\nclass name (str): ')
    prior = input(f'\n{'='*20}\npriority of this class (int): ')
    print (ClassCategory.list_all())
    category = input(f'please fill in the class category you want.: ')
    period = input(f'is this class limited by period? (True, False)')
    comment = input(f'any comment?: ')    
    
    cur_entry = ClassInfo(class_name=cls_name)
    datas = load_class_infos(clss_fl)
    if cur_entry in datas:
        print ('\nexist~~~')
    else:
        print ('\nnew entry')
        new_line = [get_last_id(clss_fl, 'class_id')+1, cls_name, prior, category, period, comment]
        
        with open(clss_fl, 'a', newline='', encoding= 'utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(new_line)
def data_input_assist_one():
    
    print("\nAssistant: Pls input your class schedule info:")
    
    start_time = input(f"\n{'='*20}\nstart_time (hh:mm): ")
    
    day = input(f'\n{'='*20}\nday (1-7): ')
    
    # below is to add the location information
    while True:
        max_id = get_last_id('db/loc_inf.csv', 'loc_id')
        print (f'\n{'='*20}\nbelow is the latest loc inf: ')
        show_id_n_content('db/loc_inf.csv', 'loc_id', 'location')
        loc_flag = input (f'Is the loc listed above you want to choose or do you want to add new? (choose_id({1}-{max_id})/ add_new(A)): ')
    
        if loc_flag.isdigit(): 
            loc_id = loc_flag
            break
        elif loc_flag.lower() == 'a': 
            loc_inf_input_assist()
            
        else:
            print ('\nthe information entered is unexpected. Please choose again.')
        
    while True:
        max_cid = get_last_id('db/class_inf.csv', 'class_id')
        print (f'\n{'='*20}\nbelow is the class inf: ')
        show_id_n_content('db/class_inf.csv', 'class_id', 'class_name')
        cls_flag = input (f'Is the class listed above you want to choose or do you want to add new? (choose_id({1}-{max_cid})/ add new (A))')
        
        if cls_flag.isdigit():
            class_id = cls_flag
            break
        elif cls_flag.lower() == 'a':
            class_inf_input_assist()
        else:
            print ('\nthe information entered is unexpected. Please choose again.')
    
    pref = input(f'\n{'='*20}\nDo you prefer this class with the schedule and the location?(True or False) ')
    
    cur_entry = ClassScheduleInfo(start_time= start_time, class_id=class_id, day = day, loc_id = loc_id, preferred= pref)
    
    datas = load_class_schedule_infos('db/class_schedule.csv')
    if cur_entry in datas:
        print (f'\n{'='*20}\nThis entry is already exist, please try next~\n')
    
    else:
        print (f'\n{'='*20}\nthe new entry is: \n{'='*20}\n{cur_entry}')
    
        csv_f = 'db/class_schedule.csv'
        new_line = [get_last_id(csv_f, 'id')+1, start_time, class_id, day, loc_id, pref]
        
        with open(csv_f,'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(new_line)
    
    
def data_input_assist_loop():
    while True: 
        data_input_assist_one()
        flag = input('If you want to exist the entry, press Q.\nif you press any other keys, we will continue the entry: ')
        if flag.lower() == 'q':
            break
    

if __name__ == "__main__":
    # import argparse, os, sys
    # parser = argparse.ArgumentParser()
    # parser.add_argument("-f", "--file", help="csv file to parse", required=True)
    # parser.add_argument("-t", "--type", help="data type", choices=["class", "classsub", "location"], default="class")
    
    # args = parser.parse_args()
    # csv_file = args.file
    # if not os.path.exists(csv_file) or not os.path.isfile(csv_file):
    #     print(f"not a file: {csv_file}")
    #     sys.exit(0)
    # type = args.type
    # load_func = load_class_infos
    # if type == "classsub":
    #     load_func = load_class_schedule_infos
    # elif type == "location":
    #     load_func = load_location_infos
    # print("sub data: ", [item.model_dump() for item in load_func(csv_file)])
    
    # loc_inf_input_assist()
    data_input_assist_loop()
    