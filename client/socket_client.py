import socket
import conf_client

def send_qw(qw, qw_type = 'req', HOST = '127.0.0.1'):
    #HOST = '127.0.0.1'  # The server's hostname or IP address
    #PORT = 65432    # The port used by the server
    PORT = conf_client.for_while.server_port

    #Первые 3 символа сообщения - тип. req - запрос, inf - информирование, cmd - команда
    if len(qw)>0:
        qw = qw_type+qw

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(bytes(qw, encoding='utf-8'))
        data = s.recv(1024)
