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

class RefineTable2csv:
    '''
    this is for the SingleSub in main.py only. 
    main purpose is to make a table for the gym class view by time in vertical and day in horizontal
    '''
    def __init__(self, inf_ls:list[SingleSub]):
        self.inf_ls = inf_ls

    def get_original_df(self):
        ls_data = []
        for i in self.inf_ls:
            ls_data.append(i.dict_form())
        needed_head = ['start_time_r', 'day', 'class_name', 'class_loc']
        self.df = pd.DataFrame(ls_data)[needed_head]
        print (self.df)
        return self.df

    
    
def table_printout(table_data):
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