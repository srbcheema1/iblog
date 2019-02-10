import os

from flask import url_for, current_app
from flask_mail import Message
from code_tester import rand
from PIL import Image

from iblog.config import mail


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

