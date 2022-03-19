import ast
import threading
import socket
from time import sleep

def requestResponse(message):
    if message['option'] == '1':
        allRoomResponse(message)
    elif message['option'] == '2':
        roomCreateResponse(message)
    else:
        joinRoomResponse(message)

def send_chat_messages():
    while True:
        message = input()
        req = {
            'request_type': 'chat',
            'userDetails': {
                'userName': str(userName),
                'userAddress': (host, port)
            },
            'message': str(userName) + ": " + str(message),
            'roomId': str(roomId)
        }
        s.sendto(str(req).encode('utf-8'), server)

def sendJoiningMessage():
    req = {
        'request_type': 'chat',
        'userDetails': {
            'userName': str(userName),
            'userAddress': (host, port)
        },
        'message': str(userName) + " just joined the room",
        'roomId': str(roomId)
    }
    s.sendto(str(req).encode('utf-8'), server)
    

def receive_message():
    while True:
        message, address = s.recvfrom(1024)
        message = ast.literal_eval(message.decode('utf-8'))
        if message['response_type'] == 'question':
            requestResponse(message)
        else:
            print(message['message'])

chatThread = threading.Thread(target=send_chat_messages)
inChatRoom = False
roomId = ''

host = '127.0.0.1'
port = 4010

server = ('127.0.0.1', 4000)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))

userName = input("Enter you name: ")
roomId = ''

listeningThread = threading.Thread(target=receive_message)
listeningThread.start()

def allRoomResponse(message):
    if len(message['allRooms']) == 0:
        print("No rooms found")
        return
    for x in message['allRooms']:
        print(f"Name: {x['roomName']}, ID: {x['roomId']}")

def roomCreateResponse(message):
    if message['error']:
        print(message['message'])
    else:
        global inChatRoom
        inChatRoom = True
        global roomId
        roomId = message['roomId']
        print(message['message'])
        chatThread.start()

def joinRoomResponse(message):
    if message['error']:
        print(message['message'])
    else:
        global inChatRoom
        inChatRoom = True
        global roomId
        roomId = message['roomId']
        print(message['message'])
        chatThread.start()

def send_question_messages(req):
    s.sendto(str(req).encode('utf-8'), server)

def getRoomsRequest():
    req = {
        'request_type': 'question',
        'option': '1'
    }
    send_question_messages(req)

def createRoomRequest():
    
    roomId = input("Enter Room ID: ")
    roomName = input("Enter Room Name: ")
    req = {
        'request_type': 'question',
        'option': '2',
        'roomId': str(roomId),
        'roomName': str(roomName),
        'userDetails': {
            'userName': str(userName),
            'userAddress': (host, port)
        }
    }
    send_question_messages(req)

def joinRoomRequest():
    roomId = input("Enter Room ID: ")
    req = {
        'request_type': 'question',
        'option': '3',
        'roomId': str(roomId),
        'userDetails': {
            'userName': str(userName),
            'userAddress': (host, port)
        }
    }
    send_question_messages(req)

chatThread = threading.Thread(target=send_chat_messages)

while True:
    sleep(0.5)
    if inChatRoom:
        break
    print('1 -> List all rooms')
    print('2 -> Create a room')
    print('3 -> Join a room')
    ch = input("Enter your option: ")
    if ch == '1':
        getRoomsRequest()
    elif ch == '2':
        createRoomRequest()
    elif ch == '3':
        joinRoomRequest()
    else:
        print("No such option")
    
listeningThread.join()
chatThread.join()
