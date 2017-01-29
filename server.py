import random
import socket
import threading
import time

IP = "127.0.0.1"
UDP_PORT = 5555
TCP_PORT = 6666
BUFFER_SIZE = 1024
SERVER_FAIL = True
PERCENTAGE_OF_FAILURES = 0  # The percentage of server is fail to send response (0 = no fail, 100 = fail all the time)

"""
return True if Fail     (NO ping should be response to the client)
return False if no Fail (ping should be response to the client)
"""


def server_failer(percentage_of_failures):
    rand = random.randint(0, 100)
    if rand < percentage_of_failures:
        return True
    else:
        return False


"""
ping udp server, udp bind
"""


def udp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((IP, UDP_PORT))
    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        print "%s New UDP connection from: %s" % (time.asctime(time.localtime()), addr)
        if SERVER_FAIL:
            if server_failer(PERCENTAGE_OF_FAILURES):
                continue
        sock.sendto(data, addr)


"""
ping tcp server, tcp bind, and open thread of new connection
"""


def tcp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((IP, TCP_PORT))
    sock.listen(1)
    while True:
        conn, addr = sock.accept()
        print "%s New TCP connection from: %s" % (time.asctime(time.localtime()), addr)
        t = threading.Thread(target=tcp_handler, name="tcp", args=conn)
        t.daemon = True
        t.start()

"""
tcp handler
"""


def tcp_handler(conn):
    while True:
        data = conn.recv(BUFFER_SIZE)
        if not data:
            break
        if SERVER_FAIL:
            if server_failer(PERCENTAGE_OF_FAILURES):
                continue
        conn.send(data)
    conn.close()


"""
main function of ping server. open 2 deamon threads (tcp, udp) and finish only with kill
"""


def main():
    s_tcp = threading.Thread(target=tcp_server, name="tcp_server")
    s_udp = threading.Thread(target=udp_server, name="udp_server")
    s_tcp.daemon = True
    s_udp.daemon = True
    s_tcp.start()
    s_udp.start()

    while True:
        pass


if __name__ == "__main__":
    main()
