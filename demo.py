#!python
import pandas as pd
from datetime import  datetime
import argparse
print(pd.__version__)

def process_data(file_path,out_file_name=""):
    now=datetime.now()
    timeStr=now.strftime("_%Y-%m-%d_%H时%M分")
    if out_file_name=='':
        out_file_name="./data"+timeStr+".csv"

    s = pd.read_csv(file_path, skiprows=18)
    res = s.query("(Evnt_Name=='Whisker - Display Image' and Group_ID==6) or (Evnt_Name=='Touch Down Event' and Group_ID==7 and Arg2_Name!='(NoImageOrVideo)')")
    print(res)
    res = res.sort_values(by=['Evnt_Time', 'Arg1_Value'])
    res.to_csv('./'+out_file_name, sep=',', header=True, index=False)

def parse_args():
    desc = "实验数据处理相关的筛选程序 从数据中筛选处所需要的实验条件和结果数据"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-i",'--input_file',help="输入CSV数据的地址 ",required=True)
    parser.add_argument("-o",'--output',help="输出数据的名字 format: xxx.csv 例如 a.csv 会在当前目录生成筛选后的数据",default="")
    return parser.parse_args()



if __name__ == '__main__':
    args = parse_args()
    if args is None:
        exit()

    process_data(args.input_file,args.output)




