# coding=UTF-8（等号换为”:“也可以）
import rpt2csv
from pathlib import Path
import pandas as pd
import time
import datetime
import numpy as np

output = '../Data/OKCSV/'
outputs = '../Data/ExtractCSV/'
result = '../Data/result/'

suffix = ['11.03', '11.04', '11.05', '11.06', '11.07', '11.08', '11.09', '11.10',
              '11.11', '11.12', '11.15', '11.16', '11.17', '11.18',
              '11.19', '11.20', '11.21', '11.22', '11.23', '11.24', '11.25', '11.26',
              '11.27', '11.28', '11.29', '11.30', '12.01', '12.02', '12.03', '12.04',
              '12.05', '12.06', '12.07']

payloadsome = "2020.11.02"

Interval = 70

def convertRPT():
    """
    :return:
    转化文件格式只适用于python2.7
    """
    p = Path("../")  # 初始化构造Path对象

    FileList = list(p.glob("**/*.rpt"))  # 得到所有的markdown文件

    print(len(FileList))

    for i in range(len(FileList)):
        with open(str(FileList[i])) as inputFile:
            with open(output + suffix[i] + '.csv', 'wb') as outputFile:
                rpt2csv.convert(inputFile, outputFile)

        print("this is the " + str(i) + "'th")


def ExtractDatas(filename,outFile):
    """
    :param filename: 输入文件名
    :param outFile: 输出文件名
    :return:
    提取感兴趣的列
    """
    data = pd.read_csv(filename, low_memory=False)  # 读取csv文件

    # "气垫仓压力和泥浆液位，贯入度,刀盘扭矩,刀盘转速,总推进力,推进速度,进浆流量,出浆流量。"
    ExtractData = data.loc[:, ['t', '100006', '101465', '860424', '100395',
                               '100004', '100003', '100005', '100002', '101403', '101404']]

    ExtractData.columns = ["时间", "state", "气垫仓压力", "泥浆液位", "贯入度",
                           "刀盘扭矩", "刀盘转速", "总推进力", "推进速度", "进浆流量", "出浆流量"]

    WorkData = ExtractData[(ExtractData.state == 1.00000)]
    print(ExtractData.info)
    print(WorkData.info)

    WorkData.to_csv(outFile, mode='a', encoding='utf-8')


def ExcavationData(period, step, resultname):
    """
    :param period: 表示窗口的大小，
    :param step: 表示窗口移动距离
    :param resultname: 表示输出文件
    :return:
    最后提取时序数据
    """
    Blank=['2020.11.13.csv', '2020.11.14.csv']
    if resultname in Blank:
        return
    filename = outputs + resultname
    data = pd.read_csv(filename, low_memory=False)  # 读取csv文件
    print("数据行数"+str(data.shape[0]))
    if(data.shape[0]<period):
        print("已经处理完" + str(resultname) + "文件")
        print("当天没有掘进工作")
        return

    Indexs = 0

    example = pd.DataFrame(columns=["时间", "state", "气垫仓压力", "泥浆液位", "贯入度",
                                    "刀盘扭矩", "刀盘转速", "总推进力", "推进速度", "进浆流量", "出浆流量"])

    while(Indexs + period < len(data)):

        start = data.iloc[Indexs, [1]][0]
        end = data.iloc[Indexs + period, [1]][0]

        Start = time.mktime(time.strptime(start, '%Y-%m-%d %H:%M:%S.000'))
        End = time.mktime(time.strptime(end, '%Y-%m-%d %H:%M:%S.000'))

        # Start = time.mktime(time.strptime(start, '%Y/%m/%d %H:%M:%S'))
        # End = time.mktime(time.strptime(end, '%Y/%m/%d %H:%M:%S'))

        if(End - Start<=Interval):
            # print("可以提取处理+1")
            temp= data.iloc[Indexs:Indexs+period, 1:]
            lisZero = [int(Indexs/step)]*period
            temp.index = lisZero

            example = pd.concat([example, temp])
        # else:
        #     print("中间间隔太大+1")

        Indexs += step

    # print(example.head(120))
    example.to_csv(result + resultname, mode='a', encoding='utf-8')

    print("我们以为"+str(period)+"s为时间段，间隔"+str(step)+"s提取时序数据")
    print("已经处理完"+str(resultname)+"文件")

# def PreChangeTag(filename, period):
#     """
#     :param filename: 文件名
#     :param period: 间隔
#     :return:
#     修改文件tag
#     """
#     filepath = outputs + filename
#     data = pd.read_csv(filepath, low_memory=False)  # 读取csv文件
#     print("数据行数" + str(data.shape[0]))
#
#     Indexs = 0
#     while (Indexs + period < len(data)):
#         print("")

if __name__ == '__main__':

    # 分次进行数据预处理

    # convertRPT()


    # for i in range(len(suffix)):
    #     filename = output + suffix[i]+'.csv'
    #     ExtractDatas(filename, outputs + suffix[i]+'.csv') # 读取csv文件

    now1 = datetime.date(2020,12, 7).strftime('%Y/%m/%d')
    start1 = datetime.date(2020, 11, 2).strftime('%Y/%m/%d')

    FileList = pd.date_range(start1, now1).strftime("%Y.%m.%d").to_list()

    print(FileList)

    for i in range(len(FileList)):
        if i == len(FileList) - 1:
            break
        payloadsome = payloadsome.replace(FileList[i], FileList[i + 1])
        print(payloadsome)
        # PreChangeTag(60, payloadsome + '.csv')
        ExcavationData(60, 30, payloadsome + '.csv')

    print('Finish')
