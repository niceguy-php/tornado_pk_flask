# -*- coding: UTF-8 -*-
import paramiko
import ssh
import sys
import time
import requests

zzzc_host = ["192.168.254.43","192.168.254.40"]
shbt_host = [
    "192.168.254.43","192.168.254.40"
]

def httpTest(host,location ,count=0):
    url = "http://%s:9090/api/xx" % host
    params = {
        
    }
    headers = {'Content-Type': 'application/json;charset=UTF-8'}
    t1 = time.time()
    res = requests.request("post", url, json=params, headers=headers)
    t2 = time.time()
    host_str = host
    if len(host) < 14:
        diff = 14-len(host)
        for i in range(diff):
            host_str += " "
    print "[%s]\tlocation=%s\tip=%s\tcode=%s\tresult=%s\ttime=%s" % (count, location, host_str, res.status_code, res.text, t2 - t1)

if len(sys.argv)==1:
    location ='zzzc'
    host_list = zzzc_host
else:
    location = sys.argv[1]
    if location == 'zzzc':
        host_list = zzzc_host
    elif location == 'shbt':
        host_list = shbt_host
    elif location == 'http':
        print '------------------------------------------------------------------zzzc---------------------------------------------------------------------'
        i = 1
        for h in zzzc_host:
            httpTest(h,'zzzc',i)
            i += 1
        print '------------------------------------------------------------------shbt---------------------------------------------------------------------'
        j = 1
        for h in shbt_host:
            httpTest(h,'shbt',j)
            j += 1
        sys.exit(0)
    else:
        sys.exit(0)
# sys.exit(0)

def login_prompt(chan):
    buff = ""
    while not buff.endswith(username+': '):  # true
        resp = chan.recv(9999)
        buff += resp.decode('utf8')
    return buff

def cmd_result(chan):
    buff = ''
    while not buff.endswith('$ '):
        resp = chan.recv(9999)
        try:
            buff += resp.decode('utf8')
        except Exception, e:
            buff += resp.decode('gb18030')
    return buff

def git_pull_prompt_user(chan):
    buff = ''
    while not buff.endswith('10080\': '):
        resp = chan.recv(9999)
        try:
            buff += resp.decode('utf8')
        except Exception, e:
            buff += resp.decode('gb18030')
    return buff

def git_pull_prompt_passwd(chan):
    buff = ''
    while not buff.endswith('10080\': '):
        resp = chan.recv(9999)
        try:
            buff += resp.decode('utf8')
        except Exception, e:
            buff += resp.decode('gb18030')
    return buff

def sudo_cmd(chan, cmd):
    chan.send(cmd + '\n')
    print login_prompt(chan)
    chan.send(password)
    chan.send('\n')





if location not in ['zzzc','shbt']:
    print "error location:%s" % location
    sys.exit(1)

print host_list
# sys.exit(0)
count = 1
for host in host_list:
    print '------------------------------------------------------------------pubulis number [ %s ]---------------------------------------------------------------------'%count
    username=""
    password=""
    passinfo = '\'s password:'

    git_user = ''
    git_pass = ''

    test_env = False

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host,22,username,password,timeout=5)

    chan=ssh.invoke_shell()

    buff = ''
    # print cmd_result(chan)
    if test_env:
        cd_cmd = 'cd /test_code_path/'
    else:
        cd_cmd = 'cd /code_path/'

    chan.send(cd_cmd+'\n')
    cmd_result(chan)

    chan.send('sudo ls -lh'+'\n')
    login_prompt(chan)
    # resp = chan.recv(100000)
    # print resp
    chan.send(password)
    chan.send('\n')
    cmd_result(chan)

    chan.send('sudo git pull'+'\n')
    git_pull_prompt_user(chan)
    chan.send(git_user+'\n')
    # chan.send('\n')
    git_pull_prompt_passwd(chan)
    chan.send(git_pass+'\n')
    print cmd_result(chan)


    chan.send('php server.php reload'+'\n')
    print cmd_result(chan)
    time.sleep(1)
    # chan.send('tail log/swoole.log'+'\n')
    # print cmd_result(chan)

    ssh.close()
    httpTest(host,location,count)
    count += 1