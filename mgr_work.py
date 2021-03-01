# -*- coding: UTF-8 -*-

import json
from bs4 import BeautifulSoup
import requests
import re


dic = json.load(open('./em_fund_mgr_list_new.json', 'r', encoding="utf-8"))
headers = {
'Host':'fund.eastmoney.com',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
'Accept-Encoding':'gzip, deflate',
'Connection':'keep-alive',
'Cookie':'qgqp_b_id=0578282506466b2ca1f51c56baca81a5; intellpositionL=1522.4px; intellpositionT=455px; HAList=a-sz-000572-*ST%20%u6D77%u9A6C%2Ca-sz-000504-*ST%u751F%u7269%2Ca-sz-000622-%u6052%u7ACB%u5B9E%u4E1A%2Ca-sz-300013-%u65B0%u5B81%u7269%u6D41; em_hq_fls=js; xsb_history=420032%7C%u77F3%u5316B1%2C400076%7C%u534E%u4FE1%u56FD%u9645%2C400077%7C%u957F%u751F%u9000%2C400074%7C%u6D77%u6DA63; st_si=57028896122784; st_sn=304; st_psi=20200115110550944-0-9407704249; st_asi=delete; EMFUND0=null; EMFUND1=null; EMFUND2=null; EMFUND3=null; EMFUND4=null; EMFUND6=01-15%2010%3A51%3A57@%23%24%u8BFA%u5B89%u6210%u957F%u6DF7%u5408@%23%24320007; ASP.NET_SessionId=mmjoahg3gj1zusr0rdx5lsy3; _adsame_fullscreen_12706=1; EMFUND8=01-15%2010%3A50%3A21@%23%24%u5174%u5168%u5408%u6DA6%u5206%u7EA7%u6DF7%u5408@%23%24163406; EMFUND9=01-15%2011%3A00%3A50@%23%24%u534E%u5546%u8BA1%u7B97%u673A%u884C%u4E1A%u91CF%u5316%u80A1%u7968@%23%24007853; EMFUND5=01-15%2011%3A01%3A15@%23%24%u4E2D%u6B27%u65B0%u84DD%u7B79%u6DF7%u5408A@%23%24166002; EMFUND7=01-15 11:05:51@#$%u534E%u5B9D%u591A%u7B56%u7565%u589E%u957F%u5F00%u653E@%23%24240005; st_pvi=05326704599668; st_sp=2020-01-02%2011%3A29%3A34; st_inirUrl=http%3A%2F%2Fquote.eastmoney.com%2Fcenter%2Fgridlist.html',
'Upgrade-Insecure-Requests':'1'
}

mgr = {}
for i in range(len(dic)):
    two = {"all":[], "rank":[]}
    print(dic[i][0])
    r = requests.get("http://fund.eastmoney.com/manager/%s.html" % dic[i][0], headers=headers)
    r.encoding = 'utf-8'
    #print(t.text)

    soup = BeautifulSoup(r.text, 'html.parser')
    tables = soup.find_all('table', class_='ftrs')
    addin = True
    for __i, t in enumerate(tables):
        if __i == 0:
            for _i, tr in enumerate(t.tbody.find_all('tr')):
                match = re.match(r'(?:(\d+)年又)?(\d+)天', tr.contents[6].text)
                days = 1
                if match != None:
                    days = int(match.group(2))
                    if match.group(1) != None:
                        days += 365 * int(match.group(1))

                percent = tr.contents[7].text
                percent = percent[:-1]
                two["all"].append({'symbol':tr.contents[0].text, 'name':tr.contents[1].text, 'type':tr.contents[3].text, 'size':tr.contents[4].text, 'span':tr.contents[5].text, 'days':str(days), 'percent':percent })
        else:
            for _i, tr in enumerate(t.tbody.find_all('tr')):
                if len(tr.contents) <= 1:
                    addin = False
                else:
                    two["rank"].append({'symbol':tr.contents[0].text, 
                    '3m':tr.contents[3].text + '|' + tr.contents[4].text, 
                    '6m':tr.contents[5].text + '|' + tr.contents[6].text,
                    '1y':tr.contents[7].text + '|' + tr.contents[8].text, 
                    '2y':tr.contents[9].text + '|' + tr.contents[10].text, '0y':tr.contents[11].text + '|' + tr.contents[12].text}
                    )

        #print(t.tbody.text)
        # for _i in range(len(t.contents)):
        #     print(t.contents[_i])
        #print(len(t.contents))
        #print(t.caption.string)
        #print(t.text)
        # if 'Stock List Description' in t.text:
        #     result = str(value[i].text)
    if addin:
        mgr[dic[i][0]] = two
    #break

jsonData = json.dumps(mgr, ensure_ascii=False)
fileObject = open('mgr_history_new_new.json', 'w', encoding="utf-8")
fileObject.write(jsonData)
fileObject.close()
