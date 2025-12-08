import time
import pandas as pd
import numpy as np
from classtable.data_deal import Subject, SingleSub

def printGroup(group, keyHeader, keyMaxLen):
    whole = ''
    last_time = ''
    new_time_flag = True
    start_time_r = 'start_time_r'
    for item in group:
        # print ('\r')
        w = ''

        if (last_time == '') or (last_time != str(item[start_time_r])):
            last_time =  item[start_time_r]
            new_time_flag = True
        else:
            new_time_flag = False

        for i,h in enumerate(keyHeader):
            
            itemLen = keyMaxLen.get(h, str(h)) + 4
            # 补空位并居中, 判断值是否是 nan 如果是的话，用空格顶上
            if str(item[h]) == 'nan': 
                s = str('').center(itemLen, '-' if item[h] == '-' else ' ')
            else:
                s = str(item[h]).center(itemLen, '-' if item[h] == '-' else ' ')
            
            if not(new_time_flag) and (h == start_time_r):
                s = str('').center(itemLen, '-' if item[h] == '-' else ' ')

            icon = '|'
            if item[h] == '-':
                icon = '+'

            s = (icon if i == 0 else '') + s[1:len(s)] + icon
            w += s
            
        # print (w)
        whole += f'{w}\n'
    print (whole)
    return whole
        

def get_max_width(data):
    keyHeader = data[0].keys()
    # 存放每列的最大长度
    keyMaxLen = {}

    for item in data:
        for i,h in enumerate(keyHeader):
            # 计算每个属性对应的最大长度
            maxLen = max(len(h), len(str(item[h])))
            if keyMaxLen.get(h, None):
                maxLen = max(maxLen, keyMaxLen[h])
            keyMaxLen[h] = maxLen
    # print (keyMaxLen)
    return keyMaxLen

class RefineTableData:
    def __init__(self, df):
        table_data = df.to_dict('records')
        self.raw_table_data = table_data.copy()
        self.keyHeader = table_data[0].keys()
        self.keyMaxLen = get_max_width(table_data)
        self.table_data = table_data.copy()
    
    def table_data_restru_termform(self):
        # 占位项
        tag = {}
        for i,h in enumerate(self.keyHeader):
            tag[h] = '-'
        # 前后添上
        self.table_data.insert(0, tag)
        self.table_data.append(tag)
        t = {i:i for i in self.keyHeader}
        self.table_data.insert(0,t)
        self.table_data.insert(0,tag)
import numbers
class RefineTable2csv:
    '''
    this is for the SingleSub in main.py only. 
    main purpose is to make a table for the gym class view by time in vertical and day in horizontal
    '''
    def __init__(self, inf_ls:list[SingleSub]):
        self.inf_ls = inf_ls

    def get_original_df(self):
        '''
        Docstring convert the day_x to column
        :param self: Description
        '''
        ls_data = []
        for i in self.inf_ls:
            ls_data.append(i.dict_form())
        
        needed_head = ['start_time_r', 'day', 'class_inf']
        self.df = pd.DataFrame(ls_data)
        self.df['class_inf'] = self.df['class_name'] + '-' + self.df['class_loc']
        self.df = self.df[needed_head]
        
        # pivot the column as day
        self.df_table = self.df.pivot(columns= 'day', values = ['start_time_r','class_inf']) 
        
        # get the start time into the col named as start_time_combined
        for ind in self.df_table.index: 
            self.df_table.loc[ind, 'start_time_c'] = [i for i in self.df_table.loc[ind, 'start_time_r']if str(i) != 'nan' ][0]
        
        # refine the df structure: combine 5 column for the start time. and remove no use columns
        self.df_table.reset_index(inplace = True, drop=True)
        new_col = []
        for i in self.df_table.columns:
            if isinstance(i[1], numbers.Number): 
                if i[0] == 'class_inf':
                    new_col.append(f'day_{i[1]}')
                else: 
                    new_col.append(f'{i[0]}_{i[1]}')
            else:
                new_col.append(i[0])
        # print (new_col)
        self.df_table.columns = new_col
        new_head = ['start_time_c'] + [i for i in new_col if 'start_time' not in i]
        
        self.df_table = self.df_table[new_head]
        
        return self.df_table
    def opt_view(self):
        '''
        Docstring for opt_view
            remove the start time, if already exists
            remove the NaN to ''
        
        :param self: Description
        '''
        self.df_table_new =pd.DataFrame()
        col = list(self.df_table.columns)
        
        tmp_t = None
        for ind in self.df_table.index:
            for c in col: 
                # this is to judge the time already exists
                if c == 'start_time_c':
                    if tmp_t != self.df_table.loc[ind,c]:
                        self.df_table_new.loc[ind, c] = self.df_table.loc[ind, c]
                        tmp_t = self.df_table.loc[ind, c]
                    else: 
                        self.df_table_new.loc[ind, c] = ''
                else:
                    if pd.isna(self.df_table.loc[ind, c]):
                        
                        self.df_table_new.loc[ind, c] = ''
                    else:
                        self.df_table_new.loc[ind, c] = self.df_table.loc[ind, c]
        self.df_table_new.to_csv('test.csv')
                
    
    
def table_printout(table_data:list[dict]):
    '''
    Docstring for table_printout
    
    :param table_data: the data you want to printout as a table, and the format of the data is the df.to_dict('records')
    '''
    rd = RefineTableData(table_data)
    rd.table_data_restru_termform()

    # 打印后面的数据项，包括两条 --+--占位
    result = printGroup(rd.table_data, rd.keyHeader, rd.keyMaxLen)
    return result

def table_csvout(inf_ls:list[SingleSub]):
    '''
    Docstring for table_csvout
    '''
    c = RefineTable2csv(inf_ls)
    c.get_original_df() 
    c.opt_view()

def run():
    s = Subject()


    s.inf_list_create()

    s.deal_time_slot()
    
    inf_ls = s.sort_inflist_for_table()
    # df = s.convert_inflist_to_df(inf_ls)

    # data = df.to_dict('records')

    f = table_csvout(inf_ls)
    
    
    # with open('temp_output.txt', 'w') as f:
    #     f.writelines(a)    

if __name__ == '__main__':
    run()