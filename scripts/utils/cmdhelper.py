#coding=utf-8
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import time
import timehelper

def ExecCmd(cmdstr):
    print cmdstr
    p=os.popen(cmdstr)
    result = p.read()
    print result
    return result

def SSHExecCmd(host,user,pwd,cmds):
    import paramiko
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host,22,user,pwd)
    for cmd in cmds:
        print cmd
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.readlines()
        print result
    ssh.close()
    return  result

def GetFile(host,usr,pwd,smbdir,srcf,dstf):
    from smb.SMBConnection import SMBConnection
    conn = SMBConnection(usr, pwd, "", "", use_ntlm_v2=True)
    conn.connect(host,445)
    #shareslist = conn.listShares()
    with open(dstf,'wb') as fobj:
        print 'get file %s%s to %s' % (smbdir,srcf,dstf)
        conn.retrieveFile(smbdir,srcf,fobj)


def GetFiles(host,port,usr,pwd,remote_dir,local_dir):
    import paramiko
    transport = paramiko.Transport((host, port))
    transport.connect(username=usr, password=pwd)
    sftp = paramiko.SFTPClient.from_transport(transport)
    fattrs=sftp.listdir_attr(remote_dir)
    cnt = 0
    for f in fattrs:
        #print f.filename,f.st_mtime,timehelper.GetDayDiff(f.st_mtime,time.time())
        #files=sftp.listdir(remote_dir)
        #for f in files:
        if timehelper.GetDayDiff(f.st_mtime,time.time()) < 1:
            remote_f,local_f = os.path.join(remote_dir,f.filename),os.path.join(local_dir,f.filename)
            print 'download:',remote_f,'->',local_f
            sftp.get(remote_f,os.path.join(local_dir,local_f))#下载
            cnt +=1
    print 'total:',cnt,'files'
    transport.close()

def PutFiles(host,port,usr,pwd,local_dir,remote_dir):
    import paramiko
    transport = paramiko.Transport((host, port))
    transport.connect(username=usr, password=pwd)
    sftp = paramiko.SFTPClient.from_transport(transport)
    #files=sftp.listdir(local_dir)
    files=os.listdir(local_dir)
    cnt = 0
    for f in files:
        ifile = os.path.join(local_dir ,f)
        if os.path.isfile(ifile):
            print 'upload:',ifile,'->',os.path.join(remote_dir,f)
            sftp.put(os.path.join(local_dir,f),os.path.join(remote_dir,f))#上传
            os.remove(ifile)
            cnt +=1
    print 'total:',cnt,'files'
    transport.close()

if __name__ == "__main__":
    PutFiles('192.168.1.1',22,'root','test','/storage/emulated/0/Pictures/表情','/mnt/sda1/opt/img/biaoqing')
    time.sleep(10)
    GetFiles('192.168.1.1',22,'root','test','/mnt/sda1/opt/img/biaoqing/out','/storage/emulated/0/Pictures/表情/out')


