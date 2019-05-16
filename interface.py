import tkinter as tk
import tkinter.messagebox
from chat_utils import *
import json
import instruction_rule

window = tk.Tk()
window.title('Super 6+1')
window.geometry('1348x806')

import ball
import hit_the_plane
import wormy
import moving
import block_jump_final
import bouncing_ball
import flappybird
import grid
import hit_fight


class SetComponent:

    def __init__(self, father_layer):
        self.father_layer = father_layer

    def create_frame(self, side, anchor):
        frame = tk.Frame(self.father_layer)
        frame.pack(side=str(side), anchor=str(anchor))
        return frame

    def create_canvas(self, bg, height, width):
        canvas = tk.Canvas(self.father_layer, bg=bg, height=height, width=width)
        return canvas

    def create_image(self, bg, height, width, anchor, file_name, x, y, side, padx, pady):  # 创建canvas和image
        canvas = self.create_canvas(bg, height, width)
        image_file = tk.PhotoImage(file=str(file_name))
        image = canvas.create_image(x, y, anchor=anchor, image=image_file)
        canvas.pack(side=side, padx=padx, pady=pady)


# 创建右方frame
f_right = SetComponent(window)
frame_r = f_right.create_frame('right', 'ne')

# 创建右上方第一个frame
f_right1 = SetComponent(frame_r)
frame_1 = f_right1.create_frame('top', 'n')
#创建画布
canvas_1 = tk.Canvas(frame_1, bg='white', height=100, width=700)
image_file_1 = tk.PhotoImage(file='banner.gif')
image = canvas_1.create_image(320, 0, anchor='n', image=image_file_1)
canvas_1.pack(side='top')


# 创建右方第二个frame,插入两个玩家的头像
f_right2 = SetComponent(frame_r)
frame_2 = f_right2.create_frame('top', 'n')

canvas_2 = tk.Canvas(frame_2, bg='white', height=350, width=700)
image_file_2 = tk.PhotoImage(file='user.gif')
image = canvas_2.create_image(620, 200, anchor='e', image=image_file_2)
canvas_2.pack(side='right')


# 创建记分板
frame_4 = tk.Frame(frame_r)
frame_4.pack(side='top')
frame_4_1 = tk.Frame(frame_4)
frame_4_1.pack(side='right')
frame_4_2 = tk.Frame(frame_4)
frame_4_2.pack(side='right')
#记分板函数被放到了下方
# point_of_1 = total_point(player_1)
# point_of_2 = total_point((player_2))
# l1 = tk.Label(frame_4_1, text=str(point_of_1), bg='white', font=('楷体', 20), width=20, height=5)
# l1.pack(side='top',  padx=10, pady=10)
# l2 = tk.Label(frame_4_2, text=str(point_of_2), bg='white', font=('楷体', 20), width=20, height=5)
# l2.pack(side='top',  padx=10, pady=10)

# l = tk.Label(frame_4, text='这是记分板', bg='#F0FFF0', font=('楷体', 20), width=40, height=5)
# l.pack(side='top', padx=10, pady=10)

# 主持人头像
frame_5 = tk.Frame(frame_r)
frame_5.pack(side='bottom', anchor='se')
canvas_4 = tk.Canvas(frame_5, bg='white', height=300, width=120)
image_file_4 = tk.PhotoImage(file='host.gif')
image2 = canvas_4.create_image(110, 60, anchor='e', image=image_file_4)
canvas_4.pack(side='right',padx=30, pady=3)

# frame_6 = tk.Frame(frame_r)
# frame_6.pack(side='bottom', anchor='s')
# i = tk.Button(frame_6, text='Help', font=("Times", "20", "bold italic"), width=4, height=2,
#                command=close(, instruction_rule.main)
# i.pack(side='bottom', padx=0, pady=0)

class close:

    def __init__(self,func):
        self.quit = quit
        self.func = func

    def check(self):
        self.func.main()
        self.func.quit()

# 创建九宫格
# 创建左方frame
frame_l = tk.Frame(window)
frame_l.pack(side='left', anchor='nw')

# 创建title;一个frame
frame_a = tk.Frame(frame_l)
frame_a.pack(side='top', anchor='n')
canvas_5 = tk.Canvas(frame_a, bg='white', height=250, width=800)
image_file_5 = tk.PhotoImage(file='1.gif')
image3 = canvas_5.create_image(320, 100, anchor='n', image=image_file_5)
image_file_7 = tk.PhotoImage(file='flag.gif')
image7 = canvas_5.create_image(180, -100, anchor='n', image=image_file_7)
canvas_5.pack(side='top')


# frame_a.pack(side='top', anchor='nw')
# l1 = tk.Label(frame_a, text='You are always charmed by gamble', bg='#DEB887', font=("Times", "27", "bold italic"),
#               width=45, height=5)
# l1.pack(side='top')
#
# frame_e = tk.Frame(frame_l)
# frame_e.pack(side='top', anchor='nw')


