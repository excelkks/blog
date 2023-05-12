#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


import os
import re
import sys
from shutil import copy as scopy
from shutil import move as smove
import argparse


def findformula(text):
    formula_re = re.search(r'(\$\$[^\$]*\$\$)|([^\$]\$[^\$]+\$[^\$])', text, re.DOTALL)
    if not formula_re:
        return [-1, -1]
    formula_start, formula_end = formula_re.span()
    if not formula_re.group(0).startswith('$$'):
        formula_start += 1
        formula_end -= 1
    return [formula_start, formula_end]


def cvtbs(src):
    dst = ''
    start_pos = 0
    while True:
        formula_start, formula_end = findformula(src[start_pos:])
        if formula_start > 0:
            formula = src[start_pos + formula_start: start_pos + formula_end]
            dst += src[start_pos:start_pos + formula_start]
            dst += formula.replace('\\\\', '\\\\\\\\')
            start_pos += formula_end
        else:
            break
    dst += src[start_pos:]
    return dst


def cvtfile(src, dst):
    print(src)
    org_f = open(src, 'r', encoding="utf-8")
    original_file = org_f.read()
    org_f.close()
    new_file = cvtbs(original_file)
    new_f = open(dst, 'w', encoding="utf-8")
    new_f.write(new_file)
    new_f.close()


def renew(src_path, dst_path):
    files = os.listdir(src_path)
    for file in files:
        if file.endswith('md'):
            cvtfile(os.path.join(src_path, file), 
                    os.path.join(dst_path, file))


def deploy(comment):
    deploy_path = "excelkks.github.io"
    cur_dir = os.getcwd()
    generate_cmd = "hugo -d " + deploy_path
    git_add_cmd = "git add ."
    git_commit_cmd = 'git commit -m "' + comment + '"' 
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--deploy", "-d", nargs=1,  dest="comment", help = "deploy blog to github with comment")
    group.add_argument("--renew", "-r", action ="store_true", help = "renew blog, convert double backslash to quadruple backslash")
    group.add_argument("--new", "-n", nargs=1, dest="post", help = "new post")

    # get absolute path of current file
    currdir = os.path.split(os.path.abspath(sys.argv[0]))[0]
    os.chdir(currdir)

    args = parser.parse_args()
    if args.post:
        post = str(args.post[0])
        new_post_cmd = "hugo new post/"+post + ".md"
        os.system(new_post_cmd)
        if not os.path.exists("data/post"):
            os.makedirs("data/post")
        if os.path.exists(os.path.join("data/post/",post+".md")):
            smove(os.path.join("data/post/",post+".md"), 
                    os.path.join("data/post/",post+".md.bk"))
            print(post+" exits, please check it rigth now!!!")
        scopy(os.path.join("content/post", post+".md"), os.path.join("data/post/",post+".md"))
        print("Created new post "+ os.path.join(currdir, "data/post/" + post))
    if(os.path.exists("data/post")):
        renew("data/post", "content/post")
    if args.comment:
        deploy(str(args.comment))
