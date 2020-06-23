import getopt
import sys

from mySock import client, close
import time

login_payload = '100#{gli&&er}{"user_name":"<user_name>","password":"<password>","enable_push_notifications":true}##'
auth_payload = '110#{gli&&er}2066##'
entity_payload = '310#{gli&&er}<id>##'
like_payload = '710#{gli&&er}{"glit_id":<glit_id>,"user_id":<user_id>,"user_screen_name":"<screen_name>","id":-1}##'
unlike_payload = '720#{gli&&er}<unlike_id>##'

NUM_LIKES = 1
GLIT_ID = 0
USER_ID = 0
USER_NAME = ""
USER_SCREEN_NAME = ""
PASSWORD = ""
UNLIKE_FLAG = False
UNLIKE_ID = ""


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
    global UNLIKE_FLAG
    global UNLIKE_ID
    global unlike_payload

    try:
        opts, args = getopt.getopt(argv, "hu:p:n:g:r:")
    except getopt.GetoptError:
        print("Usage: ping.py -u <user_name> -p <password> -n <num_likes> -g <glit_id> -r <unlike_id> (to unlike) ")
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
            like_payload = like_payload.replace("<glit_id>", GLIT_ID)
        elif opt == '-r':
            UNLIKE_FLAG = True
            UNLIKE_ID = arg
            unlike_payload = unlike_payload.replace("<unlike_id>", UNLIKE_ID)

    login_payload = login_payload.replace("<user_name>", USER_NAME)
    login_payload = login_payload.replace("<password>", PASSWORD)

    print("[+] Started")
    sock = client()

    login(sock)

    if not UNLIKE_FLAG:
        for i in range(NUM_LIKES):
            sock.send(like_payload.encode())
            data = sock.recv(2048)
            print(data.decode())
    else:
        for i in range(NUM_LIKES):
            sock.send(unlike_payload.encode())
            data = sock.recv(2048)
            print(data.decode())

            NEW_UNLIKE_ID = str(int(UNLIKE_ID) + 1)
            unlike_payload = unlike_payload.replace(UNLIKE_ID, NEW_UNLIKE_ID)
            UNLIKE_ID = NEW_UNLIKE_ID

    close(sock)


if __name__ == '__main__':
    main(sys.argv[1:])
