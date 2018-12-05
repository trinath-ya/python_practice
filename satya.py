#!/usr/bin/python
import os
import time
import subprocess
import paramiko
import datetime
import pymysql
import pandas as pd
now = datetime.datetime.now()
t=now.strftime("%H:%M:%S")
dt=now.strftime("%Y-%m-%d")
f=open("/home/ec2-user/tlgcdb_memory/tlgcdb_apiips.txt","r")
data=f.readlines()
key_path="/home/ec2-user/.ssh/.tlgcdb-ore-prd-key.pem"
username="ec2-user"
com="free"
region="US"
from_date="2018-12-03 23:01:00"
to_date="2018-12-04 23:45:00"


def memory(key_path,ip):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    privkey = paramiko.RSAKey.from_private_key_file(key_path)
    ssh.connect(ip,username='ec2-user',pkey=privkey)
    stdin, stdout, stderr = ssh.exec_command('free -m')
    stdin.flush()
    m=stdout.read()
    s=m.split()
    mem=s[8]
    return mem

def db():
    try:
        conn = pymysql.connect(host="localhost", user="root", passwd="tlg$123", database="tlg")
        return conn
    except:
        print "Unable to connect the database"
        return 0
def ips():
        con=db()
        cur=con.cursor()
        q="select IPAddress from tlg_memory where Date BETWEEN '%s' AND '%s'"%(from_date,to_date)
        d=cur.execute(q)
        Server_ips=cur.fetchall()
        ips=[]
        for i in Server_ips:
                p=i[0]
                ips.append(p)
        unique = reduce(lambda l, x: l+[x] if x not in l else l, ips, [])
        return unique
def time():
        con=db()
        cur=con.cursor()
        q="select Time from tlg_memory where Date BETWEEN '%s' AND '%s'"%(from_date,to_date)
        d=cur.execute(q)
        Server_ips=cur.fetchall()
        ts=[]
        for i in Server_ips:
                p=i[0]
                ts.append(p)
        unique = reduce(lambda l, x: l+[x] if x not in l else l, ts, [])
        return unique
def date():
        con=db()
        cur=con.cursor()
        q="select Date from tlg_memory where Date BETWEEN '%s' AND '%s'"%(from_date,to_date)
        d=cur.execute(q)
        Server_ips=cur.fetchall()
        ips=[]
        for i in Server_ips:
                p=i[0]
                ips.append(p)
        unique = reduce(lambda l, x: l+[x] if x not in l else l, ips, [])
        return unique
def stime():
        x=[]
        x.append("Time UTC")
        for i in time():
              t=i
              x.append(t)
        return x

print "1. Input\n2. Output\n"
n=raw_input("Enter your option:")
if n=="1":
    for row in data[1:]:
        ip= row.strip()
        m=memory(key_path,ip)
        print "Date:%s , Time:%s , Region:US , IPAddress:%s , Memory:%s"%(dt,t,ip,m)
        q="insert into tlg_memory values('%s', '%s' , '%s', '%s', '%s')"%(dt,t,region,ip,m)
        con=db()
        cur=con.cursor()
        try:
            cur.execute(q)
            con.commit()
            con.close()
        except:
            print "Database connection is not available"
elif n=="2":
#        try:
           f=open("tlgcdb_report.csv","w")
           g=stime()
           f.writelines(["%s," % (item)  for item in g])
           f.write("\n")

           f=open("tlgcdb_report.csv","a")
           for ip in ips():
                k=[]
                k.append(ip)
                con=db()
                cur=con.cursor()
                q="select Memory from tlg_memory where IPAddress='%s' and Date BETWEEN '%s' AND '%s'"%(ip,from_date,to_date)
                d=cur.execute(q)
                p=cur.fetchall()

                q1="select Time from tlg_memory where IPAddress='%s' and Date BETWEEN '%s' AND '%s'"%(ip,from_date,to_date)
                d1=cur.execute(q1)
                p1=cur.fetchall()
                b=g[:]
                del b[0]
                h=list(p1)
                for i in b:
                        if i!=h[0][0]:
                                k.append(" ")
                        else:
                            break
                for i in p:
                      l=i[0]
                      k.append(l)
                #print k
                f.writelines(["%s," % (item)  for item in k])
                f.write("\n")

#df = pd.read_csv("ips3.csv")
#df.plot()
#plt.savefig("bar_mem.jpg")
