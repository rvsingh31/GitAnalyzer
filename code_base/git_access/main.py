import Use_Case



class run_analysis(object):

    def __init__(self,repo_owner,repo_name,git_url):
        self.repo_owner = repo_owner
        self.git_url = git_url
        self.repo_name = repo_name
        

    def analyze(self):
        uc = Use_Case.Use_Case(self.repo_owner,self.repo_name,self.git_url)
        UC1_df = uc.UC1()
        UC2_df = uc.UC2()
        UC3_df = uc.UC3()
        return UC1_df,UC2_df,UC3_df



if __name__ == "__main__":
    repo_owner = 'mochajs'
    repo_name = 'mocha'
    git_url = 'git://github.com/mochajs/mocha.git'
    analyzer = run_analysis(repo_owner,repo_name,git_url)
    UC1, UC2, UC3 = analyzer.analyze()
        