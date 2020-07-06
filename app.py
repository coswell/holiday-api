# -*- coding: utf-8 -*-
# by well 2020/07/01 
from flask import Flask, abort, request, jsonify
from datetime import datetime

ExchangeDay = {
    "2020": (20200119, 20200426, 20200509, 20200628, 20200927, 20201010)
}
Holiday = {
    "2020": {
        "New Year's Day": (20200101, 20200101),
        "Spring Festival": (20200124, 20200202),
        "Qingming Festival": (20200404, 20200406),
        "International Workers' Day": (20200501, 20200505),
        "Dragon Boat Festival": (20200625, 20200627),
        "Mid-Autumn Festival & National Day": (20201001, 20201008)
    }
}

def queryExchangeDay(date):
    QueryYear = date[0:4]
    if int(date) in ExchangeDay[QueryYear]:
        return True
    return False

def queryHoliday(date):
    holidayinfo = {}
    QueryYear = date[0:4]
    for k,v in Holiday[QueryYear].items():
        if (int(date) >= v[0]) and (int(date) <= v[1]):
            holidayinfo["name"] = k
            holidayinfo["startday"] = v[0]
            holidayinfo["endday"] = v[1]
            return (True, holidayinfo)
    return (False, None)

def holiday(date):
    if not date:
        date = datetime.now().strftime('%Y%m%d')
    IsWork = True
    DateInfo = {
        "code": 0,
        "type": {
            "type": 0
        }
    }
    IsHoliday, HolidayInfo = queryHoliday(date)
    if IsHoliday:
        IsWork = False
    else:
        separator=""
        formatstr = "%Y" + separator + "%m" + separator + "%d"
        fdate = datetime.strptime(date,formatstr).date()
        if fdate.weekday() in [5,6]:
            IsWork = False
            DateInfo['holiday'] = {"name": "weekend"}
        else:
            IsWork = True
        IsWork = IsWork ^ queryExchangeDay(date)
    
    if not IsWork:
        DateInfo['type']['type'] = 1
        if HolidayInfo:
            DateInfo['holiday'] = HolidayInfo
    else:
        if fdate.weekday() in [5,6]:
            del DateInfo['holiday']
    return DateInfo

app = Flask(__name__)

@app.route('/holiday', methods=['POST','GET'])
def query():
    QueryDate = request.args.get('date')
    DateInfo = holiday(QueryDate)
    return jsonify(DateInfo)

if __name__ == "__main__":
    # 将host设置为0.0.0.0，则外网用户也可以访问到这个服务
    app.run(host="0.0.0.0", port=3389, debug=True)

