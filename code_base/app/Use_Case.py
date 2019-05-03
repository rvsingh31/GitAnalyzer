import get_api_data,git_local
import pandas as pd
from flatten_dict import flatten
from datetime import datetime
from dateutil import relativedelta
import random as rd
import os


class Use_Case(object):

    def __init__(self,repo_owner,git_url,repo_name):
        self.repo_owner = repo_owner
        self.git_url = git_url
        self.repo_name = repo_name
        self.local = git_local.git_local(self.git_url,self.repo_name)
        self.local.clone_repo()
        self.get_commits()
        self.get_committed()
        self.get_diffs()
        self.generate_file_timeline()


    def get_commits(self):
        self.commits = self.local.get_commits()
        self.commit_df = pd.DataFrame(self.commits, columns = ['commit_id','commit_time','author','author_email',
                                             'committer','committer_email','comments','commit_parent','bug_fixing'])

    def get_committed(self):
        self.committed_files = self.local.get_committed_files()
        self.committed_files_df = pd.DataFrame(self.committed_files, columns = ['commit_id','file_id','modification_type',
        'file_name','bug_fixing'])
    
    def get_diffs(self):
        self.diffs = self.local.get_diffs(self.commit_df.commit_id.values.tolist())

    def generate_file_timeline(self):
        self.latest_commit_time = {}
        self.oldest_commit_time = {}
        for commit in self.commits:
            if commit[0] == 'ea6bdef57db2906323deeaa648cabab69ebbdefc':
                continue
            try:
                for file_id in self.diffs[commit[0]]['files'].keys():
                    if self.diffs[commit[0]]['files'][file_id]['file_path'] not in self.latest_commit_time:
                        self.latest_commit_time[self.diffs[commit[0]]['files'][file_id]['file_path']] = commit[1]
                        self.oldest_commit_time[self.diffs[commit[0]]['files'][file_id]['file_path']] = commit[1]
                    else:
                        if self.latest_commit_time[self.diffs[commit[0]]['files'][file_id]['file_path']] < commit[1]:
                            self.latest_commit_time[self.diffs[commit[0]]['files'][file_id]['file_path']] = commit[1]
                        if self.oldest_commit_time[self.diffs[commit[0]]['files'][file_id]['file_path']] > commit[1]:
                            self.oldest_commit_time[self.diffs[commit[0]]['files'][file_id]['file_path']] = commit[1]
            except ValueError:
                print(commit[0])
                continue
        return 

    
    def UC1(self):
        uc1 = []
        for commit in self.commits:
            try:
                for file_id in self.diffs[commit[0]]['files'].keys():
                    file = os.getcwd() + '/temp_repo/' + self.repo_name + '/' + self.diffs[commit[0]]['files'][file_id]['file_path']
                    exists = os.path.isfile(file)
                    if exists:
                        # Store configuration file values
                        latest = datetime.strptime(self.latest_commit_time[self.diffs[commit[0]]['files'][file_id]['file_path']],'%Y-%m-%d %H:%M:%S')
                        oldest = datetime.strptime(self.oldest_commit_time[self.diffs[commit[0]]['files'][file_id]['file_path']],'%Y-%m-%d %H:%M:%S')
                        current = datetime.strptime(commit[1],'%Y-%m-%d %H:%M:%S')
                        # Normalization based on ration between delta of oldest chnage and latest change
                        latest_diff = abs(relativedelta.relativedelta(current,latest).months)
                        oldest_diff = abs(relativedelta.relativedelta(current,oldest).months)
                        total_diff = abs(relativedelta.relativedelta(latest,oldest).months)
                        if latest_diff == 0:
                            latest_diff = 1
                        if oldest_diff == 0:
                            oldest_diff = 1  
                        if total_diff == 0:
                            total_diff = 1
                        time_norm = (oldest_diff/latest_diff)/total_diff

                        uc1.append([commit[0],commit[1],commit[2],commit[3],
                                self.diffs[commit[0]]['files'][file_id]['file_path'],
                                    self.diffs[commit[0]]['files'][file_id]['new_lines']*time_norm])
                    else:
                        # Keep presets
                        continue
            except KeyError:
                continue
        uc1_df = pd.DataFrame(uc1,columns = ['commit_id','commit_time','AuthorName','AuthorEmail','FilePath','Score'])
        uc1_df_matrix = uc1_df.drop(labels = ['commit_time','commit_id'],axis = 1)
        uc1_df_dev_sum = uc1_df_matrix.groupby(['FilePath','AuthorEmail','AuthorName'],as_index=False).sum()
        uc1_df_dev_sum.sort_values(by=['FilePath','Score'],inplace = True,ascending = False)
        uc1_df_dev_sum['LinesOfCode'] = [0]*uc1_df_dev_sum.shape[0]
        uc1_df_dev_sum['FileSizeBytes'] = [0]*uc1_df_dev_sum.shape[0]
        uc1_df_dev_sum['LastModified'] = [0]*uc1_df_dev_sum.shape[0]
        uc1_df_dev_sum['RepoName'] = [0]*uc1_df_dev_sum.shape[0]
        uc1_df_dev_sum['RepoUrl'] = [0]*uc1_df_dev_sum.shape[0]
        for i in range(uc1_df_dev_sum.shape[0]):
            try:
                file = os.getcwd() + '/temp_repo/' + self.repo_name + '/' + uc1_df_dev_sum.iloc[i,0]
                file_size = os.path.getsize(file)
                num_lines = sum(1 for line in open(file))
            except:
                file_size = 0
                num_lines = 0
                print("Not there")
                continue
            uc1_df_dev_sum.iloc[i,4] = num_lines
            uc1_df_dev_sum.iloc[i,5] = file_size
            uc1_df_dev_sum.iloc[i,6] = self.latest_commit_time[uc1_df_dev_sum.iloc[i,0]]
            uc1_df_dev_sum.iloc[i,7] = self.repo_name
            uc1_df_dev_sum.iloc[i,8] = self.git_url
        return uc1_df_dev_sum

    
    def UC2(self):
        temp_df = self.committed_files_df
        temp_df = temp_df.drop(labels = ['file_id','modification_type'],axis = 1)
        uc2 = {}
        total_file_changed = {}
        for commit in temp_df.commit_id.unique():
            files = temp_df[temp_df['commit_id'] == commit].file_name.values.tolist()
            for file_s in files:
                _file = os.getcwd() + '/temp_repo/' + self.repo_name + '/' + file_s
                exists = os.path.isfile(_file)
                if exists:
                    if file_s not in uc2:
                        uc2[file_s] = {}
                        total_file_changed[file_s] = 1
                    else:
                        total_file_changed[file_s] += 1
                    for file_d in files:
                        if file_s == file_d:
                            continue
                        else:
                            if file_d not in uc2[file_s]:
                                uc2[file_s][file_d] = 1
                            else:
                                uc2[file_s][file_d] += 1
        uc2_matrix = []
        for file_s in uc2:
            for file_d in uc2[file_s]:
                uc2_matrix.append([file_s,file_d,uc2[file_s][file_d],uc2[file_s][file_d]/total_file_changed[file_s],self.repo_name,self.git_url])
        uc2_matrix_df = pd.DataFrame(uc2_matrix, columns = ['SourceFilePath','DestinationFilePath','NoOfTimeChanged','NormalizedChange','RepoName','RepoUrl'])
        return uc2_matrix_df



    def UC3(self):
        temp_df = self.committed_files_df
        temp_df = temp_df.drop(labels = ['file_id','modification_type'],axis = 1)
        total_file_changed = {}
        total_bugs = {}
        for commit in temp_df.commit_id.unique():
            files = temp_df[temp_df['commit_id'] == commit].file_name.values.tolist()
            buggy = temp_df[temp_df['commit_id'] == commit].bug_fixing.values.tolist()[0]
            for file_s in files:
                _file = os.getcwd() + '/temp_repo/' + self.repo_name + '/' + file_s
                exists = os.path.isfile(_file)
                if exists:
                    if file_s not in total_file_changed:
                        total_file_changed[file_s] = 1
                        total_bugs[file_s] = 0
                        if buggy:
                            total_bugs[file_s] += 1
                    else:
                        total_file_changed[file_s] += 1
                        if buggy:
                            total_bugs[file_s] += 1
                else:
                    continue
                    
        uc3_matrix = []
        for file_s in total_file_changed:
                uc3_matrix.append([file_s,total_file_changed[file_s],total_bugs[file_s],
                                total_bugs[file_s]/total_file_changed[file_s],self.repo_name,self.git_url])
        uc3_matrix_df = pd.DataFrame(uc3_matrix, columns = ['SourceFilePath','NoOfTimeChanged','BuggyCommits',
                                                            'BuggyCommitsPercentage','RepoName','RepoUrl'])
        return uc3_matrix_df
        


    
    
