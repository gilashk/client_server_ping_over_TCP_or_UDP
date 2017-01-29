client server script over TCP or UDP for "ping" in Python
---------------------------------------------------------

The scripts simulate ping request protocol, but it implement over TCP and UDP (without using icmp protocol).

The script writen in python 2.7


The client:
1. The client can send TCP or UDP request

2. The client can get input argument, and config his parameters. (protocol, deadline - waiting for answer, count - number packet to send, packet size)

Example - running the script:
::
$ python client.py 127.0.0.1

Example - answer:
::
from 127.0.0.1 req=1 time=1.026 ms
from 127.0.0.1 req=2 time=1.071 ms
from 127.0.0.1 req=3 time=1.179 ms
from 127.0.0.1 req=4 time=0.835 ms
--- 127.0.0.1 ping statistics ---
4 packets transmitted, 4 received, %0 packet loss

Example - running the script with arguments:
::
python client.py 127.0.0.1 -p tcp -w 2 -c 10 -s 100


The server:

1. The server bind on both, TCP and UDP, and with for client request.


2. It possible to simulate "server failed", by edit the variable PERCENTAGE_OF_FAILURES (The percentage of server is fail to send response (0 = no fail, 100 = fail all the time), while the default configuration is 0, no fail.


Example - running the script:
::
$ python server.py


