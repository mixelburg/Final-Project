import getopt
import sys
import time
from mySock import client, close
from myUtil import login

# payloads
like_payload = '710#{gli&&er}{"glit_id":<glit_id>,"user_id":<user_id>,"user_screen_name":"<screen_name>","id":-1}##'
unlike_payload = '720#{gli&&er}<unlike_id>##'

# params
NUM_LIKES = 1
GLIT_ID = ""
USER_ID = ""
USER_NAME = ""
USER_SCREEN_NAME = ""
PASSWORD = ""
UNLIKE_FLAG = False
UNLIKE_ID = ""
USAGE_INFO = """
Usage: liker.py -u <user_name> -p <password> -n <num_likes> 
    -g <glit_id> 
    -r <unlike_id> (to unlike) 
    -s <screen_name> 
    -r (auto delete 'n' likes)
"""


def get_params(opts):
    """
    parses parameters given to 'main'
    :param opts: params
    :return: None
    """
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
        elif opt == '-n':
            try:
                NUM_LIKES = int(arg)
            except:
                print("NUM_LIKES must be integer")
                sys.exit()
        elif opt == '-g':
            GLIT_ID = arg
        elif opt == '-r':
            UNLIKE_FLAG = True
            UNLIKE_ID = arg


def like(sock):
    """
    adds a like to a post
    :param sock: tcp socket
    :return: None
    """
    global unlike_payload
    global UNLIKE_ID

    # send data
    sock.send(like_payload.encode())
    data = sock.recv(2048)
    print(data.decode())


def dislike(sock):
    """
    delete like
    :param sock: tcp socket
    :return: None
    """
    global unlike_payload
    global UNLIKE_ID

    # send data
    print(unlike_payload)
    sock.send(unlike_payload.encode())
    data = sock.recv(2048)
    print(data.decode())

    # create id for next like
    NEW_UNLIKE_ID = str(int(UNLIKE_ID) - 1)
    unlike_payload = unlike_payload.replace(UNLIKE_ID, NEW_UNLIKE_ID)
    UNLIKE_ID = NEW_UNLIKE_ID


def format_payloads():
    global like_payload, unlike_payload
    like_payload = like_payload.replace("<user_id>", USER_ID)
    unlike_payload = unlike_payload.replace("<unlike_id>", UNLIKE_ID)
    like_payload = like_payload.replace("<screen_name>", USER_SCREEN_NAME)
    like_payload = like_payload.replace("<glit_id>", GLIT_ID)


def action(sock):
    # check, what to do
    if UNLIKE_FLAG:
        if UNLIKE_FLAG:
            for i in range(NUM_LIKES):
                dislike(sock)
    else:
        for i in range(NUM_LIKES):
            like(sock)


def main(argv):
    global USER_NAME, PASSWORD, USER_ID

    # try to get main arguments
    try:
        opts, args = getopt.getopt(argv, "hu:p:n:g:s:r:")
        if len(opts) == 0:
            print(USAGE_INFO)
            sys.exit()
    except getopt.GetoptError:
        print(USAGE_INFO)
        sys.exit()

    get_params(opts)

    # create socket and login
    print("[+] Started")
    sock = client()
    USER_ID = login(sock, USER_NAME, PASSWORD)

    # create payloads
    format_payloads()

    # perform main action
    action(sock)

    # close connection
    close(sock)


if __name__ == '__main__':
    main(sys.argv[1:])
