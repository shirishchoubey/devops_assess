import os
import requests
import subprocess

def get_url(repo):

    return "https://github.com/{}".format(repo)

def clone_repo(repo):
    repo_url = get_url(repo)
    os.system("git clone {} {} --quiet".format(repo_url, repo.split('/')[-1]))
    return os.getcwd()+"/"+repo.split('/')[-1]

def check_if_valid_url(repo):

    repo_url = get_url(repo)
    try:
        response = requests.get(repo_url)
    except requests.ConnectionError as exception:
        print("{} doesnot exist on public repository of github".format(repo))


def get_latest_commit(path):

    os.chdir("{}".format(path))
    # os.sleep(2)
    commit = subprocess.check_output("git log|head -1|cut -d' ' -f2", shell=True)
    author = subprocess.check_output("git log|sed -n '2p'|cut -c 9-",shell=True)
    # print("{}:{}".format(commit,author))
    return (commit.rstrip().decode("utf-8"), author.rstrip().decode("utf-8"))

cwd = os.getcwd()
file = open("{}/github_repo.csv".format(cwd), "w")

list_repositories = ["hashicorp/vault", "docker/compose", "kubernetes/kubernetes"]

for repo in list_repositories:
    url = get_url(repo)
    check_if_valid_url(url)
    pwd=clone_repo(repo)
    commit, author = get_latest_commit(pwd)
    # print("{}:{}".format(commit,author))
    file.write("{}:{}:{}:{}\n".format(repo.split('/')[-1],url,commit,author))
    os.chdir(cwd)
file.close()