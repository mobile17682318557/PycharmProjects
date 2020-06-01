import json,requests
import pymysql
import time
import datetime
import sys
class zabbix:
 # zabbix 及pymysql初始化
 def __init__(self):
    self.url = 'http://211.140.17.123/zabbix/api_jsonrpc.php'
    self.headers = {'Content-Type': 'application/json'}
    self.authid=''
    self.db= pymysql.connect("localhost","root","123456","braindev" )

    auth = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": "zhuye",  ###验证
            "password": "zabbix"
        },
        "id": 1,
        "auth": None,
    }
    self.db.set_charset('utf8mb4')
    response = requests.post(self.url, data=json.dumps(auth), headers=self.headers)
    authid = json.loads(response.text)['result']  ### auth的id  也就是token
    self.authid = authid
 #获取host列表
 def get_hosts(self):
        neirong = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": [
                    "hostid",
                    "host",
                    "status"
                ],
                "selectInterfaces": [
                    "ip"
                ]
            },
            "id": 2,
            "auth": self.authid
        }
        response = requests.post(self.url, data=json.dumps(neirong), headers=self.headers)
        json_host_array=json.loads(response.text)['result']

        #for i in json_host_array:
        #for i in json_host_array:

           #print(i['host'])
           #print(i['interfaces'][0]['ip'])
           #print(i)

        return json_host_array
 #获取item列表
 def get_items(self,hostid):
        content = {
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "output": [
                    "key_",
                    "name",
                    "lastvalue"
                ],
                "hostids": [
                    hostid
                ]
            },
            "id": 3,
            "auth": self.authid
        }
        response = requests.post(self.url, data=json.dumps(content), headers=self.headers)
        json_item_array=json.loads(response.text)['result']

        #for i in json_host_array:
        #for i in json_host_array:

           #print(i['host'])
           #print(i['interfaces'][0]['ip'])
           #print(i)

        return json_item_array


# 打开数据库连接


# 使用 cursor() 方法创建一个游标对象 cursor
time1=time.time()
obj1=zabbix()
json_host_array=obj1.get_hosts()
try:
     for json_host in json_host_array:
        if json_host['hostid']==None:
            continue
        #if json_host['hostid']!='10107':
        #    continue
        itemarray=obj1.get_items(json_host['hostid'])
        if itemarray is None:
            continue
        #对hostid判断是否存在 有则更新 无则插入
        cursor=obj1.db.cursor()
        cursor.execute("select count(host_id) from br_hosts where host_id = "+json_host['hostid'])
        # 使用 execute()  方法执行 SQL 查询
        host_up = cursor.fetchall()
        #bond0 mac
        bmac = ''
        #cpu型号
        cpu = ''
        #home磁盘
        disk = ''
        #总内存
        memory = ''
        #操作系统位数
        os = ''
        hosttype = 0
        creator = 0
        modifor = 0

        #遍历item 匹配出需要的属性
        for item in itemarray:
          if 'system.hw.macaddr[bond0,short]'==item['key_']:
              bmac = item['lastvalue']
          if 'system.hw.cpu[0,model]'==item['key_']:
              cpu = item['lastvalue']
          if 'vfs.fs.size[/home,total]'==item['key_']:
              disk = item['lastvalue']
          if 'vm.memory.size[total]'==item['key_']:
              memory = item['lastvalue']
          if 'system.sw.arch'==item['key_']:
              os = item['lastvalue']
        #有hostid则更新 无则插入
        #cursor.execute返回类型为二级元祖 这里我们取第一个元素
        if host_up[0][0]:
            sql='update br_hosts set host_id=%s,host_name=%s,bip=bip,bmac=%s,nip=%s,nmac=nmac,host_status=%s,host_type=0,cpu=%s,disk=%s,memory=%s,os=%s,ipv6=ipv6,modify_time=%s,modifor=0 where host_id=%s'
            cursor.execute(sql,(json_host['hostid'],json_host['host'],bmac,json_host['interfaces'][0]['ip'],json_host['status'],cpu,disk,memory,os,datetime.datetime.now().strftime("%Y-%m-%d %X"),json_host['hostid']))
        else:
            sql='insert into br_hosts (host_id,host_name,bip,bmac,nip,nmac,host_status,host_type,cpu,disk,memory,os,ipv6,create_time,creator,modify_time,modifor) value (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            cursor.execute(sql,(json_host['hostid'],json_host['host'],'bip',bmac,json_host['interfaces'][0]['ip'],'nmac',json_host['status'],0,cpu,disk,memory,os,'ipv6',datetime.datetime.now().strftime("%Y-%m-%d %X"),0,datetime.datetime.now().strftime("%Y-%m-%d %X"),0))
     obj1.db.commit()
except:
     print('发生了错误',sys.exc_info()[0])
     obj1.db.rollback()
# 关闭数据库连接
obj1.db.close()
time2=time.time()
print(time2-time1)

