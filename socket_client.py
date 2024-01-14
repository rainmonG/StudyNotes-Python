"""
@Time : 2024/1/14 16:33
@Author : rainmon
@File : socket_client.py
@Project : StudyNotes-Python
@feature : 
@description：
"""
import socket

HOST = '127.0.0.1'
PORT = 3434


def socket_client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    print(f"Connect {HOST}: {PORT} OK")
    data = s.recv(1024)     # 接收数据最大长度1024
    print(f"Received: {data.decode()}")
    s.close()


if __name__ == '__main__':
    socket_client()
