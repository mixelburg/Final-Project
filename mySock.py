import socket

# sending data
SERVER_IP = "44.224.228.136"
SERVER_PORT = 1336


def help():
    print("""This library was created by Ivan (mixelburg).
     It allows you to easily create server socket and client socket""")


def client():
    """
    Creates a client side socket for you
    :return: sock
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[+] Socket successfully created")
    except socket.error as err:
        print("[!] socket creation failed with error %s" % (err))

    server_address = (SERVER_IP, SERVER_PORT)
    sock.connect(server_address)
    print("[+] Successfully connected\n")

    return sock


def close(sock):
    sock.close()
    print("\n [+] Socket closed successfully")

