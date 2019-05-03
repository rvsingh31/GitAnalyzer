from flask import Flask, session, render_template, request, redirect, url_for
from app_scripts import use_cases, db_script
from flask_sqlalchemy import SQLAlchemy
import app_scripts.getFromDB as gt
import json

app = Flask(__name__)


# POSTGRES = {
#     'user': 'postgres',
#     'pw': 'pg123',
#     'db': 'demo2',
#     'host': 'localhost',
#     'port': '5432',
# }

POSTGRES = {
    'user': 'bpvmzwecssmefd',
    'pw': '3de40800289f2251c3192849dcfc0fec4216bc90b080f60a8d77efd37156b278',
    'db': 'd7ehdb25kv3pkv',
    'host': 'ec2-184-73-210-189.compute-1.amazonaws.com',
    'port': '5432',
}

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.init_app(app)

from models import *

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
    # session.pop('repoid', None)
    return render_template('index.html')

@app.route('/main')
def main():
    if 'repoid' in session:
        print (session['repoid'])
        tree = gt.getTree(POSTGRES,session['repoid'])
        if tree is None:
            err = 'Some error occured. Please consider analyzing your repository again!'
            return render_template('index.html', errorstr = err)    
        else:
           return render_template('main.html', response = tree)
        # return render_template('main.html')
    else:
        err = 'Please select a repository for analysis!'
        return render_template('index.html', errorstr = err)



@app.route('/update')
def update():
    if 'repoid' in session:
        tree = gt.getTree(POSTGRES,session['repoid'])
        if tree is None:
            return False, 200 
        else:
            return tree, 200
    else:
        return False, 200


@app.route('/analyze',methods = ['POST'])
def analyze():
    data = json.loads(request.data.decode())
    url = data['url']
    print("Received URL" + url)
    arr = url.split('/')
    repo_owner = arr[-2]
    repo_name = arr[-1].split('.')[0]
    uc = use_cases.Use_Case(repo_owner,repo_name,url)
    structure = uc.getTreeStructure()
    UC1_df = uc.UC1()
    UC2_df = uc.UC2()
    UC3_df = uc.UC3()
    print (UC1_df.head())
    print (UC2_df.head())
    print (UC3_df.head())
    b = db_script.storeAll(UC1_df,UC2_df, UC3_df, (repo_name,url,structure))
    if b == False:
        return "error",200
    else:
        session['repoid'] = int(b)
        return "analyzed", 200

@app.route('/getDetails',methods = ['POST'])
def getDetails():

    if 'repoid' in session:
        data = json.loads(request.data.decode())
        response = gt.getFileDetails(POSTGRES,session['repoid'],data['filepath'])
        return response, 200
    else:
        err = 'Please select a repository for analysis!'
        return render_template('index.html', errorstr = err)


@app.route('/getAllRepos')
def getAllRepos():
    res = gt.getAllRepos(POSTGRES)
    if res is None:
        return "error",200
    else:
        return res, 200

@app.route('/setRepo/<id>',methods=['GET'])
def setRepo(id):
    session['repoid'] = int(id)
    return redirect(url_for('main'))


if __name__ == "__main__":
    app.secret_key = "311296"
    app.run(debug=True)