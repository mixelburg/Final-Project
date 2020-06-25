import getopt
import sys
from mySock import client, close
from myUtil import login

# payloads
comment_payload = '650#{gli&&er}{"glit_id":<glit_id>,"user_id":<user_id>,"user_screen_name":"<screen_name>","id":-1,' \
                  '"content":"<content>","date":"2020-06-23T06:29:00.751Z"}## '

# params
GLIT_ID = ""
USER_ID = ""
USER_SCREEN_NAME = "default"
USER_NAME = ""
PASSWORD = ""
COMMENT = "default"
USAGE_INFO = """
Usage: comment.py -u <user_name> -p <password> 
    -g <glit_id>  
    -s <screen_name> 
    -c <comment_text>
"""


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


def format_payloads():
    global comment_payload
    comment_payload = comment_payload.replace("<content>", COMMENT)
    comment_payload = comment_payload.replace("<user_id>", USER_ID)
    comment_payload = comment_payload.replace("glit_id>", GLIT_ID)
    comment_payload = comment_payload.replace("<screen_name>", USER_SCREEN_NAME)


def action(sock):
    # post comment
    print(comment_payload)
    sock.send(comment_payload.encode())
    data = sock.recv(2048)
    print(data.decode())


def main(argv):
    global USER_NAME, PASSWORD, USER_ID

    # try to get main arguments
    try:
        opts, args = getopt.getopt(argv, "hu:p:g:c:s:")
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

    # main action
    action(sock)

    # close connection
    close(sock)


if __name__ == '__main__':
    main(sys.argv[1:])
