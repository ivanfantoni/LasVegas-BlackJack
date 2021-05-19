from lasvegas import *
from cards import deck_dict
from sounds import BlackJack_Sounds
from tkinter import *
from PIL import Image, ImageTk
import time
import threading
from random import choice


class LasVegas:

    def __init__(self, master):

        self.bg = {
            'blue': [
                'img/blueback.png',
                'img/blueblackjack.png',
                '#005091'
            ],
            'green':[
                'img/greenback.png',
                'img/greenblackjack.png',
                '#005b13'
            ],
            'red':[
                'img/redback.png',
                'img/redblackjack.png',
                '#8b0000'
            ],
            'grey':[
                'img/greyback.png',
                'img/greyblackjack.png',
                '#494949'
            ]
        }
        self.choice_table = choice(['green', 'blue', 'red', 'grey'])
        self.colors = self.bg[self.choice_table]

        self.master = master
        self.master.title('Las Vegas - BlackJack')
        self.master.geometry('950x600')
        self.master.resizable(False, False)
        self.color = self.colors[2]
        self.master.config(bg=self.color)
        

        self.cards = deck_dict

        self.frame_config = {
            'bg':self.color,
            'borderwidth':2,
            'relief':GROOVE,
            'background':self.color
        }

        self.btn_config = {
            'width' : 17,
            'relief':GROOVE,
            'font':('arial', 10, 'bold')
        }

        self.d_d_btn = False
        self.ins_btn = False
        self.ddbtn = False
        self.game_deal = False
        self.game_split = False
        self.d_scores = False
        self.game_insurance = False
        self.p_stand = False
        self.amount = 0
        self.mbtext = False
        self.play_button = False

        self.backcanvas()
        self.change_table()
        self.snd()
        self.default_buttons()
        self.objects_position()


#------------------------------------------------------------------
#                               Frames                            -
#------------------------------------------------------------------


    def backcanvas(self):
        self.bc = Canvas(self.master, height=600, width=950, bd=0)
        self.bc.place(x=475, y=300, anchor='center')

        b_img= Image.open(self.colors[0])
        b_r = b_img.resize((952, 602), Image.ANTIALIAS)
        b_image = ImageTk.PhotoImage(image=b_r)
        self.bgimg = b_image
        self.background_game = self.bc.create_image(475, 300, anchor='center', image=b_image)
        self.bc.tag_lower(self.background_game)

        back_img= Image.open(self.colors[1])
        back_r = back_img.resize((480, 160), Image.ANTIALIAS)
        back_image = ImageTk.PhotoImage(image=back_r)
        self.logo_image = back_image
        self.logo = self.bc.create_image(475, 300, image=back_image, anchor='center')


    def bet_frame(self):
        self.b_frame = Frame(self.bc, height=200, width=500)
        self.b_frame.config(self.frame_config, relief=None)

        self.bc_b_frame = self.bc.create_window(475, 185, window=self.b_frame, anchor='center')


    def moneybox(self, x, y):
        money_img = Image.open(f'img/money.png')
        money_img_resize = money_img.resize((70, 70), Image.ANTIALIAS)
        money_im = ImageTk.PhotoImage(money_img_resize)

        mousex = master.winfo_pointerx() - master.winfo_rootx()
        mousey = master.winfo_pointery() - master.winfo_rooty()
        pos = [x, y]
        mousepos = [mousex, mousey]   
        self.mb = money_im
        if self.play_button == False:
            if mousex - x > 300:
                xspeed = 2.5
            elif mousex -x >141:
                xspeed = 1.5
            elif mousex -x >140:
                xspeed = 1
            elif x > mousex:
                if x- mousex > 85:
                    xspeed = 0.8
                else:
                    xspeed = 0.3
            else:
                xspeed = 1

            self.chips = self.bc.create_image(mousex, mousey, image=money_im, anchor='nw')
            self.bc.tag_raise(self.chips)

            for _ in range(350):
                if mousepos != pos:
                    if int(self.bc.coords(self.chips)[0]) > x:
                        self.bc.move(self.chips, -xspeed, 0)
                        if int(self.bc.coords(self.chips)[0]) - x < xspeed:
                            xmove = int(self.bc.coords(self.chips)[0]) - x
                            self.bc.move(self.chips, -xmove, 0)
                    elif int(self.bc.coords(self.chips)[0]) < x:
                        self.bc.move(self.chips, xspeed, 0)
                        if x - int(self.bc.coords(self.chips)[0]) < xspeed:
                            xmove = x - int(self.bc.coords(self.chips)[0])
                            self.bc.move(self.chips, xmove, 0)
                    if int(self.bc.coords(self.chips)[1]) < y:
                        self.bc.move(self.chips, 0, 2)
                        if y - int(self.bc.coords(self.chips)[1]) < 2:
                            ymove = y - int(self.bc.coords(self.chips)[1])
                            self.bc.move(self.chips, 0, ymove)

                master.update()
        else:
            self.chips = self.bc.create_image(x, y, image=money_im, anchor='nw')
            self.bc.tag_raise(self.chips)
            master.update()

        self.mbtext = self.bc.create_text(x+34, y+35, text=self.game._bet.amount, fill='white', font='ubuntu', anchor='center')


    def moneybox_split(self, x1, y1, x2, y2):
        money_img = Image.open(f'img/money.png')
        money_img_resize = money_img.resize((70, 70), Image.ANTIALIAS)
        money_im = ImageTk.PhotoImage(money_img_resize)
        
        self.mb1 = money_im
        self.bc.create_image(x1, y1, image=money_im, anchor='nw')
        self.mbtext1 = self.bc.create_text(x1+34, y1+35, text=self.game._bet.amount, fill='white', font='ubuntu', anchor='center')
        self.bc.create_image(x2, y2, image=money_im, anchor='nw')
        self.mbtext2 = self.bc.create_text(x2+34, y2+35, text=self.game._bet.amount, fill='white', font='ubuntu', anchor='center')


    def moneybox_insurance(self, x, y):
        money_img = Image.open(f'img/ins.png')
        money_img_resize = money_img.resize((70, 70), Image.ANTIALIAS)
        money_im = ImageTk.PhotoImage(money_img_resize)
        
        self.mb_ins = money_im
        self.bc.create_image(x, y, image=money_im, anchor='nw')
        self.mbtext_ins = self.bc.create_text(x+34, y+35, text=int(self.game._bet.amount_insurance), fill='white', font='ubuntu', anchor='center')


    def moneybox_ddown(self, x, y):
        money_img = Image.open(f'img/x2.png')
        money_img_resize = money_img.resize((70, 70), Image.ANTIALIAS)
        money_im = ImageTk.PhotoImage(money_img_resize)
        
        self.mb_dd = money_im
        self.bc.create_image(x, y, image=money_im, anchor='nw')


