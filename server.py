import socket
import select
import ssl
from binascii import b2a_hex, a2b_hex
from Crypto.Cipher import DES


def broadcast_data (sock,message):
    for socket in conn_list:
        if socket != server_socket and socket != sock :
            try :
                socket.write(message)
            except :
                socket.close()
                conn_list.remove(socket)


def saveMessage(message):
     message = message + (8 - len(message) % 8) * ' '
     cryp = obj.encrypt(message)
     pass_hex = b2a_hex(cryp)

     file = open('history', 'a')
     file.write(pass_hex)
     file.close()


if __name__ == "__main__":
    conn_list = []
    recv_buffer = 1024
    PORT = 9999
    key = '12345678'
    obj = DES.new(key)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', PORT))
    server_socket.listen(2)

    conn_list.append(server_socket)

    print "Chat server started on port " + str(PORT)

    while 1:
        read_sockets,write_sockets,error_sockets = select.select(conn_list,[],[])
        for sock in read_sockets:
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                sock_ssl = ssl.wrap_socket(sockfd, server_side=True, certfile='cert.pem')
                conn_list.append(sock_ssl)
                print "Client (%s, %s) connected" % addr
                broadcast_data(sock_ssl, "[%s:%s] entered room\n" % addr)
            else:
                try:
                    data = sock.read(recv_buffer)
                    if data:
                        message = '\n<' + str(sock.getpeername()) + '> ' + data
                        broadcast_data(sock, message)
                        saveMessage(message)
                except:
                    broadcast_data(sock, "Client (%s, %s) is offline" % addr)
                    print "Client (%s, %s) is offline" % addr
                    sock.close()
                    conn_list.remove(sock)
                    continue

    server_socket.close()
