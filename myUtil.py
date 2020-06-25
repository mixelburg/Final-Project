# payloads
login_payload = '100#{gli&&er}{"user_name":"<user_name>","password":"<password>","enable_push_notifications":true}##'
auth_payload = '110#{gli&&er}2066##'
entity_payload = '310#{gli&&er}<id>##'
DELIMITER = "{gli&&er}"

USER_ID = "default"
import json

try:
    from colorama import init, Fore
except:
    print("You have to install colorama. just run: pip install colorama")
    exit()
# initialize colorama
init()
# define colors
RED = Fore.RED
GREEN = Fore.GREEN
BLUE = Fore.BLUE
RESET = Fore.RESET


def separator(data):
    j_data = data.split(DELIMITER)[1]
    j_data = j_data[:-3]
    data = json.loads(j_data)
    return data


def login(sock, username, password):
    """
    performs login operations
    :param password:
    :param username:
    :param sock: tcp socket
    :return: None
    """
    global entity_payload, login_payload
    global USER_ID

    # generate payloads
    login_payload = login_payload.replace("<user_name>", username)
    login_payload = login_payload.replace("<password>", password)

    # list of payloads
    payloads = [login_payload, auth_payload, entity_payload]

    for payload in payloads:
        # send data
        sock.send(payload.encode())
        data = sock.recv(2048).decode()

        # collect info
        if "Authentication approved" in data:
            # transform json to dictionary
            data = separator(data)

            # get user id
            USER_ID = str(data['id'])

            # generate payloads
            entity_payload = entity_payload.replace("<id>", USER_ID)
            print("[+] Login successful")

    return USER_ID




