import sys,os
import getpass
import re, shutil
from tempfile import mkstemp
import shlex
from string import maketrans
import difflib
import shutil
import errno
def cd_command(str) :
    try:
        os.chdir(current_working_dir+"/"+str.split()[1])
    except:
        print "directory not found"

def ls_command(str) :
    if str=="ls":
        content = os.listdir(".")
    else:
        content = os.listdir(str.split()[1])
    content.sort()
    for i in content : 
        print i
def pwd_command(current_working_dir):
    print current_working_dir

def touch_command(str) :
    if str in os.listdir("."):
        os.utime(str, None)
    else:
        file = open(str, "w")
        file.close()

def mkdir_command(str):
    try:
        os.mkdir(shlex.split(str)[1])
    except Exception as e:
        raise e
    pass

def move_command(str):
    try:
        shutil.move(shlex.split(str)[1], shlex.split(str)[2])
    except Exception as e:
        raise e
    pass

def copy_command(str):
    try:
        print os.getcwd()+"/"+shlex.split(str)[1]
        print os.getcwd()+"/"+shlex.split(str)[2]
        shutil.copytree(os.getcwd()+"/"+shlex.split(str)[1], os.getcwd()+"/"+shlex.split(str)[2])
        print "in try \n"
    except OSError as e:
        if e.errno == errno.ENOTDIR:
            shutil.copy(shlex.split(str)[1], shlex.split(str)[2])
        print "in OSErrror 1 "

while 1:
    home_dir = "/home/usr/gdrive"
    current_working_dir = os.getcwd()
    str = raw_input(">>> ")
    command = str.split()[0]
    if command == "exit":
        exit()
    if command == "cd":
        cd_command(str)        
    if command == "ls":
        ls_command(str)
    if command == "pwd":
        pwd_command(current_working_dir)
    if command == "touch":
        touch_command(str.split()[1])
    if command=="move":
        move_command(str)
    if command=="copy":
        copy_command(str)