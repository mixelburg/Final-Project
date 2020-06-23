import getopt
import sys

from mySock import client, close
import time

login_payload = '100#{gli&&er}{"user_name":"<user_name>","password":"<password>","enable_push_notifications":true}##'
auth_payload = '110#{gli&&er}2066##'
entity_payload = '310#{gli&&er}<id>##'
comment_payload = '650#{gli&&er}{"glit_id":<glit_id>,"user_id":<user_id>,"user_screen_name":"<screen_name>","id":-1,"content":"<content>","date":"2020-06-23T06:29:00.751Z"}##'


GLIT_ID = 0
USER_ID = 0
USER_NAME = ""
USER_SCREEN_NAME = "default"
PASSWORD = ""
COMMENT = "default"


def login(sock):
    global USER_ID
    global USER_SCREEN_NAME
    global entity_payload
    global like_payload
    global comment_payload

    payloads = [login_payload, auth_payload, entity_payload]

    for payload in payloads:
        sock.send(payload.encode())
        data = sock.recv(2048).decode()

        if "Authentication approved" in data:
            data = data.split(",")

            user_id_info = data[4]
            USER_ID = user_id_info.split(":")[1]

            entity_payload = entity_payload.replace("<id>", USER_ID)
            comment_payload = comment_payload.replace("<user_id>", USER_ID)
            comment_payload = comment_payload.replace("<screen_name>", USER_SCREEN_NAME)


    print("[+] Login successful")


def main(argv):
    global USER_NAME
    global PASSWORD
    global GLIT_ID
    global login_payload
    global COMMENT
    global comment_payload
    global USER_SCREEN_NAME

    try:
        opts, args = getopt.getopt(argv, "hu:p:g:c:s:")
    except getopt.GetoptError:
        print("Usage: ping.py -u <user_name> -p <password> -g <glit_id> -c <comment>")
        sys.exit()

    for opt, arg in opts:
        if opt == '-h':
            print("Usage: ping.py -u <user_name> -p <password> -n <num_likes> -g <glit_id>")
            sys.exit()
        elif opt == '-u':
            USER_NAME = arg
        elif opt == '-p':
            PASSWORD = arg
        elif opt == '-g':
            GLIT_ID = arg
            comment_payload = comment_payload.replace("<glit_id>", GLIT_ID)
        elif opt == '-c':
            COMMENT = arg
        elif opt == '-s':
            USER_SCREEN_NAME = arg
            comment_payload = comment_payload.replace("<screen_name>", USER_SCREEN_NAME)

    login_payload = login_payload.replace("<user_name>", USER_NAME)
    login_payload = login_payload.replace("<password>", PASSWORD)
    comment_payload = comment_payload.replace("<content>", COMMENT)

    print("[+] Started")
    sock = client()

    login(sock)

    print(comment_payload)
    sock.send(comment_payload.encode())
    data = sock.recv(2048)
    print(data.decode())

    close(sock)


if __name__ == '__main__':
    main(sys.argv[1:])
