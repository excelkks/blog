#!/usr/bin/env python3
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("comment", help = "comment of git commit")
args = parser.parse_args()

deploy_path = "excelkks.github.io"
cur_dir = os.getcwd()

generate_cmd = "hugo -d " + deploy_path
git_add_cmd = "git add ."
git_commit_cmd = 'git commit -m "' + str(args.comment) + '"' 
git_push_cmd = "git push"

os.system(generate_cmd)

os.chdir(os.path.join(cur_dir, deploy_path))
os.system(git_add_cmd)
os.system(git_commit_cmd)
os.system(git_push_cmd)

os.chdir(cur_dir)
os.system(git_add_cmd)
os.system(git_commit_cmd)
os.system(git_push_cmd)
