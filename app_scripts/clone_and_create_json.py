#!/usr/bin/env python
# coding: utf-8

import os
import get_api_data as get_api_data
import git_local as git_local
import pandas as pd
from flatten_dict import flatten
from datetime import datetime
from dateutil import relativedelta
import pprint
import json
from pathlib import Path, PureWindowsPath
import platform


def create_json(git_url):

    access_token = 'ef66b5bf5fd6c14d63586bf00caa9e72c78cc675'
    repo_owner = 'rspec'
    # git_url = 'git://github.com/rspec/rspec-rails.git'
    api_base_url = 'https://api.github.com'
    repo_name = git_url.split('/')[-1].split('.')[0]
    client = get_api_data.get_data(access_token,repo_owner,api_base_url,repo_name) 
    local = git_local.git_local(git_url,repo_name)
    local.clone_repo()
    path = local.repo_path

    flag = False
    root = ""
    target_path = os.path.join("static","json","{}.json".format(repo_name))
    if platform.system() == 'Darwin' or platform.system() == 'Linux':
        root = path + "/"
    else:
        flag = True
        root = path + "\\"
        
    def path_to_dict(path):
        d = {'name': os.path.basename(path)}
        rel = path.replace(root,'')
        if flag:
            rel = '/'.join(rel.split('\\'))
        d['path'] = rel
        if os.path.isdir(path):
            d['type'] = r"directory"
            d['children'] = [path_to_dict(os.path.join(path,x)) for x in os.listdir(path)]
        else:
            d['type'] = "file"
        return d

    structure = json.dumps(path_to_dict(path))
    file = open(target_path,"w")
    file.write(structure)
    file.close()
