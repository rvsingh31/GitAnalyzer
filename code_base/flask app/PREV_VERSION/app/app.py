from flask import Flask, session, render_template,request,redirect
from scripts import clone_and_create_json
app = Flask(__name__)



@app.errorhandler(404)
@app.errorhandler(405)
@app.errorhandler(403)
@app.errorhandler(500)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/analyze',methods = ['POST'])
def analyze():
    url = request.form['repo_url']
    clone_and_create_json.create_json(url)
    return "analyzed"


if __name__ == "__main__":
    app.run(debug=True)
    app.secret_key = "311296"