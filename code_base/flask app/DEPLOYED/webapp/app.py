from flask import Flask, session, render_template,request,redirect
from scripts import clone_and_create_json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

POSTGRES = {
    'user': 'postgres',
    'pw': 'pg123',
    'db': 'demo2',
    'host': 'localhost',
    'port': '5432',
}

# POSTGRES = {
#     'user': 'bpvmzwecssmefd',
#     'pw': '3de40800289f2251c3192849dcfc0fec4216bc90b080f60a8d77efd37156b278',
#     'db': 'd7ehdb25kv3pkv',
#     'host': 'ec2-184-73-210-189.compute-1.amazonaws.com',
#     'port': '5432',   
# }

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.init_app(app)


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