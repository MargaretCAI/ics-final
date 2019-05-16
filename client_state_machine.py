"""
Created on Sun Apr  5 00:00:32 2015

@author: zhengzhang
"""
from chat_utils import *
import json
import interface
import threading
import time
from multiprocessing import Queue

class ClientSM:
    def __init__(self, s):
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me

    def connect_to(self, peer):
        msg = json.dumps({"action":"connect", "target":peer})
        mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        if response["status"] == "success":
            self.peer = peer
            self.out_msg += 'You are connected with '+ self.peer + '\n'
            return (True)
        elif response["status"] == "busy":
            self.out_msg += 'User is busy. Please try again later\n'
        elif response["status"] == "self":
            self.out_msg += 'Cannot talk to yourself (sick)\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return(False)

    def disconnect(self):
        msg = json.dumps({"action":"disconnect"})
        mysend(self.s, msg)
        self.out_msg += 'You are disconnected from ' + self.peer + '\n'
        self.peer = ''

    def proc(self, my_msg, peer_msg):
        self.out_msg = ''
#==============================================================================
# Once logged in, do a few things: get peer listing, connect, search
# And, of course, if you are so bored, just go
# This is event handling instate "S_LOGGEDIN"
#==============================================================================
        if self.state == S_LOGGEDIN:
            # todo: can't deal with multiple lines yet
            if len(my_msg) > 0:

                if my_msg == 'q':
                    self.out_msg += 'See you next time!\n'
                    self.state = S_OFFLINE

                elif my_msg == 'time':
                    mysend(self.s, json.dumps({"action":"time"}))
                    time_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += "Time is: " + time_in

                elif my_msg == 'who':
                    mysend(self.s, json.dumps({"action":"list"}))
                    logged_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += 'Here are all the users in the system:\n'
                    self.out_msg += logged_in

                elif my_msg == 'play':

                    self.out_msg += "Below is an introduction of the game and its rules. Take your time to read."


                elif my_msg[0] == 'c':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.connect_to(peer) == True:
                        self.state = S_CHATTING
                        self.out_msg += 'Connect to ' + peer + '. Chat away!\n\n'
                        self.out_msg += '-----------------------------------\n'
                    else:
                        self.out_msg += 'Connection unsuccessful\n'

                elif my_msg[0] == '?':
                    term = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"search", "target":term}))
                    search_rslt = json.loads(myrecv(self.s))["results"].strip()
                    if (len(search_rslt)) > 0:
                        self.out_msg += search_rslt + '\n\n'
                    else:
                        self.out_msg += '\'' + term + '\'' + ' not found\n\n'

                elif my_msg[0] == 'p' and my_msg[1:].isdigit():
                    poem_idx = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"poem", "target":poem_idx}))
                    poem = json.loads(myrecv(self.s))["results"]
                    # print(poem)
                    if (len(poem) > 0):
                        self.out_msg += poem + '\n\n'
                    else:
                        self.out_msg += 'Sonnet ' + poem_idx + ' not found\n\n'

                else:
                    self.out_msg += menu

            if len(peer_msg) > 0:
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect":
                    self.out_msg += "You are connected with the peer"
                    self.out_msg += '. Chat away!\n\n'
                    self.out_msg += '------------------------------------\n'
                    self.state = S_CHATTING
#==============================================================================
# Start chatting, 'bye' for quit
# This is event handling instate "S_CHATTING"
#==============================================================================
        elif self.state == S_CHATTING:
            if len(my_msg) > 0:     # my stuff going out

                if my_msg == "game":
                    me = self.me
                    mysend(self.s, json.dumps({"action": "to_game", "from": me}))
                    self.state = S_GAMING
                    print('I start the game')
                    # interface.main(self.s)

                else:
                    me = self.me
                    mysend(self.s, json.dumps({"action": "exchange", "from": "[" + me + "]", "message": my_msg}))
                    if my_msg == "bye":
                        self.disconnect()
                        self.state = S_LOGGEDIN
                        self.peer = ''


            if len(peer_msg) > 0:    # peer's stuff, coming in
                peer_msg = json.loads(peer_msg)
                print('---------------------')
                print(peer_msg)
                if peer_msg["action"] == "to_game":
                    self.state = S_GAMING
                    print('I receive the game')


                elif peer_msg["action"] == "connect":
                    self.out_msg += peer_msg["from"] + " joined \n"
                elif peer_msg["action"] == "disconnect":
                    self.state = S_LOGGEDIN
                else:
                    self.out_msg += peer_msg["from"] + peer_msg["message"]


            if self.state == S_LOGGEDIN:
                self.out_msg += menu


        elif self.state == S_GAMING:

#-------------------threading------------------------------------
            # queue = Queue.Queue()




            # self.thread_function1(interface.main)



            if len(peer_msg) > 0:
                peer_msg = json.loads(peer_msg)
                if len(interface.player_1) == 5 and len(interface.player_2) == 5:
                    total1 = 0
                    total2 = 0
                    for i in interface.player_1:
                        total1 += i
                    for j in interface.player_2:
                        total2 += j
                    if total1 > total2:
                        interface.tkinter.messagebox.askyesno(title='Hi, Warrior',
                                                    message='Player 1 win the game')
                    elif total1 < total2:
                        interface.tkinter.messagebox.askyesno(title='Hi, Warrior',
                                                    message='Player 2 win the game')
                    else:
                        interface.tkinter.messagebox.askyesno(title='Hi, Warrior',
                                                    message='Player1 and Player2 are tied')
                    self.state = S_CHATTING
                    interface.window.destroy()



                if peer_msg["action"] == "gaming":

                    print("the gaming msg is here")
                    print(peer_msg)
                    game_num = peer_msg["game_num"]
                    result = peer_msg["result"]
                    if result == 0:
                        if interface.counter % 2 == 0:
                            interface.player_1.append(game_num)
                            interface.counter += 1
                        else:
                            interface.player_2.append(game_num)
                            interface.counter += 1

                        interface.update_point()
                    # self.thread_function2(interface.deal_with_msg, game, result)
                    # t2 = threading.Thread(target=interface.deal_with_msg, args=(game, result,))
                    # t2.start()


            interface.main(self.s)
            # interface.main(self.s)
        else:
            self.out_msg += 'How did you wind up here??\n'
            print_state(self.state)

        return self.out_msg


    #
    # def thread_function1(self, name):
    #     print('Thread {}: starting'.format(name))
    #     """create an infinite loop for each thread
    #        check the order of execution
    #     """
    #     counter = 0
    #     while True:
    #         # u = input('In threading {}: Stop?'.format(name))
    #         interface.Button(self.s).create_row()
    #         counter += 1
    #         if counter == 9:
    #             break
    #     # time.sleep(2)
    #     print('Thread {}: finishing'.format(name))
    #
    #     """now create multiple threads
    #        start them one by one
    #        notice that the order is random"""
    #
    #
    #     x = threading.Thread(target=name)
    #
    #     x.start()
    #
    # def thread_function2(self, name, a, b):
    #     print('Thread {}: starting'.format(name))
    #     """create an infinite loop for each thread
    #        check the order of execution
    #     """
    #     counter = 0
    #     while True:
    #         interface.Button(self.s).create_row()
    #         counter += 1
    #         if counter == 9:
    #             break
    #     print('Thread {}: finishing'.format(name))
    #
    #     """now create multiple threads
    #        start them one by one
    #        notice that the order is random"""
    #
    #     x = threading.Thread(target=name, args=(a,b,))
    #
    #     x.start()