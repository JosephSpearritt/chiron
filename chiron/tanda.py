import json

from .oauth import *


TANDA_TOKEN =  "6b14f827a74ba300a8929bba04ec282b632983b96c3b2228ec865f16b7977a2f"


def recieve_text(no, text):
    dtext = decipher_text(text)
    print(dtext)
    if dtext == 0:
        send_how_to()
        return
    id = find_employee(dtext['id'],no,dtext['name'],dtext['email'])
    return id


def decipher_text(text):
    words = text.split()
    if len(words) < 5:
        return 0
    return {'name': words[0] + " " + words[1], 'id': words[2], 'email': words[3], 'reason': words[4:]}


"""
All has failed, ask them to send back info
"""
def send_how_to():

    pass


def get_users():
    return get("users?show_wages=false",TANDA_TOKEN).json()


def find_employee(id, no, name,email):
    if id == str(123977):
        print("matched")
    #search what we may have
    for user in get_users():
        print(user['id'])

        if str(user['name']) == name:
            return user['id']
        if str(user['id']) == id:
            return id
        if str(user['phone']) == no:
            return user['id']
        if str(user['email']) == email:
            return user['id']

    #found nothing
    return

print(recieve_text("0412744217","Sam Brown 123977 windyce@gmail.com sick"))
