

import requests
import re
import json


payload = {
'dt':'14',
'mc':'returnjson',
'ft':'all',
'pn':'50',
'pi':'1',
'sc':'abbname',
'st':'asc'
}


headers = {
'Host':'fund.eastmoney.com',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
'Accept':'*/*',
'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
'Accept-Encoding':'gzip, deflate',
'Connection':'keep-alive',
'Referer':'http://fund.eastmoney.com/manager/',
'Cookie':'qgqp_b_id=0578282506466b2ca1f51c56baca81a5; intellpositionL=1522.4px; intellpositionT=455px; HAList=a-sz-000572-*ST%20%u6D77%u9A6C%2Ca-sz-000504-*ST%u751F%u7269%2Ca-sz-000622-%u6052%u7ACB%u5B9E%u4E1A%2Ca-sz-300013-%u65B0%u5B81%u7269%u6D41; em_hq_fls=js; xsb_history=420032%7C%u77F3%u5316B1%2C400076%7C%u534E%u4FE1%u56FD%u9645%2C400077%7C%u957F%u751F%u9000%2C400074%7C%u6D77%u6DA63; st_si=57028896122784; st_sn=298; st_psi=20200115105157170-0-0070289771; st_asi=delete; EMFUND0=null; EMFUND1=null; EMFUND2=null; EMFUND3=null; EMFUND4=null; EMFUND5=null; EMFUND6=01-10%2021%3A13%3A19@%23%24%u4E2D%u6B27%u65B0%u84DD%u7B79%u6DF7%u5408A@%23%24166002; ASP.NET_SessionId=mmjoahg3gj1zusr0rdx5lsy3; _adsame_fullscreen_12706=1; EMFUND8=01-15%2010%3A45%3A49@%23%24%u534E%u5B9D%u591A%u7B56%u7565%u589E%u957F%u5F00%u653E@%23%24240005; EMFUND9=01-15%2010%3A50%3A21@%23%24%u5174%u5168%u5408%u6DA6%u5206%u7EA7%u6DF7%u5408@%23%24163406; EMFUND7=01-15 10:51:57@#$%u8BFA%u5B89%u6210%u957F%u6DF7%u5408@%23%24320007; st_pvi=05326704599668; st_sp=2020-01-02%2011%3A29%3A34; st_inirUrl=http%3A%2F%2Fquote.eastmoney.com%2Fcenter%2Fgridlist.html'
}

pagecount=1
total = []

def query(pageNo):
    payload["pi"] = str(pageNo)
    r = requests.get("http://fund.eastmoney.com/Data/FundDataPortfolio_Interface.aspx", params=payload, headers=headers)
    #print(r.status_code)
    txt = r.text
    txt = re.match(r'var \w+ *= *(\{.*\});?', txt).group(1)
    txt = re.sub(r'(\w+)(:)', r'"\1"\2', txt)
    #print(txt)
    array = json.loads(txt)
    for i in range(len(array["data"])):
        #row = array["datas"][i].split(',')
        #total.append({'symbol':row[0], 'dwjz':row[4], 'ljjz':row[5], 'week':row[7], '3m':row[9], '12m':row[11], 'start':row[15]})
        total.append(array["data"][i])
    # array = r.json()
    # json.dumps(array, ensure_ascii=False)

    # pagecount = array[0]["metadata"]["pagecount"]

    # for i in range(len(array[0]["data"])):
    #     item = array[0]["data"][i]
    #     symbol = re.search(r'<u>([0-9]+)</u>', item["sys_key"]).group(1)
    #     total.append({'symbol': symbol, "jjlb":item["jjlb"], "tzlb":item["tzlb"], "ssrq":item["ssrq"], "dqgm":item["dqgm"]})

    return array["pages"]
    # return pagecount


page = 1
while (page <= pagecount):
    pagecount = query(page)
    page += 1


jsonData = json.dumps(total, ensure_ascii=False)
fileObject = open('em_fund_mgr_list_new.json', 'w', encoding="utf-8")
fileObject.write(jsonData)
fileObject.close()