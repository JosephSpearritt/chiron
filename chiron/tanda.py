"""
    Functions for Tanda related behaviour.
"""

import datetime
import re

import twilio

from .models import *
from .oauth import *

from .app import app
TANDA_TOKEN = "6b14f827a74ba300a8929bba04ec282b632983b96c3b2228ec865f16b7977a2f"


def receive_text(ph_num, text):
    text_data = decipher_text(text)

    if text_data == 0:
        send_how_to(ph_num)
        return
    user = find_employee(text_data['id'], ph_num, text_data['name'], text_data['email'])
    if not user:
        send_how_to(ph_num)
        return
    register_illness(ph_num, user)
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


def register_illness(ph_num, text):
    request = LeaveRequest(text['id'], text['name'], ph_num, text['reason'], date=datetime.date.today())
    db.session.add(request)
    db.session.commit()
    return


def send_how_to(ph_num):
    """
    All has failed, ask them to send back info
    """
    text = (
        "Please text as follows:"
        "  Name, ID, Email, Reason."
        "  Type 0 when you are not sure"
        "  Example: Sam Brown 0 sam@sam.com I'm sick"
    )

    from twilio.rest import TwilioRestClient

    client = TwilioRestClient(app.config['TWILIO_SID'], app.config['TWILIO_TOKEN'])
    client.messages.create(
        to=ph_num,
        from_=app.config['TWILIO_NUMBER'],
        body=text,
    )

def send_recieved(ph_num):
    """
    All has worked, send back success
    """
    text = (
        "Your sick leave request has been successful. We are reviewing it now"
    )

    from twilio.rest import TwilioRestClient

    client = TwilioRestClient(app.config['TWILIO_SID'], app.config['TWILIO_TOKEN'])
    client.messages.create(
        to=ph_num,
        from_=app.config['TWILIO_NUMBER'],
        body=text,
    )

def get_users():
    return get("users?show_wages=false", app.config['TANDA_TOKEN']).json()


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
    # Search what we may have
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

    # Found nothing
    return
