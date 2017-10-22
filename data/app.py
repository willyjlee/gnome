import genomelink
from flask import Flask, render_template, request, redirect, session, url_for
app = Flask(__name__)


@app.route('/')
def index():
    authorize_url = genomelink.OAuth.authorize_url(scope=['report:eye-color report:beard-thickness report:morning-person'])

    # Fetching a protected resource using an OAuth2 token if exists.
    reports = []
    if session.get('oauth_token'):
        for name in ['eye-color', 'beard-thickness', 'morning-person']:
            reports.append(genomelink.Report.fetch(name=name, population='european', token=session['oauth_token']))

    return render_template('index.html', authorize_url=authorize_url, reports=reports)

@app.route('/callback')
def callback():
    # The user has been redirected back from the provider to your registered
    # callback URL. With this redirection comes an authorization code included
    # in the request URL. We will use that to obtain an access token.
    token = genomelink.OAuth.token(request_url=request.url)

    print(token)

    # At this point you can fetch protected resources but lets save
    # the token and show how this is done from a persisted token in index page.
    session['oauth_token'] = token
    return redirect(url_for('index'))

if __name__ == '__main__':
    # This allows us to use a plain HTTP callback.
    import os
    os.environ['DEBUG'] = "1"
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    # Run local server on port 5000.
    app.secret_key = os.urandom(24)
    app.run(debug=True)