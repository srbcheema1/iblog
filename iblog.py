#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

from iblog import app

if __name__ == '__main__':
    import os
    # necessary env variables for google-login over http during debug mode
    # https://flask-dance.readthedocs.io/en/latest/quickstarts/google.html
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
    app.run(debug=True)