#------------------------------------------------------------------
#                           Cleaned Status                        -
#------------------------------------------------------------------


    def default_buttons(self):
        self.new_game()
        self.exit_btn()


    def objects_position(self):
        self.dealer_row = 90
        self.dealer_column = 475
        self.player_row = 500
        self.player_column = 475
        self.p0_column = 325
        self.p1_column = 625
        self.p0_row= 450
        self.p1_row= 450

        self.ins_btn = False
        self.ddbtn = False


    def snd(self):
        self.sound = BlackJack_Sounds()


#------------------------------------------------------------------
#                               Buttons                           -
#------------------------------------------------------------------


    def play(self):
        i = PhotoImage(file='img/play_.png')
        self.stand_img = i
        self.game_play = self.bc.create_image(475, 240, image=i, anchor='center')
        self.bc.tag_bind(self.game_play, '<Button-1>', lambda event, x=self.game_play: self.button_press(x))
        self.bc.tag_bind(self.game_play, '<ButtonRelease-1>', lambda event, x=self.game_play, func=self.bj_deal: self.button_release(button=x, func=func))
    

    def new_game(self):
        i = PhotoImage(file='img/ng_.png')
        self.ng_img = i
        self.game_ng = self.bc.create_image(100, 40, image=i, anchor='center')
        self.bc.tag_bind(self.game_ng, '<Button-1>', lambda event, x=self.game_ng: self.button_press(x))
        self.bc.tag_bind(self.game_ng, '<ButtonRelease-1>', lambda event, x=self.game_ng, func=self.n_g: self.button_release(button=x, func=func))


    def exit_btn(self):
        i = PhotoImage(file='img/exit_.png')
        self.exit_img = i
        self.game_exit = self.bc.create_image(850, 40, image=i, anchor='center')
        self.bc.tag_bind(self.game_exit, '<Button-1>', lambda event, x=self.game_exit: self.button_press(x))
        self.bc.tag_bind(self.game_exit, '<ButtonRelease-1>', lambda event, x=self.game_exit, func=self.exit: self.button_release(button=x, func=func))


    def change_table(self):
        i = PhotoImage(file='img/ct_.png')
        self.ct_img = i
        self.game_table = self.bc.create_image(850, 90, image=i, anchor='center')
        self.bc.tag_bind(self.game_table, '<Button-1>', lambda event, x=self.game_table: self.button_press(x))
        self.bc.tag_bind(self.game_table, '<ButtonRelease-1>', lambda event, x=self.game_table, func=self.change_table_func: self.button_release(button=x, func=func))


    def bet(self):
        bet_list = [10, 20, 50, 100, 200, 500]
        i = 0
        for column in range(6):
            img = Image.open(f'img/{bet_list[i]}.png')
            img_resize = img.resize((70, 70), Image.ANTIALIAS)
            im = ImageTk.PhotoImage(img_resize)
            self.bet_btn = Button(self.b_frame, image=im, command=lambda amount=bet_list[i]: self.bj_bet(amount))
            self.bet_btn.image = im
            self.bet_btn.config(border=0, bg=self.color,fg=self.color, activebackground=self.color, highlightthickness=0)
            self.bet_btn.grid(row=0, column=column, padx=0, pady=0)
            i += 1

        all_img = Image.open(f'img/all.png')
        all_img_resize = all_img.resize((70, 70), Image.ANTIALIAS)
        all_im = ImageTk.PhotoImage(all_img_resize)

        self.allin_btn = Button(self.b_frame,image=all_im, command=self.all_in)
        self.allin_btn.image = all_im
        self.allin_btn.config(border=0, bg=self.color,fg=self.color, activebackground=self.color, highlightthickness=0)
        self.allin_btn.grid(row=0, column=6, columnspan=3, padx=0, pady=0, sticky='WE')


    def ddown(self):
        d_d_img = Image.open(f'img/x2.png')
        d_d_img_resize = d_d_img.resize((70, 70), Image.ANTIALIAS)
        d_d_im = ImageTk.PhotoImage(d_d_img_resize)

        self.d_d_btn = Button(self.bc,image=d_d_im, command=self.double_down)
        self.d_d_btn.image = d_d_im
        self.d_d_btn.config(border=0, bg=self.color,fg=self.color, activebackground=self.color, highlightthickness=0)

        self.ddbtn = self.bc.create_window(475, 250, window=self.d_d_btn, anchor='center')
        if self.ins_btn != False:
            self.bc.move(self.ins_btn, -35, 0)
            self.bc.move(self.ddbtn, 35, 0)


    def p_again(self):
        i = PhotoImage(file='img/playagain_.png')
        self.playagain_img = i
        self.game_p_again = self.bc.create_image(475, 225, image=i, anchor='center')
        self.bc.tag_bind(self.game_p_again, '<Button-1>', lambda event, x=self.game_p_again: self.button_press(x))
        self.bc.tag_bind(self.game_p_again, '<ButtonRelease-1>', lambda event, x=self.game_p_again, func=self.play_again: self.button_release(button=x, func=func))

        self.change_table()


    def insurance_btn(self):
        if self.game._bet.amount_insurance == 0:
            i_img = Image.open(f'img/ins.png')
            i_img_resize = i_img.resize((70, 70), Image.ANTIALIAS)
            i_im = ImageTk.PhotoImage(i_img_resize)

            self.game_insurance = Button(self.bc, image=i_im, command=self.insurance)
            self.game_insurance.image = i_im
            self.game_insurance.config(border=0, bg=self.color,fg=self.color, activebackground=self.color, highlightthickness=0)

            self.ins_btn = self.bc.create_window(475, 250, window=self.game_insurance, anchor='center')
            if self.ddbtn != False:
                self.bc.move(self.ins_btn, -35, 0)
                self.bc.move(self.ddbtn, 35, 0)


    def deal(self):
        i = PhotoImage(file='img/deal_.png')
        self.deal_img = i
        self.btn_game_deal = self.bc.create_image(475, 240, image=i, anchor='center')
        self.bc.tag_bind(self.btn_game_deal, '<Button-1>', lambda event, x=self.btn_game_deal: self.button_press(x))
        self.bc.tag_bind(self.btn_game_deal, '<ButtonRelease-1>', lambda event, x=self.btn_game_deal, func=self.re_deal: self.button_release(button=x, func=func))


    def hit(self):
        i = PhotoImage(file='img/hit_.png')
        self.hit_img = i
        self.game_hit = self.bc.create_image(100, 400, image=i, anchor='center')
        self.bc.tag_bind(self.game_hit, '<Button-1>', lambda event, x=self.game_hit: self.button_press(x))
        self.bc.tag_bind(self.game_hit, '<ButtonRelease-1>', lambda event, x=self.game_hit, func=self.player_hit: self.button_release(button=x, func=func))


    def split(self):
        if self.d_d_btn == True:
            self.d_d_btn.destroy()
        i = PhotoImage(file='img/split_.png')
        self.split_img = i
        self.game_split = self.bc.create_image(100, 500, image=i, anchor='center')
        self.bc.tag_bind(self.game_split, '<Button-1>', lambda event, x=self.game_split: self.button_press(x))
        self.bc.tag_bind(self.game_split, '<ButtonRelease-1>', lambda event, x=self.game_split, func=self.player_split: self.button_release(button=x, func=func))


    def stand(self):
        i = PhotoImage(file='img/stand_.png')
        self.stand_img = i
        self.game_stand = self.bc.create_image(100, 450, image=i, anchor='center')
        self.bc.tag_bind(self.game_stand, '<Button-1>', lambda event, x=self.game_stand: self.button_press(x))
        self.bc.tag_bind(self.game_stand, '<ButtonRelease-1>', lambda event, x=self.game_stand, func=self.player_stand: self.button_release(button=x, func=func))


    def hit_left(self):
        i = PhotoImage(file='img/s_hit_.png')
        self.l_hit_img = i
        self.game_hit_l = self.bc.create_image(270, 550, image=i, anchor='center')
        self.bc.tag_bind(self.game_hit_l, '<Button-1>', lambda event, x=self.game_hit_l: self.button_press(x))
        self.bc.tag_bind(self.game_hit_l, '<ButtonRelease-1>', lambda event, x=self.game_hit_l, func=self.split_hit, player=0: self.button_release(button=x, func=func, player=player))


    def stand_left(self):
        i = PhotoImage(file='img/s_stand_.png')
        self.l_stand_img = i
        self.game_stand_left = self.bc.create_image(400, 550, image=i, anchor='center')
        self.bc.tag_bind(self.game_stand_left, '<Button-1>', lambda event, x=self.game_stand_left: self.button_press(x))
        self.bc.tag_bind(self.game_stand_left, '<ButtonRelease-1>', lambda event, x=self.game_stand_left, func=self.split_player_stand, player=0: self.button_release(button=x, func=func, player=player))


    def hit_right(self):
        i = PhotoImage(file='img/s_hit_.png')
        self.r_hit_img = i
        self.game_hit_r = self.bc.create_image(570, 550, image=i, anchor='center')
        self.bc.tag_bind(self.game_hit_r, '<Button-1>', lambda event, x=self.game_hit_r: self.button_press(x))
        self.bc.tag_bind(self.game_hit_r, '<ButtonRelease-1>', lambda event, x=self.game_hit_r, func=self.split_hit, player=1: self.button_release(button=x, func=func, player=player))


    def stand_right(self):
        i = PhotoImage(file='img/s_stand_.png')
        self.r_stand_img = i
        self.game_stand_right = self.bc.create_image(700, 550, image=i, anchor='center')
        self.bc.tag_bind(self.game_stand_right, '<Button-1>', lambda event, x=self.game_stand_right: self.button_press(x))
        self.bc.tag_bind(self.game_stand_right, '<ButtonRelease-1>', lambda event, x=self.game_stand_right, func=self.split_player_stand, player=1: self.button_release(button=x, func=func, player=player))


    def button_press(self, button):
        self.bc.move(button, 1, 1)


    def button_release(self, button, func, player=None):
        self.bc.move(button, -1, -1)
        if player != None:
            func(player)
        else:
            func()


