import getopt
import sys
import time
from mySock import client, close
from myUtil import login

# payloads
post_payload = '550#{gli&&er}{"feed_owner_id":<owner_id>,"publisher_id":<user_id>,' \
               '"publisher_screen_name":"<screen_name>","publisher_avatar":"<avatar>","background_color":"<color>",' \
               '"date":"2020-06-25T08:02:37.836Z","content":"<text>","font_color":"<font>","id":-1}## '

# params
USER_ID = ""
USER_NAME = ""
OWNER_ID = ""
AVATAR = ""
POST_COLOR = ""
FONT_COLOR = ""
TEXT = ""
USER_SCREEN_NAME = "default"
PASSWORD = ""
USAGE_INFO = """
Usage: post.py -u <user name> -p <password> 
    -s <screen name> 
    -t <text>
    -a <avatar>
    -f <font color>
    -c <post color>
    -o <owner id>
"""


def get_params(opts):
    global USER_NAME, PASSWORD, USER_SCREEN_NAME
    global TEXT, AVATAR, POST_COLOR, FONT_COLOR, OWNER_ID

    # collect data
    for opt, arg in opts:
        if opt == '-h':
            print(USAGE_INFO)
            sys.exit()
        elif opt == '-u':
            USER_NAME = arg
        elif opt == '-p':
            PASSWORD = arg
        elif opt == '-t':
            TEXT = arg
        elif opt == '-s':
            USER_SCREEN_NAME = arg
        elif opt == '-a':
            AVATAR = arg
        elif opt == '-f':
            FONT_COLOR = arg
        elif opt == '-c':
            POST_COLOR = arg
        elif opt == '-o':
            OWNER_ID = arg


def format_payloads():
    global post_payload

    post_payload = post_payload.replace("<user_id>", USER_ID)
    post_payload = post_payload.replace("<owner_id>", OWNER_ID)
    post_payload = post_payload.replace("<screen_name>", USER_SCREEN_NAME)
    post_payload = post_payload.replace("<avatar>", AVATAR)
    post_payload = post_payload.replace("<color>", POST_COLOR)
    post_payload = post_payload.replace("<font>", FONT_COLOR)
    post_payload = post_payload.replace("<text>", TEXT)
    post_payload = post_payload.replace("<owner_id>", OWNER_ID)


def action(sock):
    # post comment
    print(post_payload)
    sock.send(post_payload.encode())
    data = sock.recv(2048)
    print("\n\n")
    print(data.decode())


def main(argv):
    global USER_NAME, PASSWORD, USER_SCREEN_NAME, USER_ID
    global post_payload

    # try to get main arguments
    try:
        opts, args = getopt.getopt(argv, "hu:p:s:t:a:f:c:o:")
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

    # create payloads
    format_payloads()

    # main action
    action(sock)

    # close connection
    close(sock)


if __name__ == '__main__':
    main(sys.argv[1:])
