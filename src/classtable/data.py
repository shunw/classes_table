from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional
import csv

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
    start_time: str
    class_id: int
    day: int
    loc_id: int
    preferred: bool
    
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
    
if __name__ == "__main__":
    import argparse, os, sys
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="csv file to parse", required=True)
    parser.add_argument("-t", "--type", help="data type", choices=["class", "classsub", "location"], default="class")
    
    args = parser.parse_args()
    csv_file = args.file
    if not os.path.exists(csv_file) or not os.path.isfile(csv_file):
        print(f"not a file: {csv_file}")
        sys.exit(0)
    type = args.type
    load_func = load_class_infos
    if type == "classsub":
        load_func = load_class_schedule_infos
    elif type == "location":
        load_func = load_location_infos
    print("sub data: ", [item.model_dump() for item in load_func(csv_file)])