import db
from flask import abort
from flask import render_template
from flask import request
from flask import make_response
from flask import jsonify
from flask.ext.login import login_required
from flask.ext.login import current_user
import datetime
import dateutil.parser
 
@login_required
def csv():
    type = request.args.get('type', 'weekly')
    data = request.args.get('data', 'messages')
    return _get_data(type, data)


@login_required
def index():
    if not current_user.user.is_super_admin:
        abort(404)
    return render_template("/stats/index.html")

def usersperhour(key):
    if not key == '2b3j4fa28bb23k':
        abort(404)
    return _get_daily_stats()

def totaluserstoday(key):
    if not key == '2b3j4fa28bb23k':
        abort(404)
    data = request.args.get('date') 
    return _get_total_users(data)

def users_per_day_of_week(key):
    if not key == '2b3j4fa28bb23k':
        abort(404)
    return _get_users_per_day_of_week()

def weekly_totals(key):
    if not key == '2b3j4fa28bb23k':
        abort(404)
    return _get_weekly_totals()

# Get stats from yesterday and current time today
def _get_daily_stats():

    times = [
        "T00:00",
        "T01:00",
        "T02:00",
        "T03:00",
        "T04:00",
        "T05:00",
        "T06:00",
        "T07:00",
        "T08:00",
        "T09:00",
        "T10:00",
        "T11:00",
        "T12:00",
        "T13:00",
        "T14:00",
        "T15:00",
        "T16:00",
        "T17:00",
        "T18:00",
        "T19:00",
        "T20:00",
        "T21:00",
        "T22:00",
        "T23:00",
    ]

    temp_time = [] 

    now = str(datetime.datetime.now().isoformat())[:-10]

    # Number of days since live, June 1, 2016
    days_live = datetime.date.today() - datetime.date(2016, 6, 1)

    response = {
            "x_axis":
                {
                    "type": "datetime"
                },
            "series": 
            [
                {
                    "name": "Users per hour today",
                    "data": [],
                    "incomplete_from": now
                },
                {
                    "name": "Average users per hour",
                    "data": []
                }
            ]
        }

    # For today and yesterday, get the earliest and latest times possible
    # i.e. 2016-08-31T00:00:00.000000 -> 2016-08-31T23:59:59.999999
    today = datetime.date.today() #- datetime.timedelta(days=7)
    min_today = datetime.datetime.combine(today, datetime.time.min).isoformat()
    max_today = datetime.datetime.combine(today, datetime.time.max).isoformat()
    beginning = datetime.date.today() - datetime.timedelta(days=days_live.days)
    min_beginning = datetime.datetime.combine(beginning, 
            datetime.time.min).isoformat()

    # Append to response the correct hourly times, each starting with 0 created_at 
    for hour in times:
        curr = str(today.isoformat()) + hour 
        y = str(beginning.isoformat()) + hour
        if curr < now: 
            response['series'][0]['data'].append([curr, 0])
            response['series'][1]['data'].append([curr, 0])
            temp_time.append([y, 0])
        else:
            response['series'][1]['data'].append([curr, 0])
            temp_time.append([y, 0])

    # Query to get both sets of stats, today and yesterday in ascending order
    today_stats = db.User.query.with_entities(db.User.created_at).\
            filter(db.User.created_at >= min_today).\
            filter(db.User.created_at <= max_today).\
            order_by(db.User.created_at.asc()).all()
    average_stats = db.User.query.with_entities(db.User.created_at).\
            filter(db.User.created_at >= min_beginning).\
            order_by(db.User.created_at.asc()).all()

    # Adds to each hour today if a User was created during that time
    x = 0 
    for stat in today_stats:
        created = stat.created_at.isoformat()
        while x < 24 and created > response['series'][0]['data'][x][0]:
            x += 1
        response['series'][0]['data'][x-1][1] += 1
        
    # Adds to each hour yesterday if a User was created during that time
    x = 0
    for stat in average_stats:
        created_hour = int(str(stat.created_at.isoformat())[11:13])
        temp_time[created_hour][1] += 1

    # There's probably a better solution, hacked this up quickly
    # Takes temp_time, which is yesterday's times, and calculates on that
    # But adds the averages to today's date
    x = 0
    for a in temp_time:
        response['series'][1]['data'][x][1] = round(a[1] / float(days_live.days), 2)
        x += 1

    return jsonify(response)

