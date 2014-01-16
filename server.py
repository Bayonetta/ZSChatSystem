import ssl
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 8080))
s.listen(5)
print 'Listen on port: 8080'

while True:
        client, addr = s.accept()
        print 'Connection from', addr
        client_ssl = ssl.wrap_socket(client, server_side=True, certfile='cert.pem')
        client_ssl.write('sdfsdf')
        client_ssl.close()
        client.close()
