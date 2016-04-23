import json

from .oauth import *
import re
from chiron.models import *
import datetime


TANDA_TOKEN =  "6b14f827a74ba300a8929bba04ec282b632983b96c3b2228ec865f16b7977a2f"


def receive_text(no, text):
    dtext = decipher_text(text)
    print(dtext)
    if dtext == 0:
        send_how_to(no)
        return
    user = find_employee(dtext['id'],no,dtext['name'],dtext['email'])
    if not user :
        send_how_to(no)
        return
    register_illness(no, user)
    return "worked"


def check_not_email(email):
    if re.search(".*@.*", email):
        return False
    return True


def decipher_text(text):
    words = text.split()
    if len(words) < 4:
        return 0

    if not words[2].isdigit():
        return 0

    if check_not_email(words[3]):
        return {'name': words[0] + " " + words[1], 'id': words[2], 'email': '0', 'reason': words[3:]}

    return {'name': words[0] + " " + words[1], 'id': words[2], 'email': words[3], 'reason': words[4:]}


def register_illness(no,text):
    request = LeaveRequest(text['id'], text['name'], no, text['reason'], date=datetime.date.today())
    db.session.add(request)
    db.session.commit()
    return

"""
All has failed, ask them to send back info
"""
def send_how_to(no):
    text = "Please text as follows. Name, ID, Email, Reason. Type 0 when you are not sure Example: Sam Brown 0 sam@sam.com I'm sick"
    pass


def get_users():
    return get("users?show_wages=false",TANDA_TOKEN).json()


def confirm_employee(id, no, name, email, user):
    count = 0

    if str(user['name']) == name:
        count += 1
    if str(user['id']) == id:
        count += 1
    if str(user['phone']) == no:
        count += 1
    if str(user['email']) == email:
        count += 1

    if count >= 2:
        return True

    return False


def find_employee(id, no, name, email):
    #search what we may have
    for user in get_users():

        if str(user['name']) == name:
            if confirm_employee(id, no, name, email, user):
                return user
            continue
        if str(user['id']) == id:
            if confirm_employee(id, no, name, email, user):
                return user
            continue
        if str(user['phone']) == no:
            if confirm_employee(id, no, name, email, user):
                return user
            continue
        if str(user['email']) == email:
            if confirm_employee(id, no, name, email, user):
                return user
            continue

    #found nothing
    return

print(receive_text("0412744217","Sam Brown 123977 windyce@gmail.com sick"))
