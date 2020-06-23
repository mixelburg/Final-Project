import getopt
import sys

from mySock import client, close
import time

login_payload = '100#{gli&&er}{"user_name":"<user_name>","password":"<password>","enable_push_notifications":true}##'
auth_payload = '110#{gli&&er}2066##'
entity_payload = '310#{gli&&er}<id>##'
like_payload = '710#{gli&&er}{"glit_id":<glit_id>,"user_id":<user_id>,"user_screen_name":"<screen_name>","id":-1}##'

NUM_LIKES = 1
GLIT_ID = 0
USER_ID = 0
USER_NAME = ""
USER_SCREEN_NAME = ""
PASSWORD = ""


def login(sock):
    global USER_ID
    global USER_SCREEN_NAME
    global entity_payload
    global like_payload

    payloads = [login_payload, auth_payload, entity_payload]

    for payload in payloads:
        sock.send(payload.encode())
        data = sock.recv(2048).decode()

        if "Authentication approved" in data:
            data = data.split(",")
            USER_SCREEN_NAME = data[0]
            USER_SCREEN_NAME = USER_SCREEN_NAME.split(":")[1]
            USER_SCREEN_NAME = USER_SCREEN_NAME[1:-1]

            user_id_info = data[4]
            USER_ID = user_id_info.split(":")[1]

            entity_payload = entity_payload.replace("<id>", USER_ID)
            like_payload = like_payload.replace("<user_id>", USER_ID)
            like_payload = like_payload.replace("<screen_name>", USER_SCREEN_NAME)

    print("[+] Login successful")

def main(argv):
    global USER_NAME
    global PASSWORD
    global NUM_LIKES
    global GLIT_ID
    global login_payload
    global like_payload

    try:
        opts, args = getopt.getopt(argv, "hu:p:n:g:")
    except getopt.GetoptError:
        print("Usage: ping.py -u <user_name> -p <password> -n <num_likes> -g <glit_id>")
        sys.exit()

    for opt, arg in opts:
        if opt == '-h':
            print("Usage: ping.py -u <user_name> -p <password> -n <num_likes> -g <glit_id>")
            sys.exit()
        elif opt == '-u':
            USER_NAME = arg
        elif opt == '-p':
            PASSWORD = arg
        elif opt == '-n':
            try:
                NUM_LIKES = int(arg)
            except:
                print("NUM_LIKES must be integer")
                sys.exit()
        elif opt == '-g':
            GLIT_ID = arg

    login_payload = login_payload.replace("<user_name>", USER_NAME)
    login_payload = login_payload.replace("<password>", PASSWORD)
    like_payload = like_payload.replace("<glit_id>", GLIT_ID)

    print("[+] Started")
    sock = client()

    login(sock)

    for i in range(NUM_LIKES):
        sock.send(like_payload.encode())
        data = sock.recv(2048)
        print("[+] Like added")

    close(sock)


if __name__ == '__main__':
    main(sys.argv[1:])
