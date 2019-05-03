import sqlalchemy
import csv
import datetime
from sqlalchemy import create_engine, MetaData, Table, select
import json

def getTree(postgres, repoid):
    engine = create_engine('postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % postgres, echo=False)
    metadata = MetaData(engine)
    engine.connect()

    repos_table = Table('Repos', metadata, autoload=True)
    structure_table = Table('RepoStructures', metadata, autoload = True)
    conn = engine.connect()

    # Check if the repo is already existing in the database
    select_repo = select([repos_table]).\
        where((repos_table.c.RepoId == repoid))

    result = conn.execute(select_repo)
    row = result.fetchone()

    # A record already exists
    if result.rowcount > 0:
        repoId = row['RepoId']
        # get Tree from RepoStructures table
        select_tree = select([structure_table]).\
            where((structure_table.c.RepoId == repoId))

        res = conn.execute(select_tree)
        r = res.fetchone()
        if res.rowcount > 0:
            return json.dumps(r['RepoTree'])
        else:
            return None

    else:
        #Repo not found
        return None

def getFileDetails(postgres, repoid, filepath):
    engine = create_engine('postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % postgres, echo=False)
    metadata = MetaData(engine)
    engine.connect()

    repos_table = Table('Repos', metadata, autoload=True)
    files_table = Table('Files', metadata, autoload=True)
    conn = engine.connect()

    # Check if the repo is already existing in the database
    select_repo = select([repos_table]).\
        where((repos_table.c.RepoId == repoid))

    result = conn.execute(select_repo)
    row = result.fetchone()

    # A record already exists
    if result.rowcount > 0:
        repoId = row['RepoId']
        # get Details from Files table
        select_tree = select([files_table]).\
            where((files_table.c.RepoId == repoId) & (files_table.c.FilePath == filepath))

        res = conn.execute(select_tree)
        r = res.fetchone()
        if res.rowcount > 0:
            resp = dict()
            resp['FileName'] = r['FileName']
            resp['FilePath'] = r['FilePath']
            resp['FileSizeBytes'] = r['FileSizeBytes']
            resp['FileType'] = r['FileType']
            resp['LinesOfCode'] = r['LinesOfCode']
            resp['LastModified'] = str(r['LastModified'])
            return json.dumps(resp)
        else:
            return None

    else:
        #Repo not found
        return None

def getAllRepos(postgres):
    engine = create_engine('postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % postgres, echo=False)
    metadata = MetaData(engine)
    engine.connect()

    repos_table = Table('Repos', metadata, autoload=True)
    conn = engine.connect()

    select_tree = select([repos_table])

    res = conn.execute(select_tree)
    if res.rowcount > 0:
        myres = list()
        for row in res:
            temp = dict()
            temp['name'] = row['RepoName']
            temp['path'] = "/setRepo/"+str(row['RepoId'])
            myres.append(temp)
        return json.dumps(myres)
    else:
        return None
