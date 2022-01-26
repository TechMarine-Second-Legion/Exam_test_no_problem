import BD_voice as general
import socket_server as socs
import time, os

def main():
    os.system('cvlc ./voice/base/server_is_ready.wav --play-and-exit')
    d = general.load_answ_base({})

    while 1:
        socs.listen_to_first(d)
        time.sleep(0.2)

try:
    main()
except:
    os.system('cvlc ./voice/base/des.wav --play-and-exit')