# l2 = tk.Label(frame_e, text='Choose one button that charms you most', bg='light blue', font=("Times", "20"), width=45,
#               height=5)
# l2.pack(side='top')

# 9个游戏的函数

GAME_STATE = {0:1, 1:1, 2:1, 3:1, 4:1, 5:1, 6:1, 7:1, 8:1, 9:1}




# def game1():  # 游戏函数的通用模版
#     global STATE_1
#     if STATE_1 == 1:
#         a = tkinter.messagebox.askyesno(title='Hi, Warrior',
#                                         message='If you win, you will get a point; lose, get nothing.')
#         if a == True:
#             result = hit_the_plane.main()
#             hit_the_plane.quit()
#
#             if result == "win":  # 游戏胜利
#                 tkinter.messagebox.askyesno(title='Game over', message='You win')
#                 STATE_1 = 0
#             else:
#                 tkinter.messagebox.askyesno(title='Game over', message='You lose ')
#     elif STATE_1 == 0:
#         tkinter.messagebox.askyesno(title='Invalid', message='This game has been tried. Please click another number ')
#

# 打开游戏的class

time = 0 #记录玩游戏的次数
counter = 0
player_1 = []
player_2 = []
# GAME_STATE = {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1}


class play_game:
    global counter
    global player_1, player_2
    GAME_STATE = {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1}
    # counter = 0
    def __init__(self, to_sock, state, game_num, game):  # game 是导入module的触发函数
        self.state = state
        self.game_num = game_num
        self.message = 'If you win, you will get ' + str(self.game_num) + ' point; otherwise, get nothing'
        self.game = game
        self.s = to_sock

    def update_point(self):#用于发送信息的时候，更新分数
        GAME_STATE[self.game_num] = 0
        total1 = 0
        total2 = 0
        for i in player_1:
            total1 += i
        for j in player_2:
            total2 += j

        l1 = tk.Label(frame_4_1, text=str(total1), bg='white', font=('楷体', 20), width=15, height=1)
        l1.pack(side='top', padx=50, pady=0)

        l2 = tk.Label(frame_4_2, text=str(total2), bg='white', font=('楷体', 20), width=15, height=1)
        l2.pack(side='top', padx=50, pady=0)

    def check(self):
        global counter

        if self.state == 1:
            a = tkinter.messagebox.askyesno(title='Hi, Warrior',
                                            message='If you win, you will get points; otherwise, get nothing.')
            if a == True: #player确定进入游戏
                point = 0
                result = self.game.main()

                self.game.quit()

                if result == 0:  # 游戏胜利
                    tkinter.messagebox.askyesno(title='Congratulations', message='You win')
                    point = self.game_num

                else:
                    tkinter.messagebox.askyesno(title='Game over', message='You lose ')
                    point = 0


                GAME_STATE[self.game_num]  = 0
                if result == 0:#游戏胜利
                    if counter % 2 == 0:
                        player_1.append(self.game_num)
                        counter += 1
                    else:

                        player_2.append(self.game_num)
                        counter += 1
                elif result == 1:
                    counter += 1

                self.update_point()
                d = {"action": "gaming", "game_num": self.game_num, "result": result, "point": point }
                mysend(self.s, json.dumps(d))



        elif self.state == 0:
            tkinter.messagebox.askyesno(title='Invalid',
                                        message='This game has been tried. Please click another number ')

def update_point():#用于接受信息时，改变分数
    total1 = 0
    total2 = 0
    for i in player_1:
        total1 += i
    for j in player_2:
        total2 += j

    l1 = tk.Label(frame_4_1, text=str(total1), bg='white', font=('楷体', 20), width=15, height=1)
    l1.pack(side='top', padx=50, pady=0)

    l2 = tk.Label(frame_4_2, text=str(total2), bg='white', font=('楷体', 20), width=15, height=1)
    l2.pack(side='top', padx=50, pady=0)




def hit_me():#游戏测试函数
    pass


#
# def count(player, point):
#     if player == 1:
#         player_1.append(point)
#     else:
#         player_2.append(point)

# def change_player(PLAYER_STATE):
#     if PLAYER_STATE == 1:
#         return 2
#     else:
# #         return 1
#
# def total_point(player):
#     total = 0
#     for i in player:
#         total += player[i]
#     return total

#把分数当道记分板上
# point_of_1 = total_point(player_1)
# point_of_2 = total_point((player_2))
# l1 = tk.Label(frame_4_1, text=str(point_of_1), bg='white', font=('楷体', 40), width=15, height=3)
# l1.pack(side='top',  padx=10, pady=10)
# l2 = tk.Label(frame_4_2, text=str(point_of_2), bg='white', font=('楷体', 40), width=15, height=3)
# l2.pack(side='top',  padx=10, pady=10)
# print(point_of_1)


