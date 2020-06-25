import getopt
import sys
from mySock import client, close
from myUtil import login


feed_load_payload = '500#{gli&&er}{"feed_owner_id":<user_id>,"end_date":"2020-06-25T05:34:04.000Z",' \
                    '"glit_count":<number>}## '

USER_NAME = ""
PASSWORD = ""
USER_ID_LOAD = ""
NUM_LOAD = "1"

USAGE_INFO = """
Usage: feed.py -u <user_name> -p <password> 
    -n <num to load> 
    -i <user id to load>
"""


def get_params(opts):
    global USER_NAME, PASSWORD, NUM_LOAD, USER_ID_LOAD
    global feed_load_payload

    # collect data
    for opt, arg in opts:
        if opt == '-h':
            print(USAGE_INFO)
            sys.exit()
        elif opt == '-u':
            USER_NAME = arg
        elif opt == '-p':
            PASSWORD = arg
        elif opt == '-i':
            USER_ID_LOAD = arg
        elif opt == '-n':
            NUM_LOAD = arg


def format_payloads():
    global feed_load_payload
    feed_load_payload = feed_load_payload.replace("<user_id>", USER_ID_LOAD)
    feed_load_payload = feed_load_payload.replace("<number>", NUM_LOAD)


def action(sock):
    print(feed_load_payload)
    sock.send(feed_load_payload.encode())
    data = sock.recv(2048)
    print(data.decode())


def main(argv):
    # try to get main arguments
    try:
        opts, args = getopt.getopt(argv, "hu:p:i:n:")
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
