import socket
import threading
from tokenize import String
from venv import create


class Server:

    def __init__(self) -> None:
        self.chatRooms = []  # list of all room ids
        self.roomMembersDict = {}  # key-value for roomIds-members

    # This function adds a new room with unique id to chatRooms
    # and also creates roomId-members key-value pair with the user who created this room
    def createRoom(self, roomId, userDetails):
        self.chatRooms.append(roomId)
        self.roomMembersDict[roomId] = [userDetails]

    # This function is called whenever a user joins a room
    # and appends new user details to roomMembersDict[roomId]
    # where roomId is the room joined by the user
    def addUserToRoom(self, roomId, userDetails):
        self.roomMembersDict[roomId].append(userDetails)

    # return all rooms
    def getAllRooms(self):
        return self.chatRooms

    # return specific room members
    def getRoomMembers(self, roomId):
        return self.roomMembersDict[roomId]

myServer = Server()
while True:
    print("1     -> Create Room")
    print("2     -> Add Member To Room")
    print("3     -> Get all rooms Id")
    print("4     -> Get room members")
    print("Other -> Exit")
    choice = input()
    if (choice == '1'):
        print('Enter Room Id: ', end="")
        roomId = input()
        print('Enter User Id: ', end="")
        userId = input()
        myServer.createRoom(roomId, userId)
        print(f"Room Created with Id {roomId} and first user {userId}")
    elif (choice == '2'):
        print('Enter Room Id: ', end="")
        roomId = input()
        print('Enter User Id: ', end="")
        userId = input()
        myServer.addUserToRoom(roomId, userId)
        print(f"User {userId} added to room {roomId}")
    elif (choice == '3'):
        print(myServer.getAllRooms())
    elif (choice == '4'):
        print('Enter Room Id: ', end="")
        roomId = input()
        allRooms = myServer.getAllRooms()
        if not allRooms.__contains__(roomId):
            print(f"No room found with {roomId} ID")
        else:
            print(myServer.getRoomMembers(roomId))
    else:
        break
