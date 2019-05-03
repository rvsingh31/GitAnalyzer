import csv
import psycopg2
import datetime

'''
This code was written as POC for checking connection with PostgreSQL. It also tested integration with CSV file. 

It has been since replaced by newer version of the code and is no more relevant. 

DEPRECATED
'''

# CSV parsing
csvfile = open('uc1v2.csv', 'r')
reader = csv.DictReader(csvfile)

'''
All possible row headers
RepoName
RepoUrl
FilePath
LastModified
FileSizeBytes
LinesOfCode
AuthorName
AuthorEmail
Score
'''


# Database connection
conn = psycopg2.connect("host=localhost dbname=csc510 user=postgres password=password")
cur = conn.cursor()
# cur.execute('SELECT * FROM public."Files"')
# all = cur.fetchall()

insert_query_repos = 'INSERT INTO public."Repos" ("RepoName", "RepoUrl") VALUES(%s, %s) returning "RepoId"'
insert_query_authors = 'INSERT INTO public."Authors" ("AuthorName", "AuthorEmail") VALUES(%s, %s) returning "AuthorId"'
insert_query_files = 'INSERT INTO public."Files" ("RepoId", "FileName", "FilePath", "FileType", "LastModified", ' \
                       '"FileSizeBytes", "LinesOfCode") VALUES(%s, %s, %s, %s, %s, %s, %s) returning "FileId"'
insert_query_subexperts = 'INSERT INTO public."SubjectExperts" ("FileId", "AuthorId", "Score") VALUES(%s, %s, %s)'

for row in reader:
    RepoName = row['RepoName']
    RepoUrl = row['RepoUrl']
    FilePath = row['FilePath']
    LastModified = datetime.datetime.fromtimestamp(int(row['LastModified'])/1000.0)
    FileSizeBytes = row['FileSizeBytes']
    LinesOfCode = row['LinesOfCode']
    AuthorName = row['AuthorName']
    AuthorEmail = row['AuthorEmail']
    Score = float(row['Score'])

    FileName = "TestFN"
    FileType = "TestFT"

    # print(RepoName + RepoUrl + FilePath + FileSizeBytes + LinesOfCode + AuthorName + AuthorEmail + Score)

    cur.execute(insert_query_repos, (RepoName, RepoUrl))
    RepoId = cur.fetchone()[0]
    conn.commit()
    print(RepoId)

    cur.execute(insert_query_authors, (AuthorName, AuthorEmail))
    AuthorId = cur.fetchone()[0]
    conn.commit()
    print(AuthorId)

    cur.execute(insert_query_files, (RepoId, FileName, FilePath, FileType, LastModified, FileSizeBytes, LinesOfCode))
    FileId = cur.fetchone()[0]
    conn.commit()
    print(FileId)

    cur.execute(insert_query_subexperts, (FileId, AuthorId, Score))
    conn.commit()
    print("WE DONE")