import socket
import ast

class Server:

    def __init__(self) -> None:
        self.chatRooms = []  # list of all room ids
        self.roomMembersDict = {}  # key-value for roomIds-members

    # This function adds a new room with unique id to chatRooms
    # and also creates roomId-members key-value pair with the user who created this room
    def createRoom(self, roomId, roomName, userDetails):
        room = {
            'roomId': roomId,
            'roomName': roomName
        }
        self.chatRooms.append(room)
        self.roomMembersDict[roomId] = [userDetails]

    # This function is called whenever a user joins a room
    # and appends new user details to roomMembersDict[roomId]
    # where roomId is the room joined by the user
    def joinRoom(self, roomId, userDetails):
        self.roomMembersDict[roomId].append(userDetails)

    # return all rooms
    def getAllRooms(self):
        return self.chatRooms

    # return specific room members
    def getRoomMembers(self, roomId):
        return self.roomMembersDict[roomId]

# this function send data to the client which asked for room data

def sendResponse(res, address):
    s.sendto(str(res).encode('utf-8'), address)

def allRoomResponse(address):
    res = {
        'response_type': 'question',
        'option': '1',
        'error': False,
        'allRooms': myServer.getAllRooms()
    }
    sendResponse(res, address)

def roomCreateResponse(message, address):
    roomId = message['roomId']
    if roomExists(roomId):
        res = {
            'response_type': 'question',
            'option': '2',
            'error': True,
            'message': '\nRoom with given Id already exists\n'
        }
        sendResponse(res, address)
    else:
        myServer.createRoom(
            message['roomId'],
            message['roomName'],
            message['userDetails']
        )
        res = {
            'response_type': 'question',
            'option': '2',
            'error': False,
            'message': '\nRoom Created And Joined\n',
            'roomId': str(roomId)
        }
        sendResponse(res, address)

def joinRoomResponse(message, address):
    print("Joining room")
    roomId = message['roomId']
    if roomExists(roomId):
        myServer.joinRoom(
            message['roomId'],
            message['userDetails']
        )
        res = {
            'response_type': 'question',
            'option': '3',
            'error': False,
            'message': '\nRoom Created And Joined\n',
            'roomId': str(roomId)
        }
        sendResponse(res, address)
    else:
        res = {
            'response_type': 'question',
            'option': '3',
            'error': True,
            'message': '\nNo room with given Id\n'
        }
        sendResponse(res, address)

def giveResponse(message, address):
    if message['option'] == '1':
        allRoomResponse(address)
    elif message['option'] == '2':
        roomCreateResponse(message, address)
    else:
        joinRoomResponse(message, address)

def broadcastToRoom(message, address):
    roomMembers = myServer.getRoomMembers(message['roomId'])
    for member in roomMembers:
        if member['userAddress'] == address:
            continue
        res = {
            'response_type': 'chat',
            'message': message['message']
        }
        sendResponse(res, member['userAddress'])

def roomExists(roomId):
    allRooms = myServer.getAllRooms()
    for x in allRooms:
        if x['roomId'] == roomId:
            return True
    return False

myServer = Server()
host = '127.0.0.1'
port = 4000

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))



def listenUpdates():
    message, address = s.recvfrom(1024)
    message = ast.literal_eval(message.decode('utf-8'))
    print(message)
    if (message['request_type'] == 'question'):
        giveResponse(message, address)
    else:
        broadcastToRoom(message, address)

while True:
    listenUpdates()