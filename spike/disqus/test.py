#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import os
from srblib import SrbJson

from flask import Flask, redirect, url_for, render_template
from flask_dance.contrib.google import make_google_blueprint, google

app = Flask(__name__)
app.secret_key = "secretisgood"
disq = Disqus(app)

domain_url = "http://127.0.0.1:5000"
@app.route("/")
def home():
    print('home')
    srb_url = domain_url + url_for('home')
    srb_url_id = srb_url + "srbcheema"
    # srb_url is just to identify page uniquely
    return render_template('home.html',srb_url=srb_url)

if __name__ == "__main__":
    import os
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
    app.run(debug=True)
