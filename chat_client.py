"""
chat room
socket  fork练习
"""

from socket import *
import os,sys

ADDR = ('0.0.0.0',8990) #服务器地址

def main():
    sockfd = socket(AF_INET,SOCK_DGRAM)
    name = login(sockfd)
    chat(sockfd,name)

# 请求加入聊天室
def login(sockfd):
    while True:
        name = input("name:")
        msg = 'L ' + name
        sockfd.sendto(msg.encode(), ADDR)
        date, addr = sockfd.recvfrom(4096)
        if date == b'OK':
            print('you are now in the chatroom...')
            break
        else:
            print(date.decode())
    return name

# 发起聊天
def chat(sockfd,name):
    pid = os.fork()
    if pid < 0:
        return
    elif pid == 0:
        send(name, sockfd)
    else:
        recv(sockfd)

# 接受消息
def recv(sockfd):
    while True:
        try:
            date, addr = sockfd.recvfrom(4096)
        except KeyboardInterrupt:
            date = b'EXIT'
        # 服务端发送EXIT让客户端退出
        if date.decode() == 'EXIT':
            sys.exit()
        print('\n'+date.decode() +'\nwrite your words:',end = '')

# 发送消息
def send(name, sockfd):
    while True:
        try:
            date = input("write your words:")
        except KeyboardInterrupt:
            date = 'quit'
        if date == 'quit':
            msg = 'Q %s' % name
            sockfd.sendto(msg.encode(), ADDR)
            sys.exit('quit chatroom.')
        msg = 'C %s %s' % (name, date)
        sockfd.sendto(msg.encode(), ADDR)

if __name__ == '__main__':
    main()