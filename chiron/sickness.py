from .app import app
from .oauth import authenticate, get, post
from twilio.rest import TwilioRestClient
import datetime
import json

# Log in to get token (lasts 2 hours)
token = authenticate('me@andyg.com.au', 'tandahack2016')

# User that sets incoming contactor to sick
user = get("users/me", token)
leaveToken = "43de03713b783975a79d86ab8706e9ca4a404e8b681a1333b1ecbf97c3c8c0a5"


# Set incoming to sick
def setSick(id, reason, hours, start, finish):
    body = {
        "reason": reason,
        "user_id": id,
        "hours": hours,
        "start": start,
        "finish": finish,
        "leave_type": "Sick Leave"}
    data = post("leave", body, leaveToken)
    print(data.content.decode('utf-8'))


# Get list of available according to sick
def getAvailable(shift, date):
    avail = list()
    role = shift.get('role_id')
    working = list()
    shifts = json.loads(get("rosters/on/" + date, leaveToken).content.decode('utf-8')).get('schedules')
    for schedule in shifts:
        if date == schedule.get('date'):
            for shift in schedule.get('schedules'):
                working.append(shift.get('user_id'))
    notWorking = list()
    users = json.loads(get("users/", leaveToken).content.decode('utf-8'))
    for user in users:
        if user.get('id') not in working:
            notWorking.append(user)
    for person in notWorking:
        if role in person.get('role_ids'):
            avail.append(person)
    return avail


# Get Manager on that shift
def getManager(avail, date):
    deptID = str(avail[0].get('department_ids')[0])
    # get department
    depts_data = get("departments/" + deptID or "", leaveToken).content.decode('utf-8')
    if depts_data:
        dept = json.loads(depts_data)
    else:
        pass
    # get department managers that are working on date
    managers = dept.get('managers')
    for manager in managers:
        if getShift(manager, date):
            #return manager
            print("Would be manager of dept")
    #find 'Shift Manager' on date
    users = json.loads(get("users/", leaveToken).content.decode('utf-8'))
    roles = json.loads(get("roles/", leaveToken).content.decode('utf-8'))
    for user in users:
        for role in user.get('role_ids'):
            if getRoleName(role, roles) == 'Shift Manager':
                print(user.get('name'))
                if getShift(user.get('id'), date):
                    print(getShift(user.get('id'), date))
                    return user
    return


def getRoleName(id, roles):
    for role in roles:
        if id == role.get('id'):
            return role.get('name')


# Get the shift of the person on the given date
def getShift(id, date):
    shifts = json.loads(get("rosters/on/" + date, leaveToken).content.decode('utf-8')).get('schedules')
    # find shift with id
    for schedule in shifts:
        if date == schedule.get('date'):
            for shift in schedule.get('schedules'):
                if id == shift.get('user_id'):
                    return shift
    return


# Send list to manager, and the sick person
def tellManager(id, manager, available):
    # for person in available:
        # avail += person.get('name') + " " + person.get('ph') + '\n'
    avail = 'Bob Smith, Tom Cranny, Sandra Lemmings'
    app.logger.info('FOUND AVAILIBLE: %s', avail)

    msg = str(id) + " is sick for their next shift\nThese are the available employees to replace them: \n{0}".format(avail)
    body = {
        "message": msg,
        "user_ids": [
            manager
        ]
    }
    # data = post('sms/send', body, leaveToken)

    client = TwilioRestClient(app.config['TWILIO_SID'], app.config['TWILIO_TOKEN'])
    client.messages.create(
        to='+61422655246',
        from_=app.config['TWILIO_NUMBER'],
        body=msg,
    )


# Get list of leave types of someone
def getLeaveTypes(id):
    return get("leave/types_for/" + id, leaveToken)


def unix_to_datetime(unixTime):
    return datetime.datetime.fromtimestamp(int(unixTime))


def approve_sick_day(employee_id, date):
    # Get the shift for that day
    shift = getShift(employee_id, date)

    # Get other available employees
    available = getAvailable(shift, date)

    # Get the manager in charge
    manager = getManager(available, date)

    # Text the manager who is available
    tellManager(employee_id, manager, available)


# print(user.content)

# # print (token)
# # userID = json.loads(user.content.decode('utf-8')).get('id')
# annaID = 124011
# sickDate = "2016-04-23"
# # print(json.loads(getLeaveTypes(userID).content.decode('utf-8')))
# # setSick(userID, "siiick", 3, "2016-04-23", "2016-04-23")
#
# shift = getShift(annaID, sickDate)
# startTime = unix_to_datetime(shift.get('start'))#.strftime('%Y-%m-%d %H:%M:%S')
# endTime = unix_to_datetime(shift.get('finish'))#.strftime('%Y-%m-%d %H:%M:%S')
# print("Start: " + str(startTime) + " End: " + str(endTime))
#
# available = getAvailable(shift, sickDate)
# print(available)
#
# manager = getManager(available, sickDate)
# print(manager)

# tellManager(userID, manager, available)
