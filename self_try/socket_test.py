"""
@Time : 2024/1/14 16:25
@Author : rainmon
@File : socket_test.py
@Project : StudyNotes-Python
@feature : 
@description：
"""
import datetime

import socket

HOST = '0.0.0.0'
PORT = 3434


def socket_tcp_server():
    # AF_INET说明使用IPV4地址，SOCK_STREAM指明TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定IP、端口
    s.bind((HOST, PORT))
    # 监听
    s.listen(1)
    while True:
        # 接受TCP连接，返回新的Socket对象
        conn, addr = s.accept()
        print('Client {} connected!'.format(addr))
        dt = datetime.datetime.now()
        message = "Current time is {}".format(dt)
        conn.send(message.encode())
        print(f"Sent: {message}")
        conn.close()


if __name__ == '__main__':
    socket_tcp_server()