def _get_total_users(data):
    if not data:
        return _get_total_users_today()
    return _get_total_users_on_date(data)

def _get_total_users_today():
    
    response = {
        "item": [
            {
                "value": 0,
                "text": "Total Users Today"
            },
            {
                "value": 0,
                "text": "Total Users Yesterday"
            }
        ]
    }

    # For today and yesterday, get the earliest and latest times possible
    # i.e. 2016-08-31T00:00:00.000000 -> 2016-08-31T23:59:59.999999
    today = datetime.date.today() #- datetime.timedelta(days=7)
    min_today = datetime.datetime.combine(today, datetime.time.min).isoformat()
    max_today = datetime.datetime.combine(today, datetime.time.max).isoformat()
    yest = datetime.date.today() - datetime.timedelta(days=1)
    min_yest = datetime.datetime.combine(yest, datetime.time.min).isoformat()
    max_yest = datetime.datetime.combine(yest, datetime.time.max).isoformat()

    # Query to get both sets of stats, today and yesterday in ascending order
    today_stats = db.User.query.with_entities(db.User.created_at).\
            filter(db.User.created_at >= min_today).\
            filter(db.User.created_at <= max_today).\
            order_by(db.User.created_at.asc()).all()
    yesterday_stats = db.User.query.with_entities(db.User.created_at).\
            filter(db.User.created_at >= min_yest).\
            filter(db.User.created_at <= max_yest).\
            order_by(db.User.created_at.asc()).all()

    # Adds to today number of Users created
    for stat in today_stats:
        response['item'][0]['value'] += 1

    # Adds to yesterday number of Users created
    for stat in yesterday_stats:
        response['item'][1]['value'] += 1

    return jsonify(response)

def _get_total_users_on_date(data):

    # Convert date string to datetime object
    # Create min and max times of that day
    if data == 'today':
        day = datetime.date.today() 
    elif data == 'yesterday':
        day = datetime.date.today() - datetime.timedelta(days=1)
    else:
        day = datetime.datetime.strptime(data, '%Y-%m-%d')
    min_day = datetime.datetime.combine(day, datetime.time.min).isoformat()
    max_day = datetime.datetime.combine(day, datetime.time.max).isoformat()

    response = {
        "item": [
            {
                "value": 0,
                "text": "Total Users on " + day.isoformat() 
            }
        ]
    }

    stats = db.User.query.with_entities(db.User.created_at).\
            filter(db.User.created_at >= min_day).\
            filter(db.User.created_at <= max_day).all()

    for stat in stats:
        response['item'][0]['value'] += 1

    return jsonify(response)

