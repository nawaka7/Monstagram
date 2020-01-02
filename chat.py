# chat.py
import socket


def chat(database, sign_result):
    #print(database)
    #print(sign_result)

    looper = True
    while looper:
        print('''
    ====================
      CHAT SELCECTION
    ====================
    1. Open Chatroom
    2. Search Chatroom
    3. Exit
            ''')
        chat_choice = input("Choose the menu: ")
        if chat_choice == '1':
            main_server(database, sign_result)
            # main_server()


        elif chat_choice == '2':
            main_client(database, sign_result)

        elif chat_choice == "3":
            looper = False
            print('Bye')
        else:
            print("wrong choice")
    pass




def main_server(database, sign_result, host = "192.168.0.205", port = 25):
    # host = socket.gethostbyname(socket.gethostname())
    port = port
    #print(database)
    #print(sign_result)
    server_name = input("what's the chatroom title? ")
    mySocket = socket.socket()
    mySocket.bind((host,port))
    myname = sign_result[0]['name']['first']
    print("Matching the person...")
    try:
        mySocket.settimeout(600)
        database.chats.insert_one({"server_id":sign_result[0]['id'], "server_name": server_name, "server_ip": host, "server_port": port})
        mySocket.listen(1)
        connection, address = mySocket.accept()
        print("Connection from: ", address)


        while True:
            data = connection.recv(1024).decode()
            if not data:
                break
            print("Received from " + str(data))
            #data = str(data).upper()
            m_input = input(" -> ")

            if m_input == 'q':
                break

            message = myname + ': ' + m_input

            #print("sending: " + m_input)
            connection.send(message.encode())
        connection.close()
    except:
        print("timeout")

# def main_server():
#     # host = 'DESKTOP-8P2BS56'
#     # host = socket.gethostbyname(socket.getfqdn())
#     # host = '127.0.0.1'
#     # host = '147.47.164.186'
#     host = ''
#     # print('host', socket.gethostbyname(socket.getfqdn()))
#     port = 25
#     print('port', port)
#
#     mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     mySocket.bind((host,port))
#
#     print("listening...")
#     mySocket.listen(1)
#     connection, address = mySocket.accept()
#     print("Connection from: ", address)
#
#     while True:
#         data = connection.recv(1024).decode()
#
#         if not data:
#             break
#         print("from connected  user: " + str(data))
#
#         message = input("-> ")
#         print("sending: " + str(message))
#         connection.send(message.encode())
#
#     connection.close()

def main_client(database, sign_result):
    #host = '192.168.56.1'
    #port = 7240
    host = '127.0.0.1'  #IPv4
    port = 4321
    mySocket = socket.socket()
    mySocket.connect((host, port))

    message = input(" -> ")

    while True:
        mySocket.send(message.encode())
        data = mySocket.recv(1024).decode()
        print('Received from ' + data)

        message = sign_result[0]['name']['first'] + ": " +input(" -> ")
        if message[len(sign_result[0]['name']['first'])+2] == '/q':
            break
    mySocket.close()
