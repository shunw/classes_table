from pydantic import BaseModel, Field, field_validator, model_validator, ValidationInfo
from enum import Enum
from typing import Optional
import csv
import pandas as pd
from datetime import datetime

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
    

class ClassInfo(BaseModel):
    """
    class info
    """
    class_id: int
    class_name: str
    category: ClassCategory
    priority: int
    period_limit: bool
    comment: Optional[str] = None
    
class LocationInfo(BaseModel):
    loc_id: int
    location: str
    home_dis: float
    # https://docs.pydantic.dev/latest/concepts/alias/
    loc_close: str = Field(description="the nearest city center", alias="close")
    
    
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
                self.start_time_dt = datetime.strptime(t_str, custom_format).time()
                
            except ValueError as e:
                
                raise ValueError(f"时间字符串 '{t_str}' 与预期格式 '%H/%M' 不匹配。") from e
        return self
    
class ClassTable(BaseModel):
    start_time: str
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

def data_combine() -> list:
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
    for i in class_schedule:
        
        cc = next(filter(lambda p: p.class_id == i.class_id, class_info), None)
        ll = next(filter(lambda p: p.loc_id == i.loc_id, loc_info), None)
        d = {**i.model_dump(), **cc.model_dump(), **ll.model_dump()}

        # cd = 
        final_schedule.append(ClassTable.model_validate(d))
        # break
    # print (final_schedule)
    return final_schedule


# from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional



def run():
    class_schedule = load_class_schedule_infos('db/class_schedule.csv')
    print (class_schedule)
    
# def data_to_df(data_ls:list[ClassTable] = data_combine()) -> pd.DataFrame:
#     dict_ls = [d.model_dump() for d in data_ls]
#     df = pd.DataFrame(dict_ls)
#     print (df)
    
    

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
    run()