class Button:

    def __init__(self, to_sock):
        self.s = to_sock

    def create_row(self):
        frame_b1 = tk.Frame(frame_l)
        frame_b1.pack(side='top')
        canvas_6 = tk.Canvas(frame_b1, bg='white', height=80, width=800)
        image_file_6 = tk.PhotoImage(file='gift_row1.gif')
        image4 = canvas_6.create_image(270, 0, anchor='n', image=image_file_6)
        canvas_6.pack(side='top')

        frame_b2 = tk.Frame(frame_l)
        frame_b2.pack(side='top')

        a1 = tk.Button(frame_b2, text='1', font=("Times", "20", "bold italic"), width=4, height=2,
                       command=play_game(self.s, GAME_STATE[1], 1, ball
                                         ).check)  # 这里的函数不能有括号，PLAYER_STATE 不知道需不需要，先保留在这里
        a1.pack(side='left', anchor='w', padx=60, pady=0)
        #
        a2 = tk.Button(frame_b2, text='2', font=("Times", "20", "bold italic"), width=4, height=2,
                       command=play_game(self.s, GAME_STATE[2], 2, hit_the_plane
                                         ).check)  # play_game(STATE_2, 2, f2).check)
        a2.pack(side='left', padx=60, pady=0)
        #
        a3 = tk.Button(frame_b2, text='3', font=("Times", "20", "bold italic"), width=4, height=2,
                       command=play_game(self.s, GAME_STATE[3], 3, moving
                                        ).check)  # play_game(STATE_3, 3, f3).check)
        a3.pack(side='left', padx=60, pady=0)




        # 创建第二行货架
        frame_c1 = tk.Frame(frame_l)
        frame_c1.pack(side='top')
        canvas_7 = tk.Canvas(frame_c1, bg='white', height=140, width=800)
        image_file_7 = tk.PhotoImage(file='gift_row2.gif')
        image5 = canvas_7.create_image(270, 0, anchor='n', image=image_file_7)
        canvas_7.pack(side='top')

        # # 创建第二行的三个按钮
        frame_c2 = tk.Frame(frame_l)
        frame_c2.pack(side='top')
        #
        a4 = tk.Button(frame_c2, text='4', font=("Times", "20", "bold italic"), width=4, height=2,
                       command=play_game(self.s, GAME_STATE[4], 4, wormy).check)  # play_game(STATE_4, 4, f4).check)
        a4.pack(side='left', anchor='w', padx=60, pady=0)
        #
        a5 = tk.Button(frame_c2, text='5', font=("Times", "20", "bold italic"), width=4, height=2,
                       command=play_game(self.s, GAME_STATE[5], 5, block_jump_final).check)  # play_game(STATE_5, 5, f5).check)
        a5.pack(side='left', anchor='w', padx=60, pady=0)

        a6 = tk.Button(frame_c2, text='6', font=("Times", "20", "bold italic"), width=4, height=2,
                       command=play_game(self.s, GAME_STATE[6], 6, bouncing_ball).check)  # play_game(STATE_6, 6, f6).check)
        a6.pack(side='left', anchor='w', padx=60, pady=0)

#

        # 创建第三行货架
        frame_d1 = tk.Frame(frame_l)
        frame_d1.pack(side='top')
        canvas_8 = tk.Canvas(frame_d1, bg='white', height=130, width=800)
        image_file_8 = tk.PhotoImage(file='gift_row3.gif')
        image6 = canvas_8.create_image(270, 0, anchor='n', image=image_file_8)
        canvas_8.pack(side='top')

        # 创建第三行的三个按钮
        frame_d2 = tk.Frame(frame_l)
        frame_d2.pack(side='top')

        a7 = tk.Button(frame_d2, text='7', font=("Times", "20", "bold italic"), width=4, height=2,
                       command=play_game(self.s, GAME_STATE[7], 7, flappybird).check)  # play_game(STATE_7, 7, f7).check)
        a7.pack(side='left', anchor='w', padx=60, pady=0)
        #
        a8 = tk.Button(frame_d2, text='8', font=("Times", "20", "bold italic"), width=4, height=2,
                       command=play_game(self.s, GAME_STATE[8], 8, grid).check)  # play_game(STATE_8, 8, f8).check)
        a8.pack(side='left', anchor='w', padx=60, pady=0)

        a9 = tk.Button(frame_d2, text='9', font=("Times", "20", "bold italic"), width=4, height=2,
                       command=play_game(self.s, GAME_STATE[9], 9, hit_fight).check)  # play_game(STATE_9, 9, f9).check)
        a9.pack(side='left', anchor='w', padx=60, pady=0)



#
def main(to_sock):
    global GAME_STATE
    c = 0
    # window.update_idletasks()
    Button(to_sock).create_row()
    window.update()
    for i in GAME_STATE:
        if i == 0:
            c += 1
        if c == 9:
            break

    # window.update_idletasks()




# window.mainloop()