def _get_users_per_day_of_week():

    response = {
            "chart": {
                "type": "column"
            },
            "title": {
                "text": None 
            },
            "subtitle": {
                "text": None 
            },
            "xAxis": {
                "categories": [
                    "Mon",
                    "Tue",
                    "Wed",
                    "Thur",
                    "Fri",
                    "Sat",
                    "Sun"
                ]
            },
            "yAxis": {
                "min": 0,
                "title": {
                    "text": "# Users"
                }
            },
            "plotOptions": {
                "column": {
                    "pointPadding": 0.2,
                    "borderWidth": 0
                }
            },
            "series": [
                {
                    "name": "This Week",
                    "data": [0, 0, 0, 0, 0, 0, 0]
                },
                {
                    "name": "Last Week",
                    "data": [0, 0, 0, 0, 0, 0, 0]
                },
                {
                    "name": "Average",
                    "data": [0, 0, 0, 0, 0, 0, 0]
                }
            ]
        }
    
    days_live = datetime.date.today() - datetime.date(2016, 6, 6)
    weeks_live = days_live.days / 7
    diff = days_live.days - (weeks_live * 7)
    t_monday = datetime.date.today() - datetime.timedelta(diff) 
    l_monday = datetime.date.today() - datetime.timedelta(diff + 7)
    this_monday = datetime.datetime.combine(t_monday, datetime.time.min).isoformat()
    last_monday = datetime.datetime.combine(l_monday, datetime.time.min).isoformat()
    beginning = datetime.date.today() - datetime.timedelta(days=days_live.days)
    min_beginning = datetime.datetime.combine(beginning, 
            datetime.time.min).isoformat()

    this_week_stats = db.User.query.with_entities(db.User.created_at).\
            filter(db.User.created_at >= this_monday).\
            order_by(db.User.created_at.asc()).all()
    last_week_stats = db.User.query.with_entities(db.User.created_at).\
            filter(db.User.created_at >= last_monday).\
            filter(db.User.created_at <= this_monday).\
            order_by(db.User.created_at.asc()).all()
    average_stats = db.User.query.with_entities(db.User.created_at).\
            filter(db.User.created_at >= min_beginning).\
            order_by(db.User.created_at.asc()).all()

    # Number of users per day this week
    x = 0
    next_day = t_monday + datetime.timedelta(x + 1)
    for stat in this_week_stats:
        created = stat.created_at.isoformat()
        while x <= 7 and created > next_day.isoformat():
            x += 1
            next_day = t_monday + datetime.timedelta(x + 1) 
        if x < 7:
            response['series'][0]['data'][x] += 1

    # Number of users per day last week
    x = 0
    next_day = l_monday + datetime.timedelta(x + 1)
    for stat in last_week_stats:
        created = stat.created_at.isoformat()
        while x <= 7 and created > next_day.isoformat():
            x += 1
            next_day = l_monday + datetime.timedelta(x + 1) 
        if x < 7:
            response['series'][1]['data'][x] += 1

    # Number of average users per day since beginning
    average = [0,0,0,0,0,0,0]
    x = 0
    next_day = beginning + datetime.timedelta(x + 1)
    for stat in average_stats: 
        created = stat.created_at.isoformat()
        while x <= days_live.days and created > next_day.isoformat():
            x += 1
            next_day = beginning + datetime.timedelta(x + 1) 
        average[x % 7] += 1
        #response['series'][2]['data'][x % 7] += 1

    for x in range(0, 7):
        response['series'][2]['data'][x] = round(average[x] / float(weeks_live), 2)
    
    return jsonify(response)

def _get_weekly_totals():
    response = {
        "x_axis": {
            "labels": [
                "So Far This Week",
                "Last Week This Time",
                "Last Week Total"
            ]
        },
        "series": [{
            "data": [
                0,
                0,
                0
            ]
        }]
    }

    now = datetime.datetime.now().isoformat()
    days_live = datetime.date.today() - datetime.date(2016, 6, 6)
    weeks_live = days_live.days / 7
    diff = days_live.days - (weeks_live * 7)
    t_monday = datetime.date.today() - datetime.timedelta(diff) 
    l_monday = datetime.date.today() - datetime.timedelta(diff + 7)
    this_monday = datetime.datetime.combine(t_monday, datetime.time.min).isoformat()
    last_monday = datetime.datetime.combine(l_monday, datetime.time.min).isoformat()

    this_week_stats = db.User.query.with_entities(db.User.created_at).\
            filter(db.User.created_at >= this_monday).\
            order_by(db.User.created_at.asc()).all()
    last_week_stats = db.User.query.with_entities(db.User.created_at).\
            filter(db.User.created_at >= last_monday).\
            filter(db.User.created_at <= this_monday).\
            order_by(db.User.created_at.asc()).all()

    # Number of users this week
    for stat in this_week_stats:
        response['series'][0]['data'][0] += 1

    # Number of users until current time minus one week 
    last_week_now = (datetime.datetime.now() - datetime.timedelta(7)).isoformat()
    for stat in last_week_stats:
        created = stat.created_at.isoformat()
        if created < last_week_now:
            response['series'][0]['data'][1] += 1
        else:
            break

    # Number of users last week
    for stat in last_week_stats:
        response['series'][0]['data'][2] += 1

    return jsonify(response)

def _get_data(type, data):
    if type not in ['weekly', 'daily']:
        abort(403)
    if type == 'weekly':
        stats = db.WeeklyStats.query.order_by(db.WeeklyStats.end.asc()).all()
    else:
        stats = db.DailyStats.query.order_by(db.DailyStats.created_at.asc()).all()
    
    response = 'date,count\n'
    for stat in stats:
        if data == 'apps_per_listing':
            response += stat.date.strftime('%Y-%b-%d') + ',' \
                + str(_get_apps_per_listing(stat)) + '\n'
        else:
            response += stat.date.strftime('%Y-%b-%d') + ',' \
                + str(getattr(stat, data, '0')) + '\n'

    return response


def _get_apps_per_listing(stat):
    if not stat.listings:
        return 0
    else:
        return stat.applications / (1.0 * stat.listings)