#------------------------------------------------------------------
#                               Functions                         -
#------------------------------------------------------------------


    def n_g(self):
        if self.bc.find_withtag(self.game_table):
            self.bc.delete(self.game_table)
        self.clean()
        self.game = Game(2)
        self.bet_frame()
        self.bet()
        self.play()
        self.amount = 0
        self._cash(self.game._bet.cash)
        self.sound.s_welcome()
        self.play_button = False


    def exit(self):
        master.destroy()


    def change_table_func(self):
        colors = []
        for c in self.bg:
            if self.choice_table != c:
                colors.append(c)

        self.choice_table = choice(colors)
        self.colors = self.bg[self.choice_table]
        self.color = self.colors[2]
        self.master.config(bg=self.color)
        self.frame_config = {
            'bg':self.color,
            'borderwidth':2,
            'relief':GROOVE,
            'background':self.color
        }

        self.clean()
        self.change_table()


    def play_again(self):
        self.clean()
        self._cash(self.game._bet.cash)
        self.bet_frame()
        self.bet()
        self.deal()
        self.play_button = False


    def bj_bet(self, amount):
        if self.game._bet.amount == 0:
            self.game._bet.amount = amount
        else:
            self.game._bet.amount += amount
        if amount > self.game._bet.cash:
            flash = threading.Thread(target=self.amount_flash)
            nobet = threading.Thread(target=self.no_bet)
            nobet.start()
            flash.start()
        else:
            self.sound.s_chips()

            self.betting = self.game._bet.bet(amount)
            self.moneybox(360, 450)
            
            self.bc.itemconfigure(self.money, text=f'${self.game._bet.cash}')


    def insurance(self):
        self.sound.s_ins_split()
        self.game_insurance.destroy()
        self.ins = self.game._bet.insurance()
        self.bc.itemconfigure(self.money, text=f'${self.game._bet.cash}')
        self.moneybox_insurance(360, 120)


    def double_down(self):
        if self.game._bet.cash < self.game._bet.amount:
            flash = threading.Thread(target=self.amount_flash)
            flash.start()
        else:
            self.game._bet.bet(self.game._bet.amount)
            self.game._bet.amount *= 2
            self.d_d_btn.destroy()
            self.moneybox_ddown(290, 450)
            self.bc.delete(self.game_hit)
            self.bc.delete(self.game_stand)
            if self.game_split != False:
                self.bc.delete(self.game_split)
            self.master.update()
            self.sound.s_option()
            time.sleep(0.5)
            self.moneybox(360, 450)
            self.master.update()
            self.bc.itemconfigure(self.money, text=f'${self.game._bet.cash}')
            self.master.update()
            time.sleep(1)
            self.player_hit()
            self.master.update()
            time.sleep(0.5)
            self.player_stand()


    def amount_flash(self):
        for i in range(6):
            self.bc.itemconfigure(self.money, fill='red')
            time.sleep(0.1)
            self.bc.itemconfigure(self.money, fill='yellow')
            time.sleep(0.1)


    def no_bet(self):
        self.sound.s_alert()
        self.bc.move(self.bc_b_frame, -5, 0)
        self.master.update()
        time.sleep(0.05)
        self.bc.move(self.bc_b_frame, 10, 0)
        self.master.update()
        time.sleep(0.05)
        self.bc.move(self.bc_b_frame, -10, 0)
        self.master.update()
        time.sleep(0.05)
        self.bc.move(self.bc_b_frame, 10, 0)
        self.master.update()
        time.sleep(0.05)
        self.bc.move(self.bc_b_frame, -10, 0)
        self.master.update()
        time.sleep(0.05)
        self.bc.move(self.bc_b_frame, 5, 0)


    def all_in(self):
        if self.game._bet.cash == 0:
            flash = threading.Thread(target=self.amount_flash)
            nobet = threading.Thread(target=self.no_bet)
            nobet.start()
            flash.start()
        else:
            self.sound.s_chips()
            self.game._bet.amount = self.game._bet.cash
            self.betting = self.game._bet.bet(self.game._bet.cash)
            self.moneybox(360, 450)
            self.bc.itemconfigure(self.money, text=f'${self.game._bet.cash}')


    def bj_deal(self):
        self.play_button = True
        self.p0 = False
        self.p1 = False
        if self.game._bet.amount == 0:
            self.no_bet()
        else:
            self.bc.delete(self.game_play)
            if self.game_deal:
                self.clean()
                self.moneybox(360, 450)
                self._cash(self.game._bet.cash)
                time.sleep(0.3)
            self.game.HAND[0] = []
            self.game.HAND[1] = []

            self.b_frame.destroy()
            self.game_deal = self.game.deal()
            self.player_cards(0)
            self.dealer_cards()
            self.scores(0)
            self.player_scores()
            self.hit()
            self.stand()
            self.new_game()
            if self.score >= 9 and self.score <= 11:
                self.ddown()
            self._split()
            self._blackjack()


    def re_deal(self):
        self.play_button = True
        self.p0 = False
        self.p1 = False
        if self.game._bet.amount == 0:
            self.no_bet()
        else:
            if self.game_deal:
                self.clean()
                self.moneybox(360, 450)
                self._cash(self.game._bet.cash)
                time.sleep(0.3)
            if len(self.game.HAND) == 3:
                del self.game.HAND['dealer']
                del self.game.HAND[1]
            else:
                del self.game.HAND['dealer']
            self.game.HAND[0] = []
            self.game.HAND[1] = []
            self.game_deal = self.game.deal()
            self.player_cards(0)
            self.dealer_cards()
            self.scores(0)
            self.player_scores()
            self.hit()
            self.stand()
            if self.score >= 9 and self.score <= 11:
                self.ddown()
            self._split()
            self._blackjack()


    def scores(self, player):
        self.score =  self.game.scores(player)


    def player_scores(self):
        self.p_scores = self.bc.create_text(400, 410, text=self.score, font=('ubuntu', 36), fill='yellow')


    def split_player_scores(self, player):
        self.scores(player)

        if player == 0:
            self.p_scores_0 = self.bc.create_text(250, 400, text=self.score, font=('ubuntu', 36), fill='yellow')
        if player ==1:
            self.p_scores_1 = self.bc.create_text(550, 400, text=self.score, font=('ubuntu', 36), fill='yellow')


    def dealer_scores(self):
        self.d_scores = self.bc.create_text(370, 50, text=self.score, font=('ubuntu', 36), fill='yellow', anchor='nw')


    def player_hit(self):
        if self.d_d_btn:
            self.d_d_btn.destroy()
        if self.game_split:
