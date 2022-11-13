from flask import Flask, render_template, request
from datetime import datetime,timedelta
from logic import WorkHours, WorkCompensation
app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def index():
    message=""
    max_datetime=datetime.now()
    min_datetime=max_datetime.replace(year=(max_datetime.year-1)).strftime('%Y-%m-%dT%H:%M')
    max_datetime=datetime.strftime(max_datetime, "%Y-%m-%dT%H:%M")
    #Users are only allowed to select dates from right now to a year ago from right now
    if request.method =='POST':
        message=[] #this will be a list of 3 datetime objects and 4 integers representing pay
        startTime=request.form.get("startTime") #request from the form
        bedTime=request.form.get("bedTime")
        endTime=request.form.get("endTime")
        start,bed,mid, end=WorkHours(startTime,bedTime,endTime).structure_datetime(startTime,bedTime,endTime)
        message.extend((start,bed,end))
        myhours=WorkHours(startTime,bedTime,endTime).returnTimeDiff(startTime,bedTime,endTime)
        pay_start2bed=WorkCompensation(myhours).pay_start2bed(myhours)
        pay_bed2mid=WorkCompensation(myhours).pay_bed2mid(myhours)
        pay_mid2end=WorkCompensation(myhours).pay_mid2end(myhours)
        total=WorkCompensation(myhours).total_pay(myhours)
        message.extend((pay_start2bed,pay_bed2mid,pay_mid2end,total))
        return render_template("index.html",message=message,max_datetime=max_datetime,min_datetime=min_datetime)
    return render_template("index.html",message=message,max_datetime=max_datetime,min_datetime=min_datetime)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
