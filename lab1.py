import _thread
import os
import socket
import struct
import random


class Test:
    def __init__(self, name):
        self.name = name
        self.message = ""
        self.chatId = ""
        self.num = ""
        self.gp = ("233.2.29.34", 0)
        self.waiting = ""
        self.group_name = ""
        self.mysocket = None

    def getMessage(self):
        while True:
            self.get_msg = self.mysocket.recv(1024)
            self.a = self.mysocket.recv(1024)
            message = str(self.get_msg.decode('utf-8'))

            if self.num == "Admin":
                print("<", message.split('\n')[0], ">", ": ", message.split('\n')[1], sep="")

                if message.find != "wait":
                    self.mysocket.sendto(message.encode("utf-8"), self.gp)
                else:
                    print("".join(["Do you want new user to join us?", message.split('\n')[0], "? [YES/NO] "]))
                    self.waiting = f'{self.num} \n{message} \n {self.a}'
            else:
                if self.name != message.split('\n')[0]:
                    print("<", message.split('\n')[0], ">", ": ", message.split('\n')[1], sep="")

    def sendMessage(self):
        while True:
            try:
                self.message = input()
                self.passing = f'{self.message} \n{self.name}'
                self.chatId = int(input("Enter id: "))
                self.mysocket.sendto(self.passing.encode("utf-8"), ("", self.chatId))
                self.get_msg = self.mysocket.recv(1024)
                self.a = self.mysocket.recv(1024)
                if self.num == "Admin":
                    if self.waiting:
                        message, self.a = (
                            "message",
                            "address",
                        )

                        self.state = False
                        self.check_string = f'{self.name} \n{self.message} \n{self.gp[-1]}' \
                                            f'\n{self.group_name} \n{self.state}'
                        if message == "NO":
                            self.mysocket.sendto(
                                self.check_string.encode("utf-8"), self.a
                            )
                        else:
                            print(f"User {message.split[0]} entered to the room!")
                            self.state = True
                            self.mysocket.sendto(
                                self.check_string.encode("utf-8"), self.a
                            )
                        self.waiting = ''
                    else:
                        self.mysocket.sendto(self.check_string.encode("utf-8"), self.gp)
                else:
                    self.mysocket.sendto(
                        self.passing.encode("utf-8"), ("", self.chatId)
                    )
            except Exception:
                continue

    def main(self):

        self.mysocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print('Hello in our room')
        self.name = ''
        while True:
            if not self.name:
                self.name = input('Enter your nickname: ')
                if not self.name:
                    print('Please enter your name')
                else:
                    break
        print('Your options')
        print('1.Create room')
        print('2.Join room')
        print('3.Exit')
        while True:
            option = int(input())
            if option == 1:
                self.adminOpt()
            elif option == 2:
                self.userOpt()
            elif option == 3:
                os._exit(1)
            else:
                print('Make correct choice please')

            _thread.start_new_thread(Test.getMessage, ())

            Test.sendMessage()

    def userOpt(self):
        self.num = "User"
        accept = f'{self.name} \n wait \n can i join to your group'
        self.chatId = int(input("Enter identifier: "))
        self.mysocket.sendto(accept.encode("utf-8"), ("", self.chatId))
        data, self.a = str(self.mysocket.recv(1024))
        if data.find(''):
            print(f"You join {self.group_name} chat")
            self.mysocket.close()
            self.gp = (self.gp[0], self.gp[-1])
            self.mysocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.mysocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.mysocket.bind(self.gp)
            mreq = struct.pack(
                "4sL", socket.inet_aton(self.gp[0]), socket.INADDR_ANY
            )
            self.mysocket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        else:
            print('You cant join ')

    def adminOpt(self):
        self.num = "Admin"
        ttl = struct.pack("b", 1)
        self.mysocket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        self.gp = (self.gp[0], random.randint(10000, 20000))
        self.group_name = input("Please type your group nickname: ")
        self.mysocket.sendto("".encode("utf-8"), self.gp)
        print("Id: ", self.mysocket.getsockname()[-1])


if __name__ == '__main__':
    Test.main(Test)
