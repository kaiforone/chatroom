"""
chat room
socket  fork练习
"""

from socket import *
import os,sys

ADDR = ('0.0.0.0',8990) #服务器地址
dict_member = {} # 聊天室成员{名字：地址}

# 创建网络链接
def main():
    sockfd = socket(AF_INET,SOCK_DGRAM)
    sockfd.bind(ADDR)
    pid = os.fork()
    if pid < 0:
        return
    elif pid == 0:
        while True:
            msg = input("manager's news : ")
            msg = 'C manager %s '%msg
            sockfd.sendto(msg.encode(),ADDR)
    else:
        do_request(sockfd)  #处理客户端请求

# 接受客户端请求
def do_request(sockfd):
    while True:
        date,addr = sockfd.recvfrom(4096)
        list_date = date.decode().split(' ')
        if list_date[0] == 'L':
            do_login(addr, list_date[1], sockfd)
        elif list_date[0] == 'C':
            date = ' '.join(list_date[2:])
            do_chat(list_date[1],date,sockfd)
        elif list_date[0] == 'Q':
            if list_date[1] not in dict_member:
                sockfd.sendto(b'EXIT', addr)
                continue
            do_logout(list_date[1],sockfd,addr)


# 处理用户加入聊天
def do_login(addr, name, sockfd):
    if name in dict_member or 'manager' in name:
        sockfd.sendto(b'the name is exist ,please try again.', addr)
        return
    sockfd.sendto(b'OK', addr)
    # 通知其他人
    msg = '%s join our chatroom...' % name
    for v in dict_member.values():
        sockfd.sendto(msg.encode(), v)
    # 用户加入
    dict_member[name] = addr

# 处理聊天
def do_chat(name,date,sockfd):
    msg = '%s : %s ' % (name,date)
    for key in dict_member:
        if key != name:
            sockfd.sendto(msg.encode(), dict_member[key])

# 处理用户退出
def do_logout(name,sockfd,addr):
    sockfd.sendto(b'EXIT',addr)
    del dict_member[name]
    for key in dict_member:
        msg = '%s quit chatroom '%name
        sockfd.sendto(msg.encode(),dict_member[key])

if __name__ == '__main__':
    main()

# sockfd.close()