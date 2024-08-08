import socket
import sys
import ssl
import threading

def prompt():
    sys.stdout.write('<You> ')
    sys.stdout.flush()

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                print('\nDisconnected from chat server')
                sys.exit()
            else:
                sys.stdout.write(data.decode())
                prompt()
        except Exception as e:
            print(f'\nError receiving data: {e}')
            sys.exit()

def send_messages(sock):
    while True:
        msg = sys.stdin.readline()
        sock.send(msg.encode())
        prompt()

if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 9999

    # 创建一个 TCP/IP 套接字
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 创建一个默认的 SSL 上下文
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    context.load_verify_locations("cert.pem")
    
    # 使用 SSL 包装套接字
    s = context.wrap_socket(s, server_hostname=HOST)
    
    s.settimeout(120)
    try:
        s.connect((HOST, PORT))
    except Exception as e:
        print(f'Unable to connect: {e}')
        sys.exit()

    print('Connected to remote host. Start sending messages')
    prompt()

    # 创建线程来处理接收和发送消息
    receive_thread = threading.Thread(target=receive_messages, args=(s,))
    send_thread = threading.Thread(target=send_messages, args=(s,))
    
    receive_thread.start()
    send_thread.start()

    receive_thread.join()
    send_thread.join()