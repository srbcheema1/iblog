import os
from flask import Flask, redirect, url_for
from flask_dance.contrib.github import make_github_blueprint, github

app = Flask(__name__)
app.secret_key = "supersekrit"
github_blueprint = make_github_blueprint(
    redirect_url='/github_login', # where to redirect
    client_id='c168c8022ef87be316f7',
    client_secret='381f103176c05c5b4185c4e4b204ceda1e716ea9'
)
app.register_blueprint(github_blueprint,url_prefix='/')

@app.route("/")
def index():
    return "home"

@app.route("/github_login")
def github_login():
    print("login")
    if not github.authorized:
        return redirect(url_for("github.login"))# dance starts
    resp = github.get("/user")
    assert resp.ok
    return "You are @{login} on GitHub".format(login=resp.json()["login"])

"""
if you have set url_prefix = '/xyz'
then:
    1. in github oauth page set Authorization callback URL to "/xyz/github/authorized"
    2. set redirect_url same as the github_login url so that the function /xyz/github/authorized may redirect to it
"""
if __name__ == "__main__":
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run(debug=True)
