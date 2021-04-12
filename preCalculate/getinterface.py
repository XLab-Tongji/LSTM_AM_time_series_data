import requests
import json
import pandas as pd
import datetime

url = "http://47.101.219.119:7001/api/universal/Monitoring/MonDataEqu_shushui/where?prj=shushui&" \
      "dataset=3835049491879165952&order=ID&increase=false"

headers = {
  'Content-Type': 'application/json'
}

Interesting = ['t', '100006', '101465', '860424', '100395',
             '100004', '100003', '100005', '100002', '101403', '101404','101420']

payloadsome = "(([t]>'2021/12/07 00:00:00') and ([t]<'2021/12/07 23:59:59') and ([wm]>0))"

outputs = '../Data/ExtractCSV/'


def analyze_data(data, result):
    """
    :param data:
    :param result:
    :return:
    对于json格式数据深度递归查询
    """
    if isinstance(data, dict):
        for k, v in data.items():
            analyze_data(v, result + ".get(\"%s\")" % str(k))
    elif isinstance(data, (list, tuple)):
        for i in range(len(data)):
            analyze_data(data[i], result + "[%s]" % i)
    else:
        print(result + "=" + str(data))


def ExtractDatas(data,outFile):
    """
    :param data: 数据str
    :param outFile: 日期编号
    :return:
    提取我们感兴趣的信息
    """
    print(data)
    for k1, v1 in data.items():

        if(k1=='data'):


            df = pd.DataFrame(v1, columns=Interesting)
            df.columns=["时间", "state", "气垫仓压力", "泥浆液位", "贯入度",
                           "刀盘扭矩", "刀盘转速", "总推进力", "推进速度", "进浆流量", "出浆流量","泥水仓压力"]


            WorkData = df[(df['state'] < str(1.000001)) & (df['state'] >= str(1.00000))]
            WorkData.to_csv(outputs + outFile+'.csv', mode='a', encoding='utf-8')

            print("已经完成对" + outFile + "的数据提取")
            print(WorkData.shape)


if __name__ == '__main__':

    # now1 = datetime.datetime.now().date().strftime('%Y/%m/%d')
    now1 = datetime.date(2021, 3, 31).strftime('%Y/%m/%d')
    start1 = datetime.date(2020, 12, 7).strftime('%Y/%m/%d')

    holiday = pd.date_range(start1,now1).strftime("%Y/%m/%d").to_list()
    FileList = pd.date_range(start1,now1).strftime("%Y.%m.%d").to_list()

    print(FileList)

    for i in range(len(holiday)):
        if i == len(holiday) - 1:
            break
        payloadsome= payloadsome.replace(holiday[i], holiday[i + 1])
        print(payloadsome)
        payload = json.dumps({
            "where": payloadsome
        })
        response = requests.request("POST", url, headers=headers, data=payload)
        data = json.loads(response.text)

        ExtractDatas(data, FileList[i + 1])
        break


    print("程序运行结束")
