#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 19:02:56 2019

@author: suvodeepmajumder
"""

import scripts.api as api
import json
import pandas as pd
import numpy as np

class get_data(object):
    
    def __init__(self,token,repo_owner,api_base_url,repo_name):
        self.access_token = token
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.api_base_url = api_base_url
        self.get_client()
        
    def get_client(self):
        self.client = api.GitClient({'access_token': self.access_token,
                       'repo_owner': self.repo_owner, 
                       'repo_name': self.repo_name,
                       'api_base_url': self.api_base_url})
        
    def get_users(self):
        url = self.api_base_url + '/repos/' + self.repo_owner + '/' + self.repo_name + '/stats/contributors'
        users = []
        result = [0]*100
        page_number = 1
        while len(result) >= 100 :
            paged_url = url + '?page=' + str(page_number) + '&per_page=100'
            print("Now at url:",paged_url)
            page_number += 1
            res = self.client.get(paged_url)
            result = json.loads(res.content)
            for i in range(len(result)):
                user_name = 'jonny boy'
                #user_name = result['name']
                user_logon = result[i]['author']['login']
                users.append([user_name,user_logon]) 
        print(len(users))
        return users