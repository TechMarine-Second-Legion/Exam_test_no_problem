import socket
import BD_voice as general
import conf_server

def listen_to_first(d):
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    #PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
    PORT = conf_server.for_search.server_port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                general.message_center(d, data.decode())
                conn.sendall(b'Done')
