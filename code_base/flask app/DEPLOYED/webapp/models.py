from app import db
from sqlalchemy.dialects.postgresql import JSON, DOUBLE_PRECISION
from sqlalchemy.sql.schema import PrimaryKeyConstraint

class Author(db.Model):
    __tablename__ = 'Authors'

    AuthorId = db.Column(db.BigInteger, primary_key=True)
    AuthorName = db.Column(db.Text)
    AuthorEmail = db.Column(db.Text)

    def __init__(self, name,email):
        self.AuthorName = name
        self.AuthorEmail = email

    def __repr__(self):
        return '<AuthorId {}>'.format(self.AuthorId)

class Repo(db.Model):
    __tablename__ = 'Repos'

    RepoId = db.Column(db.BigInteger, primary_key=True)
    RepoName = db.Column(db.Text, nullable = False)
    RepoUrl = db.Column(db.Text, nullable = False)

    def __init__(self, name,url):
        self.RepoName = name
        self.RepoUrl = url

    def __repr__(self):
        return '<RepoId {}>'.format(self.RepoId)

class File(db.Model):
    __tablename__ = 'Files'

    FileId = db.Column(db.BigInteger, primary_key=True)
    RepoId = db.Column(db.Integer, db.ForeignKey('Repos.RepoId'))
    FileName = db.Column(db.Text, nullable = False)
    FilePath = db.Column(db.Text, nullable = False)
    FileType = db.Column(db.Text, nullable = False)
    FileSizeBytes = db.Column(db.BigInteger, nullable = False)
    LinesOfCode = db.Column(db.Integer, nullable = False)
    LastModified = db.Column(db.DateTime(timezone = False), nullable = False)

    
    def __repr__(self):
        return '<FileId {}>'.format(self.FileId)

class SubjectExpert(db.Model):
    __tablename__ = 'SubjectExperts'

    __table_args__ = (
        PrimaryKeyConstraint('AuthorId', 'FileId'),
    )
    
    FileId = db.Column(db.BigInteger, db.ForeignKey('Files.FileId') )
    AuthorId = db.Column(db.BigInteger, db.ForeignKey('Authors.AuthorId') )
    Score = db.Column(db.Integer, nullable = False)

class FileDependency(db.Model):
    __tablename__ = 'FileDependencies'
    
    SourceFileId = db.Column(db.BigInteger, db.ForeignKey('Files.FileId'), primary_key = True )
    DestinationFileId = db.Column(db.BigInteger, db.ForeignKey('Files.FileId'), primary_key = True )  
    NoOfTimeChanged = db.Column(db.Integer, nullable = False)
    NormalizedChanged = db.Column(DOUBLE_PRECISION, nullable = False)


class BugProbablility(db.Model):
    __tablename__ = 'BugProbablities'
    
    FileId = db.Column(db.BigInteger, db.ForeignKey('Files.FileId'), primary_key = True )
    NoOfTimeChanged = db.Column(db.Integer)
    BuggyCommits = db.Column(db.Integer)
    BuggyCommitsPercentage = db.Column(DOUBLE_PRECISION)


