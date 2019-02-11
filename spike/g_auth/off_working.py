#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import os
from srblib import SrbJson

from flask import Flask, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google

app = Flask(__name__)
config = SrbJson('~/.config/iblog/config.json')
app.secret_key = "secretisgood"
app.config["GOOGLE_OAUTH_CLIENT_ID"] = config.get('GOOGLE_OAUTH_CLIENT_ID','')
app.config["GOOGLE_OAUTH_CLIENT_SECRET"] = config.get('GOOGLE_OAUTH_CLIENT_SECRET','')
google_bp = make_google_blueprint(
    offline=True,
    redirect_url='/google_login',
    scope=[
        "https://www.googleapis.com/auth/plus.me",
        "openid https://www.googleapis.com/auth/userinfo.email",
    ]
)
app.register_blueprint(google_bp, url_prefix="/google_login")# url prefix should be same as registered there.
"""
if url_prefix is xyz here
then
Authorized redirect URLs will be xyz/google/authorized
"""

@app.route("/")
def home():
    print('home')
    return "home"

@app.route("/google_login")
def register():
    if not google.authorized: return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    # print(resp.json()) # whoe result
    return "You are {email}, {name} on Google".format(email=resp.json()["email"],name=resp.json()['name'])

if __name__ == "__main__":
    import os
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
    app.run(debug=True)
