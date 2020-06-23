import getopt
import sys

from mySock import client, close
import time

# payloads
login_payload = '100#{gli&&er}{"user_name":"<user_name>","password":"<password>","enable_push_notifications":true}##'
auth_payload = '110#{gli&&er}2066##'
entity_payload = '310#{gli&&er}<id>##'
comment_payload = '650#{gli&&er}{"glit_id":<glit_id>,"user_id":<user_id>,"user_screen_name":"<screen_name>","id":-1,' \
                  '"content":"<content>","date":"2020-06-23T06:29:00.751Z"}## '

# params
GLIT_ID = 0
USER_ID = 0
USER_NAME = ""
USER_SCREEN_NAME = "default"
PASSWORD = ""
COMMENT = "default"
USAGE_INFO = "Usage: comment.py -u <user_name> -p <password> -g <glit_id> -c <comment> -s <screen_name>"


def login(sock):
    """
    performs login operations
    :param sock: tcp socket
    :return: None
    """
    global USER_ID
    global USER_SCREEN_NAME
    global entity_payload
    global like_payload
    global comment_payload

    # list of payloads
    payloads = [login_payload, auth_payload, entity_payload]

    for payload in payloads:
        # send data
        sock.send(payload.encode())
        data = sock.recv(2048).decode()

        # collect info
        if "Authentication approved" in data:
            data = data.split(",")

            # get user id
            user_id_info = data[4]
            USER_ID = user_id_info.split(":")[1]

            # generate payloads
            entity_payload = entity_payload.replace("<id>", USER_ID)
            comment_payload = comment_payload.replace("<user_id>", USER_ID)
            comment_payload = comment_payload.replace("<screen_name>", USER_SCREEN_NAME)

    print("[+] Login successful")


def get_params(opts):
    global comment_payload
    global USER_NAME, PASSWORD, GLIT_ID, COMMENT, USER_SCREEN_NAME

    # collect data
    for opt, arg in opts:
        if opt == '-h':
            print(USAGE_INFO)
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


def main(argv):
    global USER_NAME, PASSWORD, GLIT_ID, USER_SCREEN_NAME
    global login_payload, comment_payload
    global COMMENT

    # try to get main arguments
    try:
        opts, args = getopt.getopt(argv, "hu:p:g:c:s:")
    except getopt.GetoptError:
        print(USAGE_INFO)
        sys.exit()

    get_params(opts)

    # generate payloads
    login_payload = login_payload.replace("<user_name>", USER_NAME)
    login_payload = login_payload.replace("<password>", PASSWORD)
    comment_payload = comment_payload.replace("<content>", COMMENT)

    # create socket and login
    print("[+] Started")
    sock = client()
    login(sock)

    # post comment
    print(comment_payload)
    sock.send(comment_payload.encode())
    data = sock.recv(2048)
    print(data.decode())

    close(sock)


if __name__ == '__main__':
    main(sys.argv[1:])
