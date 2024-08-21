import requests
import re
import urllib
import random
import json

def login(username,password):
    headers = {"Content-Type":"application/x-www-form-urlencoded"}
    data = f"username={urllib.parse.quote(username)}&psd={urllib.parse.quote(password)}"
    session = requests.session()
    session.trust_env = False
    ret = session.post("http://192.168.1.1/cgi-bin/luci",data=data,headers=headers,allow_redirects=False)
    ret = session.post(url="http://192.168.1.1/cgi-bin/luci",data=data,headers=headers)
    matchObj = re.search(r'([a-z]|[0-9]){32}', str(ret.text))
    token = matchObj.group()
    return session,token

def list_port(session,token):
    ret = session.get(f"http://192.168.1.1/cgi-bin/luci/admin/settings/pmDisplay?_={random.random()}")
    return ret.json()

def add_port(session,token,name,client_ip,protocol,export,inport):
    headers = {"Content-Type":"application/x-www-form-urlencoded"}
    data = f"token={token}&op=add&srvname={urllib.parse.quote(name)}&client={client_ip}&protocol={protocol}&exPort={export}&inPort={inport}&_={random.random()}"
    ret = session.post("http://192.168.1.1/cgi-bin/luci/admin/settings/pmSetSingle",
            headers = headers,
            data = data
            )
    return ret.json()

def del_port(session,token,name):
    headers = {"Content-Type":"application/x-www-form-urlencoded"}
    data = f"token={token}&op=del&srvname={urllib.parse.quote(name)}&_={random.random()}"
    ret = session.post("http://192.168.1.1/cgi-bin/luci/admin/settings/pmSetSingle",
            headers = headers,
            data = data
            )
    return ret.json()

def disable_port(session,token,name):
    headers = {"Content-Type":"application/x-www-form-urlencoded"}
    data = f"token={token}&op=disable&srvname={urllib.parse.quote(name)}&_={random.random()}"
    ret = session.post("http://192.168.1.1/cgi-bin/luci/admin/settings/pmSetSingle",
            headers = headers,
            data = data
            )
    return ret.json()

def enable_port(session,token,name):
    headers = {"Content-Type":"application/x-www-form-urlencoded"}
    data = f"token={token}&op=enable&srvname={urllib.parse.quote(name)}&_={random.random()}"
    ret = session.post("http://192.168.1.1/cgi-bin/luci/admin/settings/pmSetSingle",
            headers = headers,
            data = data
            )
    return ret.json()

def enable_all_port(session,token):
    headers = {"Content-Type":"application/x-www-form-urlencoded"}
    data = f"token={token}&op=enable&_={random.random()}"
    ret = session.post("http://192.168.1.1/cgi-bin/luci/admin/settings/pmSetAll",
            headers = headers,
            data = data
            )
    return {}

def disable_all_port(session,token):
    headers = {"Content-Type":"application/x-www-form-urlencoded"}
    data = f"token={token}&op=disable&_={random.random()}"
    ret = session.post("http://192.168.1.1/cgi-bin/luci/admin/settings/pmSetAll",
            headers = headers,
            data = data
            )
    return {}

def del_all_port(session,token):
    headers = {"Content-Type":"application/x-www-form-urlencoded"}
    data = f"token={token}&op=del&_={random.random()}"
    ret = session.post("http://192.168.1.1/cgi-bin/luci/admin/settings/pmSetAll",
            headers = headers,
            data = data
            )
    print(ret.content)
    return {}

# 登录
session,token = login('useradmin','yourpassword')
print(session,token)

# 查看端口映射
ret_json = list_port(session,token)
print(json.dumps(ret_json,indent=4,sort_keys=True))

# 新增端口映射
ret_json = add_port(session,token,"我的小主机","192.168.1.24","BOTH",2052,80)
print(json.dumps(ret_json,indent=4,sort_keys=True))

# 关闭端口映射
ret_json = disable_port(session,token,"我的小主机")
print(json.dumps(ret_json,indent=4,sort_keys=True))

# 打开端口映射
ret_json = enable_port(session,token,"我的小主机")
print(json.dumps(ret_json,indent=4,sort_keys=True))

# 删除端口映射
ret_json = del_port(session,token,"我的小主机")
print(json.dumps(ret_json,indent=4,sort_keys=True))

# 开启所有端口映射
ret_json = enable_all_port(session,token)
print(json.dumps(ret_json,indent=4,sort_keys=True))

# 关闭所有端口映射
ret_json = disable_all_port(session,token)
print(json.dumps(ret_json,indent=4,sort_keys=True))

# 删除所有端口映射
ret_json = del_all_port(session,token)
print(json.dumps(ret_json,indent=4,sort_keys=True))
