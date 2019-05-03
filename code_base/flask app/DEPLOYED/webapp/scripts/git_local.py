#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 20:05:45 2019

@author: suvodeepmajumder
"""

from pygit2 import clone_repository
from pygit2 import GIT_SORT_TOPOLOGICAL, GIT_SORT_REVERSE,GIT_MERGE_ANALYSIS_UP_TO_DATE,GIT_MERGE_ANALYSIS_FASTFORWARD,GIT_MERGE_ANALYSIS_NORMAL,GIT_RESET_HARD
from pygit2 import Repository
import shutil,os
import pygit2
import re
from os import listdir
from os.path import isfile, join
from datetime import datetime
import platform
import time
from scripts.utils import utils


class git_local(object):
    
    def __init__(self,repo_url,repo_name):
        self.repo_url = repo_url
        self.repo_name = repo_name
        self.repos = []
        self.commit_objs = []
        if platform.system() == 'Darwin' or platform.system() == 'Linux':
            self.temp_path = os.getcwd() + '/temp_repo/' 
            self.repo_path = os.getcwd() + '/temp_repo/' + repo_name
        else:
            self.repo_path = os.getcwd() + '\\temp_repo\\' + repo_name
            self.temp_path = os.getcwd() + '\\temp_repo\\'
            
    def clone_repo(self):
        git_path = pygit2.discover_repository(self.repo_path)
        if git_path is not None:
            self.repo = pygit2.Repository(git_path)
            return self.repo
        if not os.path.exists(self.repo_path):
            os.makedirs(self.repo_path)
        self.repo = clone_repository(self.repo_url, self.repo_path)
        return self.repo
    
    def get_commits(self):
        commit_objs = []
        commits = []
        for commit in self.repo.walk(self.repo.head.target, GIT_SORT_TOPOLOGICAL | GIT_SORT_REVERSE):
            result = self.isBuggyCommit(commit.message)
            commit_objs.append([commit,result])
            commits.append([commit.id.hex,time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(commit.commit_time))
                ,commit.author.name,commit.author.email,
                            commit.committer.name,commit.committer.email,commit.message,commit.parent_ids,result])
        self.commit_objs = commit_objs
        return commits
    
    def get_committed_files(self):
        committed_files = []
        commits = self.commit_objs
        for i in range(len(commits)):
            try:
                if len(commits[i][0].parents) == 0:
                    continue
                t0 = commits[i][0]
                if i != 0:
                    t1 = commits[i][0].parents[0]
                else:
                    continue
                _diff = self.repo.diff(t1,t0)
                for j in _diff.deltas:
                    committed_files.append([commits[i][0].id.hex,j.new_file.id.hex, j.new_file.mode,j.new_file.path,commits[i][1]])
            except:
                print("commit:",commits[i][0].id)
                continue
        return committed_files
    
    def get_diffs(self,commits):
        diffs = {}
        for i in range(len(commits)):
            t0 = self.repo.get(commits[i])
            files = {}
            if len(t0.parents) == 0:  
                continue
            if i != 0:
                t1 = t0.parents[0]
            else:
                continue
            _diff = self.repo.diff(t1,t0)
            for diff_i in _diff.__iter__():
                file_path = diff_i.delta.new_file.path
                old_lineno = []
                new_lineno = []
                for x in diff_i.hunks:
                    for y in x.lines:
                        old_lineno.append(y.old_lineno)
                        new_lineno.append(y.new_lineno)
                files[diff_i.delta.new_file.id] = {'file_path':file_path, 'old_lines':len(old_lineno),'new_lines':len(new_lineno)}
            diffs[t0.id.hex] = {'files':files,'object':t0}
        return diffs

    def get_blame(self,file_path):
        return self.repo.blame(file_path,flags = 'GIT-BLAME_TRACK_COPIES_ANY_COMMIT_COPIES')

    def isBuggyCommit(self, commit):
        res=re.search(r'\b{bug|fix|issue|error|correct|proper|deprecat|broke|optimize|patch|solve|slow|obsolete|vulnerab|debug|perf|memory|minor|wart|better|complex|break|investigat|compile|defect|inconsist|crash|problem|resol|#}\b',utils().stemming(commit),re.IGNORECASE)
        if res is not None:
            return True
        else:
            return False


    