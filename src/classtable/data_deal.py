import pandas as pd
import time
from datetime import datetime
from classtable.data import data_combine, ClassTable

def sort_dict_by_tuplekey(d:dict[tuple,ClassTable])->dict[tuple,ClassTable]:
    return dict(sorted(d.items(), key=lambda item: (item[0][0], item[0][1])))

class Subject:
    def __init__(self):
        self.inf_ls = data_combine()
    

    def _make_sort_dict(self):
        '''
        Docstring 为之后的 fill in 课程做准备，目的是创作 dict 以prefer/priority， category，day 的tuple为key
            
        :param self: Description
        '''
        self.sort_dict_pref = dict()
        self.sort_dict_prir = dict()
        
        for i in self.inf_ls:
            if i.preferred:
                self.sort_dict_pref.setdefault((i.priority, i.category), []).append(i)
            else:
                self.sort_dict_prir.setdefault((i.priority, i.category), []).append(i)
        self.sort_dict_pref = sort_dict_by_tuplekey(self.sort_dict_pref)
        self.sort_dict_prir = sort_dict_by_tuplekey(self.sort_dict_prir)
        # for k, v in self.sort_dict_prir.items():
        #     print (v[0].category, v[0].priority)
            
    def _deal_sort_dict(self, sorted_dict:dict[tuple[str, str], ClassTable])->None:
        '''
        Docstring for _deal_sort_dict
        
        :param self: Description
        :param sorted_dict: Description
        :type sorted_dict: dict[tuple[str, str], ClassTable]
        '''
        for k, v_ls in sorted_dict.items():
            if self.class_category.get(v_ls[0].category, 0) >= 1: # category >2 => skip
                continue
            for v in v_ls:
                if self.class_day.get(v.day, 0) >= 2: 
                    continue
                self.class_new_ls.append(v)
                self.class_category[v.category] = self.class_category.get(v.category,0) + 1
                self.class_day[v.day] = self.class_day.get(v.day, 0) + 1
        
            
    def arrange_class(self):
        self.class_new_ls = list()
        self.class_category = dict() # 用来统计当前 有多少 category 被book
        self.class_day = dict() # 用来统计当前有多少 day 被book
        
        # prepare two sort dict
        self._make_sort_dict()
        
        self._deal_sort_dict(self.sort_dict_pref)
        self._deal_sort_dict(self.sort_dict_prir)
        
         
            
    def sort_inflist_for_table(self):
        '''
        purpose is to sort the information for the further usage. 

        '''
        # k_list = ['start_time_r', 'day']
        # self.class_new_ls = []
        
        self.class_new_ls = sorted(self.class_new_ls, key = lambda x: (x.day, x.start_time_dt))
        return self.class_new_ls

    
    

def run():
    s = Subject()

    
    s.arrange_class()
    # s._make_sort_dict()
    inf_ls = s.sort_inflist_for_table()
    df = pd.DataFrame([i.model_dump() for i in inf_ls])
    print (df)
    

if __name__ == '__main__':
    
    run()
    
    