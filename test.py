import threading
from time import ctime, sleep
import tkinter

# var = StringVar()
#
# def thread_function(name):
#     print('Thread {}: starting'.format(name))
#     """create an infinite loop for each thread
#        check the order of execution
#     """
#     while True:
#         u = input('In threading {}: Stop?'.format(name))
#         if u.lower() == 'y':
#             break
#     sleep(2)
#     print('Thread {}: finishing'.format(name))
#
# # https://realpython.com/intro-to-python-threading/
# """now create multiple threads
#    start them one by one
#    notice that the order is random"""
# th = []
# for i in range(2):
#     x = threading.Thread(target=thread_function, args=(i+1,))
#     th.append(x)
#     x.start()
#
# def music(name):
#     for i in range(2):
#         print("I was listening to the music %s! %s" % (name, ctime()))
#         sleep(1)
#
# def move(name):
#     for i in range(2):
#
#         print("I was at the %s! %s" % (name, ctime()))
#         sleep(5)
#
#
# threads = []
# t1 = threading.Thread(target=music, args=(u'love',))
# threads.append(t1)
# t2 = threading.Thread(target=move, args=(u'fine',))
# threads.append(t2)
#
#
# if __name__ == '__main__':
#
#     for t in threads:
#         t.start()
#
#     print('all over %s' % ctime())

import Tkinter
import time
import threading
import random
import Queue
from kivy.app import App
from kivy.clock import Clock
from GUI.Widgets import ChatWindow, PongBall, PongPaddle
from client.chat_client_class import Client
from GUI.Widgets.GameWindow import GameWindow
from kivy.graphics import Color
import threading
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from GUI.customLayouts.customGridLayout import CustomGridLayout
from kivy.animation import *


class ChatApp(App):

    def build(self):
        # Copy from chat_cmdl_client.py, to provide "args" this data to new Client

        import argparse
        parser = argparse.ArgumentParser(description='chat client argument')
        parser.add_argument('-d', type=str, default=None, help='server IP addr')
        args = parser.parse_args()
        # Initialize the whole chatWindow
        chatWindow = ChatWindow.ChatWindow(args)
        chatWindow.size_hint = (1, 1)
        #
        chatWindow.hintButton = Button(text= chatWindow.client.system_msg_to_GUI, pos = (0,0), size_hint_y = 0.18)
        print(chatWindow.hintButton.background_color)
        chatWindow.hintButton.background_color = [121/255, 14/255, 139/255, 1]
        chatWindow.hintButton.background_normal = "border.png"
        chatWindow.hintButton.border = (30,30,30,30)


        #
        chatWindow.ScrollWindow = CustomGridLayout(cols=1, spacing=10, size_hint_y=None) #Button(text="This is msgButton", pos = (0, 100), size = (100000, 200))
        chatWindow.ScrollWindow.bind(minimum_height=chatWindow.ScrollWindow.setter('height'))

        for i in range(1):
            btn = Button(text= "Note: Peer messages will be shown below", size_hint_y=None, height=60,\
                         font_size = 20, font_name = 'Tekton.otf', color = [255/255, 255/255, 255/255, 0])
            btn.background_color = [171/255, 71/255, 188/255, 0]
            btn.background_normal = 'border.png'
            btn.border = (30, 30, 30, 30)

            chatWindow.ScrollWindow.add_widget(btn)
            anim = Animation(background_color=[171 / 255, 71 / 255, 188 / 255, 1], t = 'out_circ',\
                             color = [255/255, 255/255, 255/255, 1], duration = 1.8)
            anim.start(btn)


        scrollBtn = ScrollView(size_hint_y= 0.65, size=(Window.width/2, Window.height/2), \
                               bar_width = '20dp', bar_color = [253/255, 216/255, 53/255, 1],bar_margin = 5)



        scrollBtn.add_widget(chatWindow.ScrollWindow)
        # scrollBtn._change_bar_color([.5, .7, .7, .2])
        #
        def add_input_widget(input):
            btn = Button(text="["+chatWindow.client.name+'] '+ input, size_hint_y=None, \
                         height=60, font_size = 30, font_name = 'Tekton.otf', color = [255/255, 255/255, 255/255, 0])
            #btn.background_color = [0, 1, 0, 1]

            btn.background_color = [240/255, 98/255, 146/255, 0]
            btn.background_normal = 'border.png'
            btn.border = (30, 30, 30, 30)
            chatWindow.ScrollWindow.add_widget(btn)

            anim = Animation(background_color= [240/255, 98/255, 146/255, 1], t='out_expo', \
                            color=[1, 1, 1, 1], duration=1.8)
            anim.start(btn)
        def on_enter(instance):
            chatWindow.client.console_input.append(instance.text)
            if chatWindow.client.sm.state == 3:
                add_input_widget(instance.text)
            instance.text = ''

        chatWindow.inputWindow = TextInput(text= '(Type Enter to send message)',pos = (0,200), size_hint_y= 0.07,\
                                           multiline=False, font_size = 30, font_name = 'Tekton.otf')
        chatWindow.inputWindow.bind(on_text_validate=on_enter)

        #
        btnsLayout = BoxLayout(orientation='vertical', size=(Window.width, Window.height))
        btnsLayout.add_widget(chatWindow.hintButton)
        btnsLayout.add_widget(scrollBtn)
        btnsLayout.add_widget(chatWindow.inputWindow)

        #
        chatWindow.add_widget(btnsLayout)

        #1
        reading_thread1 = threading.Thread(target=chatWindow.updateChat)
        reading_thread1.daemon = True
        reading_thread1.start()

        #2
        reading_thread2 = threading.Thread(target=chatWindow.updateHint)
        reading_thread2.daemon = True
        reading_thread2.start()

        #3
        reading_thread3 = threading.Thread(target=chatWindow.updatePeerMsg)
        reading_thread3.daemon = True
        reading_thread3.start()

        return chatWindow


if __name__ == '__main__':
    ChatApp().run()