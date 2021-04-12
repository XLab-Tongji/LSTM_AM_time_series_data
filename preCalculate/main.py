# coding=UTF-8（等号换为”:“也可以）
import rpt2csv
from pathlib import Path
import pandas as pd
import time
import datetime
import matplotlib.pyplot as plt
import numpy as np

output = '../Data/OKCSV/'
outputs = '../Data/ExtractCSV/'
result = '../Data/result/'
picture='../Data/picture/'

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
                               '100004', '100003', '100005', '100002', '101403', '101404','101420']]

    ExtractData.columns = ["时间", "state", "气垫仓压力", "泥浆液位", "贯入度",
                           "刀盘扭矩", "刀盘转速", "总推进力", "推进速度", "进浆流量", "出浆流量","泥水仓压力"]

    WorkData = ExtractData[(ExtractData.state == 1.00000)&(ExtractData['泥浆液位']>-4)&(ExtractData['泥浆液位']<4)
                           & (ExtractData['气垫仓压力'] > 1)&(ExtractData['气垫仓压力']<5)]
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

    # example = pd.DataFrame(columns=["时间", "state", "气垫仓压力", "泥浆液位", "贯入度",
    #                                 "刀盘扭矩", "刀盘转速", "总推进力", "推进速度", "进浆流量", "出浆流量","泥水仓压力"])

    example = pd.DataFrame(columns=["气垫仓压力", "泥浆液位", "贯入度",
                                    "刀盘扭矩", "刀盘转速", "总推进力", "推进速度", "进浆流量", "出浆流量","泥水仓压力"])

    datas=data.iloc[:,2:]
    while(Indexs + period < len(data)):

        start = data.iloc[Indexs, [1]][0]
        end = data.iloc[Indexs + period, [1]][0]

        Start = time.mktime(time.strptime(start, '%Y-%m-%d %H:%M:%S.000'))
        End = time.mktime(time.strptime(end, '%Y-%m-%d %H:%M:%S.000'))

        # Start = time.mktime(time.strptime(start, '%Y/%m/%d %H:%M:%S'))
        # End = time.mktime(time.strptime(end, '%Y/%m/%d %H:%M:%S'))

        if(End - Start<=Interval):
            # print("可以提取处理+1")
            temp= datas.iloc[Indexs:Indexs+period, 1:]
            lisZero = [int(Indexs/step)]*period
            temp.index = lisZero

            average=temp.mean()
            number3=average["气垫仓压力"]
            number4=average["泥浆液位"]
            temp["气垫仓压力"]= number3
            temp["泥浆液位"]= number4
            example = pd.concat([example, temp])
        # else:
        #     print("中间间隔太大+1")

        Indexs += step

    # print(example.head(120))
    example.to_csv(result + resultname, mode='a', encoding='utf-8')

    print("我们以为"+str(period)+"s为时间段，间隔"+str(step)+"s提取时序数据")
    print("已经处理完"+str(resultname)+"文件")

def PrintData(period,resultname):

    Blank = ['2020.11.13.csv', '2020.11.14.csv']
    if resultname in Blank:
        return
    filename = outputs + resultname
    data = pd.read_csv(filename, low_memory=False)  # 读取csv文件

    if(len(data) == 0):
        return



    """
    查看每一小段的抖动
    """
    # temp = int(len(data)/period)
    # for i in range(temp):
    #     some = data.iloc[i:i+period, 3:4]
    #     some = some.astype(float)
    #     print(some)
    #     some.plot()
    #     plt.savefig(picture+'Zsplit'+ str(i) +resultname + '.jpg')
    #     plt.close()
    #     if(i>=40):
    #         break

    # temp = int(len(data)/period)
    # for i in range(temp):
    #     some = data.iloc[i:i+period, 4:5]
    #     some = some.astype(float)
    #     print(some)
    #     some.plot()
    #     plt.savefig(picture+'split'+ str(i) +resultname + '.jpg')
    #     plt.close()
    #     if(i>=40):
    #         break

    """
        查看气垫仓压力
     """
    # some = data.iloc[:, 3:4]
    # some = some.astype(float)
    # print(some)
    # some.plot()
    # plt.savefig(picture+'Z'+resultname + '.jpg')
    """
        查看泥浆液位
    """
    # somes = data.iloc[:, 4:5]
    # somes = somes.astype(float)
    # print(somes)
    # somes.plot()
    # plt.savefig(picture+resultname+'.jpg')

    print("OK")


if __name__ == '__main__':
    # 设置字体为楷体
    plt.rcParams['font.sans-serif'] = ['KaiTi']
    plt.rcParams['font.family'] = ['sans-serif']

    # 分次进行数据预处理

    # convertRPT()

    # 处理直接zip提取的数据。
    # now1 = datetime.date(2020, 12, 7).strftime('%Y/%m/%d')
    # start1 = datetime.date(2020, 11, 3).strftime('%Y/%m/%d')
    # FileList = pd.date_range(start1, now1).strftime("%Y.%m.%d").to_list()
    # FileList.remove('2020.11.13')
    # FileList.remove('2020.11.14')
    #
    #
    # for i in range(len(FileList)):
    #     filename = output + suffix[i] + '.csv'
    #     ExtractDatas(filename, outputs + FileList[i] + '.csv')  # 读取csv文件
    #     print(filename)
    #     print(outputs + FileList[i] + '.csv')
    now1 = datetime.date(2020, 12, 7).strftime('%Y/%m/%d')
    start1 = datetime.date(2020, 11, 2).strftime('%Y/%m/%d')
    FileList = pd.date_range(start1, now1).strftime("%Y.%m.%d").to_list()
    print(FileList)

    for i in range(len(FileList)):
        if i == len(FileList) - 1:
            break
        payloadsome = payloadsome.replace(FileList[i], FileList[i + 1])
        print(payloadsome)
        ExcavationData(60, 30, payloadsome + '.csv')
        # PrintData(60,payloadsome+'.csv')

    print('Finish')
