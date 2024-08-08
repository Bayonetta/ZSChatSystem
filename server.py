import socket
import select
import ssl
import binascii

def broadcast_data(sock, message):
    for client_socket in CONNECTION_LIST:
        if client_socket != server_socket and client_socket != sock:
            try:
                client_socket.send(message.encode())
            except:
                client_socket.close()
                CONNECTION_LIST.remove(client_socket)

def saveMessage(message):
     file = open('history', 'a')
     file.write(message)
     file.close()

if __name__ == "__main__":
    CONNECTION_LIST = []
    RECV_BUFFER = 4096
    PORT = 9999

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

    server_socket = context.wrap_socket(server_socket, server_side=True)

    CONNECTION_LIST.append(server_socket)
    print(f"Chat server started on port {PORT}")

    while True:
        read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST, [], [])

        for sock in read_sockets:
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print(f"Client ({addr}) connected")
                broadcast_data(sockfd, f"[{addr}] entered our chatting room\n")
            else:
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        message = f"\r<{str(sock.getpeername())}> {data.decode()}"
                        broadcast_data(sock, message)
                        saveMessage(message)
                except:
                    addr = sock.getpeername()
                    broadcast_data(sock, f"Client ({addr}) is offline\n")
                    print(f"Client ({addr}) is offline")
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue