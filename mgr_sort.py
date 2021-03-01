# -*- coding: UTF-8 -*-

import re
import json
import functools
import math


dic = json.load(open('./mgr_history_new_new.json', 'r', encoding="utf-8"))
type_spec = ['股票型', '混合型', 'ETF-场内', '股票指数', '混合-FOF', '封闭式']
#type_spec = ['股票型', '混合型', '联接基金', 'ETF-场内', '股票指数', 'QDII', 'QDII-指数', 'QDII-ETF', '混合-FOF', '封闭式']
#type_spec = ['固定收益', '分级杠杆', '其他创新', '债券型', '定开债券', '理财型', '货币型', '债券指数', '保本型']
#{'股票型': 688, '混合型': 7695, '联接基金': 479, 'ETF-场内': 464, '股票指数': 1011, '固定收益': 300, '分级杠杆': 301, '其他创新': 26, 'QDII': 331, 'QDII-指数': 169, '债券型': 4358, '定开债券': 1636, '理财型': 286, '货币型': 1787, '封闭式': 30, '债券指数': 335, '保本型': 73, '混合-FOF': 147, 'QDII-ETF': 26}
le2 = []
le5 = []
le8 = []
le20 = []
le40 = []
gt40 = []
spec = []
for id, config in dic.items():
    if len(config["all"]) <= 2:
        le2.append(id)
    elif len(config["all"]) <= 5:
        le5.append(id)
    elif len(config["all"]) <= 8:
        le8.append(id)
    elif len(config["all"]) <= 20:
        le20.append(id)
    elif len(config["all"]) <= 40:
        le40.append(id)
    else:
        gt40.append(id)
    # count = str(len(config["all"]))
    # val = counts.get(count) and (counts[count]+1) or 1
    # counts[count] = val

_re = re.compile(r'(-|[\d.]+%)\|(\d+|-)\|(\d+|-)')
for id, config in dic.items():
    #fund_count = len(config["all"])
    symbols = []
    fund_count = 0
    lose = 0
    avg = 0
    days = 0
    for i in range(len(config["all"])):
        fund = config["all"][i]

        if fund['type'].strip() in type_spec:
            fund_count += 1
            symbols.append(fund['symbol'])
            if fund["percent"].startswith('-') or fund["percent"] == "" or fund["days"]  == "0":
                lose += 1

                if fund["percent"].startswith('-'):
                    days = max(days, int(fund["days"]))
                    avg += float(fund["percent"].replace(',', '')) / int(fund["days"])
            else:
                #print(fund["percent"])
                avg += float(fund["percent"].replace(',', '')) / int(fund["days"])
                fund['avg'] = float(fund["percent"].replace(',', '')) / int(fund["days"])
    
    config['days'] = days
    config['count'] = fund_count
    if lose >= fund_count:
        config["avg"] = 0
        config["lose"] = 1
    else:
        # 平均速度扩大到年速率
        # TODO各个时间段股市速率不一样处理。也许中位数更好
        avg = avg / (fund_count) * 365# - lose
        config["avg"] = avg
        config["lose"] = lose / fund_count

    rank_total = 0
    rank_times = 0
    for i in range(len(config["rank"])):
        fund = config["rank"][i]
        if fund['symbol'] in symbols:
            match = _re.match(fund['3m'])
            if match != None and match.group(2) != '-':
                rank_total += int(match.group(2)) / int(match.group(3))
                if int(match.group(2)) / int(match.group(3)) <= 0.01:
                    spec.append(id)
                rank_times += 1

            match = _re.match(fund['6m'])
            if match != None and match.group(2) != '-':
                rank_total += int(match.group(2)) / int(match.group(3))
                if int(match.group(2)) / int(match.group(3)) <= 0.01:
                    spec.append(id)
                rank_times += 1

            match = _re.match(fund['1y'])
            if match != None and match.group(2) != '-':
                rank_total += int(match.group(2)) / int(match.group(3))
                if int(match.group(2)) / int(match.group(3)) <= 0.01:
                    spec.append(id)
                rank_times += 1

            match = _re.match(fund['2y'])
            if match != None and match.group(2) != '-':
                rank_total += int(match.group(2)) / int(match.group(3))
                if int(match.group(2)) / int(match.group(3)) <= 0.01:
                    spec.append(id)
                rank_times += 1

            # match = _re.match(fund['0y'])
            # if match != None and match.group(2) != '-':
            #     rank_total += int(match.group(2)) / int(match.group(3))
            #     if int(match.group(2)) / int(match.group(3)) <= 0.01:
            #         spec.append(id)
            #     rank_times += 1

    config['rank_val'] = rank_times > 0 and rank_total / rank_times or 1

margin = 0.5
def sort_func(_l, _r):
    l = dic[_l]
    r = dic[_r]

    # if (l['count'] == 0 or r['count'] == 0) and l['count'] - r['count'] != 0:
    #     return r['count'] - l['count']

    # 排名相差多少
    if math.fabs(l["rank_val"] - r["rank_val"]) > 0.006:
        return l["rank_val"] - r["rank_val"]

        # 年收益率高8%
    if math.fabs(l["avg"] - r["avg"]) > 30:
        return r["avg"] - l["avg"]

    # 损失率差10%
    if math.fabs(l["lose"] - r["lose"]) > margin:
        return l["lose"] - r["lose"]
    

    if (l["days"] < 330 and r["days"] >= 330) or (r["days"] < 330 and l["days"] >= 330):
        return r['days'] - l['days']

    #print("{0}-{1}".format(l["count"], r["count"]))
    return l["count"] - r["count"]

# #mgr_id = list(dic.keys())
print(sorted(le2, key=functools.cmp_to_key(sort_func)))
margin = 0.3
print(sorted(le5, key=functools.cmp_to_key(sort_func)))
margin = 0.24
print(sorted(le8, key=functools.cmp_to_key(sort_func)))
margin = 0.21
print(sorted(le20, key=functools.cmp_to_key(sort_func)))
margin = 0.16
print(sorted(le40, key=functools.cmp_to_key(sort_func)))
#margin = 0.1
print(sorted(gt40, key=functools.cmp_to_key(sort_func)))

# cnt = {}
# for i in range(len(spec)):
#     cnt.setdefault(spec[i],0)
#     cnt[spec[i]] = cnt[spec[i]] + 1

# def _sort_func(l, r):
#     return cnt[r] - cnt[l]
# l = list(cnt.keys())
# l = sorted(l, key=functools.cmp_to_key(_sort_func))
# while cnt[l[len(l)-1]] <= 1:
#     l.pop(len(l)-1)
# print(l)