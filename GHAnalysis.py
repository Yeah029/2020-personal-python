import json
import os
import argparse

class Data:

    def __init__(self, comb:int =0, address:int=None):
        if comb == 1:
            if(address == None):
                raise RuntimeError('error: init failed')
            self.AllJson(address)
            self.SaveToLocal()
        else:
            self.localU={}
            self.localR={}
            self.userAndrepo={}
            if self.ReadLocal() == False:
                raise RuntimeError("file is not exist")
        self.uEvent = {}
        self.rEvent = {}
        self.urEvent = {}
    def AllJson(self,address:str):#解析文件夹中的所有json
        for root, dic, files in os.walk(address):
            for f in files:
                if f[-5:] == ".json":
                    jsonPath = f
                    self.OneJson(address, jsonPath)

    def OneJson(self, address:str, jPath:str):#单个json解析函数
        f = open(address + '\\' + jPath, 'r', encoding='utf-8')

        try:
            while True:
                thefile = f.readline()
                if thefile:
                    jsLoads = json.loads(thefile)

                    if not jsLoads["type"] in ['PushEvent','IssueCommentEvent',
                                            'IssuesEvent','PullRequestEvent']:
                        continue
                    if not jsLoads["actor"]["login"] in self.uEvent.keys():
                        event = {'PushEvent':0,'IssueCommentEvent':0,
                                 'IssuesEvent':0,'PullRequestEvent':0}
                        self.uEvent[jsLoads["actor"]["login"]] = event

                    if not jsLoads["repo"]["name"] in self.rEvent.keys():
                        event = {'PushEvent':0,'IssueCommentEvent':0,
                                 'IssuesEvent':0,'PullRequestEvent':0}
                        self.rEvent[jsLoads["repo"]["name"]] = event

                    if not jsLoads["actor"]["login"]+'&'+jsLoads["repo"]["name"] in self.urEvent.keys():
                        event = {'PushEvent': 0, 'IssueCommentEvent': 0,
                                 'IssuesEvent': 0, 'PullRequestEvent': 0}
                        self.urEvent[jsLoads["actor"]["login"] + '&' + jsLoads["repo"]["name"]] = event
                    self.uEvent[jsLoads["actor"]["login"]][jsLoads['type']] += 1
                    self.rEvent[jsLoads["repo"]["name"]][jsLoads['type']] += 1
                    self.urEvent[jsLoads["actor"]["login"] + '&' + jsLoads["repo"]["name"]][jsLoads['type']] += 1
                else:
                    break
        except:
            pass
        finally:
            f.close()

    def ReadLocal(self) -> bool:#判断数据是否成功存在本地
        if not os.path.exists('user.json') and not os.path.exists(
                'repo.json') and not os.path.exists('userrepo.json'):
            return False
        x = open('user.json', 'r', encoding='utf-8').read()
        self.localU = json.loads(x)
        x = open('repo.json', 'r', encoding='utf-8').read()
        self.localR = json.loads(x)
        x = open('userepo.json', 'r', encoding='utf-8').read()
        self.userandrepo = json.loads(x)
        return True

    def SaveToLocal(self):
        try:
            with open('user.json', 'w', encoding = 'utf-8') as f:
                json.dump(self.uEvent, f)
            with open('repo.json', 'w', encoding = 'utf-8') as f:
                json.dump(self.rEvent, f)
            with open('userepo.json', 'w', encoding = 'utf-8') as f:
                json.dump(self.urEvent, f)
        except:
            raise RuntimeError("save error")
        finally:
            f.close()

    def QueryByUser(self, user:str, event: str):
        if not user in self.theUser.keys():
            return 0
        return self.theUser[user][event]

    def QueryByRepo(self, repo: str, event: str):
        if not self.theRepo.get(repo, 0):
            return 0
        return self.theUser[repo][event]

    def QueryByUserAndRepo(self, user:str, repo:str, event: str):
        if not self.theUserAndRepo.get(user + '&' + repo, 0):
            return 0
        return self.theUserAndRepo[user + '&' + repo][event]


class Run:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.data = None
        self.ArgInit()
        print(self.Analyse())

    def ArgInit(self):
        self.parser.add_argument('-i', '--init')
        self.parser.add_argument('-u', '--user')
        self.parser.add_argument('-r', '--repo')
        self.parser.add_argument('-e', '--event')

    def Analyse(self):
        if self.parser.parse_args().init:
            self.data = Data(1,self.parser.parse_args().init)
            return 0
        else:
            #if self.data is None:
            self.data = Data(0,None)
            if self.parser.parse_args().event:
                if self.parser.parse_args().user:
                    if self.parser.parse_args().repo:
                        res = self.data.QueryByUserAndRepo(
                            self.parser.parse_args().user, self.parser.parse_args().repo,
                            self.parser.parse_args().event)
                    else:
                        res = self.data.QueryByUser(
                            self.parser.parse_args().user, self.parser.parse_args().event)
                elif self.parser.parse_args().repo:
                    res = self.data.QueryByRepo(
                        self.parser.parse_args().repo, self.parser.parse_args().event)
                else:
                    raise RuntimeError('error: argument -l or -c are required')
            else:
                raise RuntimeError('error: argument -e is required')
        return res


if __name__ == '__main__':

    run = Run()