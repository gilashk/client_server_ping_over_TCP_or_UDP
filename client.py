import socket
import time
import sys
import getopt
import random
import string

IP = ""
UDP_PORT = 5555
TCP_PORT = 6666
BUFFER_SIZE = 1024

PROTOCOL = "UDP"
DEADLINE = 4  # deadline - waiting for answer
COUNT = 4  # counting packet to send
PACKET_SIZE = 10


"""
The function handel input arguments
"""


def input_handler(argv):
    global IP
    global PROTOCOL
    global DEADLINE  # deadline_legal_input --> int
    global COUNT     # count_legal_input --> int
    global PACKET_SIZE
    ping_usage = "Usage: %s IP [-p protocol] [-w deadline] [-c count] [-s packetsize]" % (argv[0])
    unknown_command = "%s: unknown command \n" % (argv[0])
    legal_input = "The input argument is not legal"
    protocol_legal_input = ["TCP", "UDP", "tcp", "udp"]

    try:
        IP = argv[1]
        socket.inet_aton(IP)
    except Exception as e:
        print "Bad IP addres: %s " % str(e)
        print ping_usage
        sys.exit(2)

    try:
        opts, args = getopt.getopt(argv[2:], "hp:w:c:s:", ["help", "protocol=", "deadline=", "count=", "packetsize="])
    except getopt.GetoptError:
        print unknown_command
        print ping_usage
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            print ping_usage
            sys.exit(0)
        elif opt in ("-p", "--protocol"):
            if arg in protocol_legal_input:
                PROTOCOL = arg.upper()
            else:
                print unknown_command, legal_input
                sys.exit(2)
        elif opt in ("-w", "--deadline"):
            try:
                DEADLINE = int(arg)
            except Exception as e:
                print unknown_command, legal_input, str(e)
                sys.exit(2)
        elif opt in ("-c", "--count"):
            try:
                COUNT = int(arg)
            except Exception as e:
                print unknown_command, legal_input, str(e)
                sys.exit(2)
        elif opt in ("-s", "--packetsize"):
            try:
                PACKET_SIZE = int(arg)
                if PACKET_SIZE < 1 or PACKET_SIZE > 1500:
                    raise ValueError('PACKET_SIZE not legal')
            except Exception as e:
                print unknown_command, legal_input, str(e)
                sys.exit(2)
    if opts:
        print "PROTOCOL: %s, DEADLINE: %s, COUNT: %s, PACKET_SIZE: %s" % (PROTOCOL, DEADLINE, COUNT, PACKET_SIZE)


"""
The function generat random string
"""


def str_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return''.join(random.choice(chars) for _ in range(size))


"""
The function handel udp client
"""


def udp_client():
    global PACKET_SIZE
    success = 0
    failure = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for pings in range(COUNT):
        random_message = str_generator(PACKET_SIZE)
        sock.settimeout(DEADLINE)
        start = time.time()*1000
        sock.sendto(random_message, (IP, UDP_PORT))

        try:
            data, addr = sock.recvfrom(BUFFER_SIZE)
            end = time.time()*1000
            diff = end - start
            if not data == random_message:
                raise ValueError('data response not correct')
            print "from %s req=%s time=%s ms" % (IP, pings+1, round(diff, 3))
            success += 1
            time.sleep(1)
        except socket.timeout:
            print 'REQUEST TIMED OUT'
            failure += 1

    return success, failure


"""
The function handel tcp client
"""


def tcp_client():
    global PACKET_SIZE
    success = 0
    failure = 0
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((IP, TCP_PORT))
        for pings in range(COUNT):
            random_message = str_generator(PACKET_SIZE)
            start = time.time()*1000
            sock.send(random_message)
            try:
                data = sock.recv(BUFFER_SIZE)
                end = time.time()*1000
                diff = end - start
                if not data == random_message:
                    raise ValueError('data response not correct')
                print "from %s req=%s time=%s ms" % (IP, pings+1, round(diff, 3))
                success += 1
                time.sleep(1)
            except socket.timeout:
                print 'REQUEST TIMED OUT'
                failure += 1
        sock.close()
    except Exception as e:
        print "No TCP server in listen, %s " % str(e)

    return success, failure

"""
main function
"""


def main():
    success = 0
    failure = 0
    input_handler(sys.argv)
    if PROTOCOL == "UDP":
        success, failure = udp_client()
    elif PROTOCOL == "TCP":
        success, failure = tcp_client()

    print "--- %s ping statistics ---" % IP
    print "%s packets transmitted, %s received, %%%s packet loss" % (
        success+failure, success, 100*failure/(success+failure))

if __name__ == "__main__":
    main()