<<<<<<< HEAD
            self.bc.delete(self.game_split)
        if self.ins_btn != False:
            self.bc.delete(self.ins_btn)
=======
            self.game_split.destroy()
>>>>>>> parent of c86c97b... Exceptions
        if len(self.game_deal[0]) == 4 or len(self.game_deal[0]) == 8 or len(self.game_deal[0]) == 12:
            self.player_row +=80
        hit = self.game.hit(0)
        self.card_generator(self.bc, self.player_row, self.player_column, hit[0][-1])
        self.scores(0)
        self.master.update()
        self.player_column += 25
        self.player_row -=20
        if self.score <=21:
            self.bc.delete(self.p_scores)
            self.player_scores()
<<<<<<< HEAD
            try:
                if self.score == 21:
                    self.bc.itemconfigure(self.game_hit, state='disable')
                    self.hit_img['format'] = 'png -alpha 0.5'
            except TclError:
                pass
=======
            if self.score == 21:
                self.game_hit.config(state='disable')

>>>>>>> parent of c86c97b... Exceptions
        else:
            self.bc.delete(self.p_scores)
            self.player_scores()
            if self.game._bet.amount_insurance != 0:
                self._dealer_bj()
            self._dealer_win()


    def split_hit(self, player):
        if player == 0:
            if len(self.game_deal[player]) == 4 or len(self.game_deal[player]) == 8 or len(self.game_deal[player]) == 12:
                self.p0_row +=80
            hit = self.game.hit(player)
            self.card_generator(self.bc, self.p0_row, self.p0_column, hit[player][-1])
            self.scores(player)
            self.p0_column += 25
            self.p0_row -=20

            if self.score <=21:
                self.bc.delete(self.p_scores_0)
                self.split_player_scores(player)
                if self.score == 21:
                    self.bc.itemconfigure(self.game_hit_l, state='disable')
                    self.l_hit_img['format'] = 'png -alpha 0.5'

            else:
                self.bc.delete(self.p_scores_0)
                self.split_player_scores(player)
                self.bc.itemconfigure(self.game_hit_l, state='disable')
                self.l_hit_img['format'] = 'png -alpha 0.5'

        if player == 1:
            if len(self.game_deal[player]) == 4 or len(self.game_deal[player]) == 8 or len(self.game_deal[player]) == 12:
                self.p1_row +=80
            hit = self.game.hit(player)
            self.card_generator(self.bc, self.p1_row, self.p1_column, hit[player][-1])
            self.p1_column += 25
            self.p1_row -=20
            self.scores(player)
            
            if self.score <=21:
                self.bc.delete(self.p_scores_1)
                self.split_player_scores(player)
                if self.score == 21:
                    self.bc.itemconfigure(self.game_hit_r, state='disable')
                    self.r_hit_img['format'] = 'png -alpha 0.5'

            else:
                self.bc.delete(self.p_scores_1)
                self.split_player_scores(player)
                self.bc.itemconfigure(self.game_hit_r, state='disable')
                self.r_hit_img['format'] = 'png -alpha 0.5'


    def player_split(self):
        self.bc.itemconfigure(self.game_split, state='disable')
        if self.game._bet.cash < self.game._bet.amount:
            flash = threading.Thread(target=self.amount_flash)
            flash.start()
        else:
            self.sound.s_ins_split()
            time.sleep(0.5)
            self.bc.delete(10)
            self.bc.delete(self.mbtext)
            self.bc.delete(self.p_scores)
            self.clean()
            if self.game._bet.amount_insurance != 0:
                self.moneybox_insurance(360, 120)
            self.game.split()
            self._cash(self.game._bet.cash)
            self.master.update()
            self.bc.delete(self.game_hit)
            self.bc.delete(self.game_stand)
            self.dealer_cards()
            self.moneybox_split(210, 450, 510, 450)
            self.player_cards(0, split=True)
            self.split_player_scores(0)
            self.player_cards(1, split=True)
            self.split_player_scores(1)
            self.stand_left()
            self.stand_right()
            self.hit_left()
            self.hit_right()


    def split_player_stand(self, player):
        if self.game_insurance:
            self.game_insurance.destroy()

        if player == 0:
            self.p0 = True
            self.bc.itemconfigure(self.game_stand_left, state='disable')
            self.l_stand_img['format'] = 'png -alpha 0.5'
            self.bc.itemconfigure(self.game_hit_l, state='disable')
            self.l_hit_img['format'] = 'png -alpha 0.5'
        if player == 1:
            self.p1 = True
            self.bc.itemconfigure(self.game_stand_right, state='disable')
            self.r_stand_img['format'] = 'png -alpha 0.5'
            self.bc.itemconfigure(self.game_hit_r, state='disable')
            self.r_hit_img['format'] = 'png -alpha 0.5'

        if self.p0 == True and self.p1 == True:
            self.p_stand = True
            for i in range(2):
                stand = self.game.player_stand(i)

                self.dealer_column -=25
                self.dealer_row -=20
                if i == 0:
                    for e , s in enumerate(self.game_deal['dealer'][1:]):
                        if e+1 == 3 or e+1 == 6 or e+1 == 9 or e+1 == 12:
                            self.dealer_row -=60
                        self.card_generator(self.bc, self.dealer_row, self.dealer_column, s)
                        self.dealer_column +=25
                        self.dealer_row +=20
                        self.scores('dealer')
                        self.master.update()
                        time.sleep(0.3)
                        if self.d_scores:
                            self.bc.delete(self.d_scores)
                    self.dealer_scores()

                self.state = self.game.end_game(i)
                if self.state == 'dealer':
                    self._split_dealer_win(i)
                if self.state[0] == 'player':
                    self._split_player_win(self.state[1])
                if self.state == 'tie':
                    self._split_tie(i)

            self.game._bet.amount = 0
            self.game._bet.amount2 = 0
        else:
            pass


    def player_stand(self):
        self.bc.itemconfigure(self.game_stand, state='disable')
        self.p_stand = True
        if self.d_d_btn:
            self.d_d_btn.destroy()
        if self.ins_btn != False:
            self.bc.delete(self.ins_btn)
        if self.game_split:
            self.bc.delete(self.game_split)
        stand = self.game.player_stand(0)
        self.dealer_column -=25
        self.dealer_row -=20
        for e , s in enumerate(self.game_deal['dealer'][1:]):
            if e+1 == 3 or e+1 == 6 or e+1 == 9 or e+1 == 12:
                self.dealer_row -=60
            self.card_generator(self.bc, self.dealer_row, self.dealer_column, s)
            self.dealer_column +=25
            self.dealer_row +=20
            self.scores('dealer')
            self.master.update()
            time.sleep(0.3)
        self.dealer_scores()

        self.state = self.game.end_game(0)
        if self.state == 'dealer':
            self._dealer_win()
        if self.state[0] == 'player':
            self._player_win()
        if self.state == 'tie':
            self._tie()


    def player_cards(self, player, split=False):
        if split == True:
            for c in self.game_deal[player]:
                if player == 0:
                    self.card_generator(self.bc, self.p0_row, self.p0_column, c)
                    self.p0_column +=25
                    self.p0_row -=20
                    time.sleep(0.3)
                if player == 1:
                    self.card_generator(self.bc, self.p1_row, self.p1_column, c)
                    self.p1_column +=25
                    self.p1_row -=20
                    time.sleep(0.3)
        else:
            for c in self.game_deal[player]:
                self.card_generator(self.bc, self.player_row, self.player_column, c)
                self.player_column +=25
                self.player_row -=20
                time.sleep(0.3)


    def dealer_cards(self):
        self.card_generator(self.bc, self.dealer_row, self.dealer_column, self.game_deal['dealer'][0])
        self.dealer_column +=25
        self.dealer_row +=20
        time.sleep(0.3)
        self.card_generator(self.bc, self.dealer_row, self.dealer_column, 'back')
        self.dealer_column +=25
        self.dealer_row +=20
        time.sleep(0.3)
        if self.game_deal['dealer'][0][0] == 'A':
            self.insurance_btn()


    def card_generator(self, frame, row, column, card):
        img = Image.open(self.cards[card])
        img_resize = img.resize((84, 122), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(img_resize)
        self.card_image = Label(frame, image=image)
        self.card_image.image = image            
        pos = [column, row]

        if self.p_stand == True:
            self.p_stand = False
            self.c = self.bc.create_window(500, 120, window=self.card_image)
            master.update()
        else:
            self.c = self.bc.create_window(950, 0, window=self.card_image)
            for _ in range(35):
                if self.bc.coords(self.c) != pos:
                    if int(self.bc.coords(self.c)[0]) > column:
                        self.bc.move(self.c, -20, 0)
                        if int(self.bc.coords(self.c)[0]) - column < 20:
                            xmove = int(self.bc.coords(self.c)[0]) - column
                            self.bc.move(self.c, -xmove, 0)
                    if int(self.bc.coords(self.c)[1]) < row:
                        self.bc.move(self.c, 0, 20)
                    master.update()

        self.sound.s_card()

#------------------------------------------------------------------
#                               Checks                            -
#------------------------------------------------------------------


    def check_split(self):
        if self.game_deal[0][0][0] == self.game_deal[0][1][0]:
            return True


    def check_blackjack(self):
        self.scores(0)
        if self.score == 21:
            self.scores('dealer')
            if self.score != 21:
                self.game._bet.cash = self.game._bet.black_jack(self.game._bet.amount)
                return True
            else:
                if self.ins_btn != False:
                    self.bc.delete(self.ins_btn)

                self.dealer_column -= 25
                self.dealer_row -=20
                self.p_stand = True
                self.card_generator(self.bc, self.dealer_row, self.dealer_column, self.game_deal['dealer'][1])
                self.game_stand.config(state='disable')
                self.stand_img['format'] = 'png -alpha 0.5'
                self._tie()
        else:
            return False


    def _blackjack(self):
        if self.check_blackjack() == True:
            if self.game_insurance:
                self.game_insurance.destroy()
            if self.d_d_btn == True:
                self.d_d_btn.destroy()
            bj_img = Image.open(f'img/bj.png')
            bj_im = ImageTk.PhotoImage(bj_img)

            self.bjlabel = Label(self.bc,image=bj_im)
            self.bjlabel.image = bj_im
            self.bjlabel.config(border=0, bg=self.color,fg=self.color, activebackground=self.color, highlightthickness=0)
            self.bc.delete(self.logo)
            self.bc.create_window(475,300, window=self.bjlabel, anchor='center')

            self.bc.delete(self.game_hit)
            self.bc.delete(self.game_stand)
            self.game._bet.amount = 0
            self.p_again()
            self.bc.itemconfigure(self.money, text=f'${self.game._bet.cash}')

            self.sound.s_blackjack()


    def _split(self):
        if self.check_split() == True:
            self.split()


#------------------------------------------------------------------
#                           Labels Results                        -
#------------------------------------------------------------------


    def _dealer_bj(self):
        self.dealer_column -=25
        self.dealer_row -=20
        for e , s in enumerate(self.game_deal['dealer'][1:]):
            if e+1 == 3 or e+1 == 6 or e+1 == 9 or e+1 == 12:
                self.dealer_row -=60
            self.card_generator(self.bc, self.dealer_row, self.dealer_column, s)
            self.dealer_column +=25
            self.dealer_row +=20
            self.scores('dealer')
            self.master.update()
            time.sleep(0.3)
        self.dealer_scores()


    def _dealer_win(self):
        if self.game_insurance:
            self.game_insurance.destroy()

        dw_img = Image.open(f'img/dw.png')
        dw_im = ImageTk.PhotoImage(dw_img)

        self.dw_label = Label(self.bc,image=dw_im)
        self.dw_label.image = dw_im
        self.dw_label.config(border=0, bg=self.color,fg=self.color)

        self.bc.delete(self.logo)
        self.bc.create_window(475, 300, window=self.dw_label, anchor='center')

        self.p_again()
        self.bc.itemconfigure(self.money, text=f'${self.game._bet.cash}')
        self.game._bet.amount = 0
        self.bc.delete(self.game_hit)
        self.bc.delete(self.game_stand)
        time.sleep(0.4)
        self.sound.s_loose()


    def _player_win(self):
        if self.game_insurance:
            self.game_insurance.destroy()

        pw_img = Image.open(f'img/pw.png')
        pw_im = ImageTk.PhotoImage(pw_img)

        self.pw_label = Label(self.bc,image=pw_im)
        self.pw_label.image = pw_im
        self.pw_label.config(border=0, bg=self.color,fg=self.color)
        self.bc.delete(self.logo)
        self.bc.create_window(475, 300, window=self.pw_label, anchor='center')

        self.game._bet.cash = self.game._bet.winnning(self.game._bet.amount)
        self.p_again()
        self.bc.itemconfigure(self.money, text=f'${self.game._bet.cash}')
        self.game._bet.amount = 0
        self.bc.delete(self.game_hit)
        self.bc.delete(self.game_stand)
        time.sleep(0.4)
        self.sound.s_win()


    def _tie(self):
        if self.game_insurance:
            self.game_insurance.destroy()

        self.p_again()
        tie_img = Image.open(f'img/tie.png')
        tie_im = ImageTk.PhotoImage(tie_img)

        self.tie_label = Label(self.bc,image=tie_im)
        self.tie_label.image = tie_im
        self.tie_label.config(border=0, bg=self.color,fg=self.color)

        self.bc.delete(self.logo)
        self.bc.create_window(475, 300, window=self.tie_label, anchor='center')
        time.sleep(0.4)
        self.sound.s_tie()
        self.game._bet.cash = self.game._bet.tie(self.game._bet.amount)
        self.bc.itemconfigure(self.money, text=f'${self.game._bet.cash}')
        self.bc.delete(self.game_hit)
        self.bc.delete(self.game_stand)
        self.game._bet.amount = 0


    def _split_player_win(self, player):
        self.p_again()
        pw_img = Image.open(f'img/pw.png')
        pw_img_resize = pw_img.resize((205, 46), Image.ANTIALIAS)
        pw_im = ImageTk.PhotoImage(pw_img_resize)

        self.pw_label = Label(self.bc,image=pw_im)
        self.pw_label.image = pw_im
        self.pw_label.config(border=0, bg=self.color,fg=self.color)

        if player == 0:            
            self.bc.delete(self.logo)
            self.bc.create_window(350, 300, window=self.pw_label, anchor='center')

            self.game._bet.cash = self.game._bet.winnning(self.game._bet.amount)
            self.sound.s_win()
            self.master.update()
            time.sleep(1)

        if player == 1:
            self.bc.delete(self.logo)
            self.bc.create_window(650, 300, window=self.pw_label, anchor='center')

            self.game._bet.cash = self.game._bet.winnning(self.game._bet.amount2)
            self.bc.itemconfigure(self.money, text=f'${self.game._bet.cash}')
            self.sound.s_win()
            self.master.update()


    def _split_dealer_win(self, player):
        self.p_again()
        dw_img = Image.open(f'img/dw.png')
        dw_img_resize = dw_img.resize((207, 36), Image.ANTIALIAS)
        dw_im = ImageTk.PhotoImage(dw_img_resize)

        self.dw_label = Label(self.bc,image=dw_im)
        self.dw_label.image = dw_im
        self.dw_label.config(border=0, bg=self.color,fg=self.color)

        if player == 0:
            self.bc.delete(self.logo)
            self.bc.create_window(350, 300, window=self.dw_label, anchor='center')

            self.game._bet.amount = 0
            self.sound.s_loose()
            self.master.update()
            time.sleep(1)

        if player == 1:
            self.bc.delete(self.logo)
            self.bc.create_window(650, 300, window=self.dw_label, anchor='center')

            self.game._bet.amount2 = 0
            self.sound.s_loose()
            self.master.update()
            time.sleep(1)

        self.bc.itemconfigure(self.money, text=f'${self.game._bet.cash}')


    def _split_tie(self, player):
        self.p_again()
        tie_img = Image.open(f'img/tie.png')
        tie_img_resize = tie_img.resize((72, 35), Image.ANTIALIAS)
        tie_im = ImageTk.PhotoImage(tie_img_resize)

        self.tie_label = Label(self.bc,image=tie_im)
        self.tie_label.image = tie_im
        self.tie_label.config(border=0, bg=self.color,fg=self.color)

        if player == 0:
            self.bc.delete(self.logo)
            self.bc.create_window(350, 300, window=self.tie_label, anchor='center')

            self.game._bet.tie(self.game._bet.amount)
            self.game._bet.amount = 0
            self.sound.s_tie()
            self.master.update()
            time.sleep(1)

        if player == 1:
            self.bc.delete(self.logo)
            self.bc.create_window(650, 300, window=self.tie_label, anchor='center')


            self.game._bet.tie(self.game._bet.amount2)
            self.game._bet.amount2 = 0
            self.sound.s_tie()
            self.master.update()
            time.sleep(1)

        self.bc.itemconfigure(self.money, text=f'${self.game._bet.cash}')


    def _cash(self, money):
        self.money = self.bc.create_text(220, 15, text=f'${money}',font=('ubuntu', 32),fill='yellow', anchor='nw')


    def clean(self):
        self.backcanvas()
        self.snd()
        self.default_buttons()
        self.objects_position()

        
if __name__ == '__main__':
    import sys, os
    if getattr(sys, 'frozen', False):
        os.chdir(sys._MEIPASS)
    master = Tk()
    master.iconphoto(False, PhotoImage(file='img/ico.png'))
    app = LasVegas(master)
    mainloop()
