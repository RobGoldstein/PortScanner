import socket
import threading
from queue import Queue

target = "127.0.0.1"   #Target ip address "127.0.0.1" is localhost
queue = Queue()
open_ports = []

def port_scan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #Says we are using TCP not UDP
        sock.connect((target, port))
        return True       #if the port is open True is returned
    except:
        return False     #port is closed and False is returned

#fills queue in FIFO format
def fill_queue(port_list):
    for port in port_list:
        queue.put(port)

#only prints when True to save compute cost
def worker():
    while not queue.empty():
        port = queue.get()
        if port_scan(port):
            print("Port {} is open!".format(port))
            open_ports.append(port)


port_list = range(1, 1024)
fill_queue(port_list)

thread_list = []
#number of threads you want
for t in range(100):
    thread = threading.Thread(target=worker)
    thread_list.append(thread)


for thread in thread_list:
    thread.start()
#waits for thread to finish before moving on
for thread in thread_list:
    thread.join()

print("Open ports are: ", open_ports)



#slow non threaded option
# for port in range(1, 1024):
#     result = port_scan(port)
#     if result:
#         print("Port {} is open!".format(port))
#     else:
#         print("Port {} is closed!".format(port))