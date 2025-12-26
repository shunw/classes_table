import pandas as pd
import time
from datetime import datetime
from classtable.data import data_combine


class Subject:
    def __init__(self):
        self.inf_ls = data_combine()
        # print (len(self.inf_ls))
    
    def _refine_new_time(self,time_str:str):
        h, m = time_str.split(':')
        if int(m) - 30 > 15: 
            return f'{int(h)+1}:00'
        elif (int(m) - 30 <= 15) and (int(m) - 30 > -15):
            return f'{int(h)}:30'
        elif int(m) - 30 <= -15:
            return f'{int(h)}:00'
        else:
            return 'something wrong'
        

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

    def arrange_time_table(self):
        
        # collect the information of arranged class
        arg_dict = dict() # {group_key: [case1, case2, ... ], group_key1: [case5, case6, ...]}
        # group_key_fd = # (preferred, priority, category)
        
        # put the preferred item
        self.inf_ls_org = []
        for i in self.inf_ls:
            if i.preferred == True: 
                self.inf_ls_org.append(i)
                self.arrange_category[i.class_category] += 1
                i.selected = True
                continue
        
        # check the (priority and the category)
        for p in self.priority_lvl:
            for i in self.inf_ls:
                if self.arrange_category[i.class_category] > 0:
                    continue
                if self.inf_ls.class_priority != p:
                    continue
        
         
            
    def sort_inflist_for_table(self):
        '''
        purpose is to sort the information for the further usage. 

        '''
        # k_list = ['start_time_r', 'day']
        self.inf_ls_new = []
        
        self.inf_ls_new = sorted(self.inf_ls, key = lambda x: (x.start_time_r, x.day))
        return self.inf_ls_new

    
    

def run():
    s = Subject()

    # s.deal_time_slot()
    # # s.arrange_time_table()
    
    # inf_ls = s.sort_inflist_for_table()
    # df = s.convert_inflist_to_df(inf_ls)
    # print (df)

if __name__ == '__main__':
    
    run()
    
    