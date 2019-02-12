from flask import Flask, redirect, url_for, render_template
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import SubmitField

app = Flask(__name__)
app.secret_key = "secretsarehidden"

class AccountSetupForm(FlaskForm):
    picture = FileField('Update Profile Picture', validators=[])
    submit = SubmitField('Submit')

@app.route('/')
def home(): return "home"

@app.route("/upload",methods=['GET','POST'])
def upload():
    form = AccountSetupForm()
    if form.validate_on_submit():
        if form.picture.data: print('got picture')
        else: print('got no pic')
        return redirect(url_for('home'))
    print("form not validated")
    return render_template('upload.html', title='Account Setup', form=form)

if __name__=='__main__':
    app.run(debug=True)
