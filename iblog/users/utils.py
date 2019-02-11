import os

from flask import url_for, current_app
from flask_mail import Message
from code_tester import rand
from PIL import Image
from urllib.request import urlopen

from iblog.config import mail

def get_unique_username(uname):
    temp_uname = uname
    user = User.query.filter_by(username=uname).first()
    while user:
        temp_uname = uname + '_' + str(rand(1,1000))
        user = User.query.filter_by(username=temp_uname).first()
    return temp_uname


def save_picture(form_picture):
    random_hex = 'pic_'+str(rand(100,1000)*rand(1000,10000))+'_'
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def save_picture_url(url):
    random_hex = 'pic_'+str(rand(100,1000)*rand(1000,10000))+'_'
    f_ext = '.'+url.split('.')[-1]
    if f_ext == '.': f_ext = '.jpg'
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(urlopen(url))
    i.thumbnail(output_size)
    try: i.save(picture_path)
    except: return 'default.jpg'
    return picture_fn



def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='srbcheema.iblog@gmail.com',
                  recipients=[user.email])
    msg.body = 'To reset your password, visit the following link: \n'\
            + url_for('users.reset_token', token=token, _external=True)\
            + '\nIf you did not make this request then simply ignore this email.'\
            + '\n'
    mail.send(msg)

