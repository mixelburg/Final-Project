import getopt
import sys

from mySock import client, close
import time

# payloads
login_payload = '100#{gli&&er}{"user_name":"<user_name>","password":"<password>","enable_push_notifications":true}##'
auth_payload = '110#{gli&&er}2066##'
entity_payload = '310#{gli&&er}<id>##'
like_payload = '710#{gli&&er}{"glit_id":<glit_id>,"user_id":<user_id>,"user_screen_name":"<screen_name>","id":-1}##'
unlike_payload = '720#{gli&&er}<unlike_id>##'

# params
NUM_LIKES = 1
GLIT_ID = 0
USER_ID = 0
USER_NAME = ""
USER_SCREEN_NAME = ""
PASSWORD = ""
UNLIKE_FLAG = False
UNLIKE_ID = ""
USAGE_INFO = "Usage: liker.py -u <user_name> -p <password> -n <num_likes> -g <glit_id> -r <unlike_id> (to unlike) "

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
            like_payload = like_payload.replace("<user_id>", USER_ID)

    print("[+] Login successful")


def get_params(opts):
    global like_payload, unlike_payload
    global UNLIKE_FLAG, UNLIKE_ID
    global USER_NAME, PASSWORD, USER_SCREEN_NAME, NUM_LIKES, GLIT_ID

    # collect data
    for opt, arg in opts:
        if opt == '-h':
            print(USAGE_INFO)
            sys.exit()
        elif opt == '-u':
            USER_NAME = arg
        elif opt == '-p':
            PASSWORD = arg
        elif opt == '-s':
            USER_SCREEN_NAME = arg
            like_payload = like_payload.replace("<screen_name>", USER_SCREEN_NAME)
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


def main(argv):
    global USER_NAME, PASSWORD, NUM_LIKES, USER_ID, GLIT_ID, USER_SCREEN_NAME
    global login_payload, like_payload, unlike_payload
    global UNLIKE_FLAG, UNLIKE_ID

    # try to get main arguments
    try:
        opts, args = getopt.getopt(argv, "hu:p:n:g:r:s:")
    except getopt.GetoptError:
        print(USAGE_INFO)
        sys.exit()

    get_params(opts)

    # generate payloads
    login_payload = login_payload.replace("<user_name>", USER_NAME)
    login_payload = login_payload.replace("<password>", PASSWORD)

    # create socket and login
    print("[+] Started")
    sock = client()
    login(sock)

    # like or unlike
    for i in range(NUM_LIKES):
        if UNLIKE_FLAG:
            dislike(sock)
        else:
            like(sock)

    close(sock)


def like(sock):
    # send data
    sock.send(like_payload.encode())
    data = sock.recv(2048)
    print(data.decode())


def dislike(sock):
    global unlike_payload
    global UNLIKE_ID

    # send data
    sock.send(unlike_payload.encode())
    data = sock.recv(2048)
    print(data.decode())

    # create id for next like
    NEW_UNLIKE_ID = str(int(UNLIKE_ID) + 1)
    unlike_payload = unlike_payload.replace(UNLIKE_ID, NEW_UNLIKE_ID)
    UNLIKE_ID = NEW_UNLIKE_ID


if __name__ == '__main__':
    main(sys.argv[1:])
