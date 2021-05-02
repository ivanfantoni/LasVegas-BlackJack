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
            ]
        }
        self.colors = self.bg[choice(['green', 'blue'])]

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
        self.game_deal = False
        self.game_split = False
        self.d_scores = False
        self.game_insurance = False
        self.amount = 0

        self.backcanvas()
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
        self.bc.create_image(475, 300, anchor='center', image=b_image)
        self.bc.image=b_image

        back_img= Image.open(self.colors[1])
        back_r = back_img.resize((480, 160), Image.ANTIALIAS)
        back_image = ImageTk.PhotoImage(image=back_r)
        self.bg_label = Label(self.bc, image=back_image, bd=0)
        self.bg_label.image = back_image

        self.bc.create_window(475, 300, window=self.bg_label, anchor='center')


    def bet_frame(self):
        self.b_frame = Frame(self.bc, height=200, width=500)
        self.b_frame.config(self.frame_config, relief=None)

        self.bc_b_frame = self.bc.create_window(475, 170, window=self.b_frame, anchor='center')


    def moneybox(self, x, y):
        money_img = Image.open(f'img/money.png')
        money_img_resize = money_img.resize((70, 70), Image.ANTIALIAS)
        money_im = ImageTk.PhotoImage(money_img_resize)
        
        self.mb = money_im
        self.bc.create_image(x, y, image=money_im, anchor='nw')
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


    def snd(self):
        self.sound = BlackJack_Sounds()


#------------------------------------------------------------------
#                               Buttons                           -
#------------------------------------------------------------------


    def play(self):
        self.game_play = Button(self.bc, text='PLAY', command=self.bj_deal)
        self.game_play.config(self.btn_config)

        self.bc.create_window(475, 225, window=self.game_play, anchor='center')
        

    def new_game(self):
        self.game_ng = Button(self.bc, text='NEW GAME', command=self.n_g)
        self.game_ng.config(self.btn_config)

        self.bc.create_window(25, 25, window=self.game_ng, anchor='nw')


    def exit_btn(self):
        self.game_exit = Button(self.bc, text='EXIT', command=self.exit)
        self.game_exit.config(self.btn_config)

        self.bc.create_window(925, 25, window=self.game_exit, anchor='ne')


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

        self.bc.create_window(475, 215, window=self.d_d_btn, anchor='center')


    def p_again(self):
        self.game_p_again = Button(self.bc, text='PLAY AGAIN', command=self.play_again)
        self.game_p_again.config(self.btn_config)

        self.bc.create_window(475, 225, window=self.game_p_again, anchor='center')


    def insurance_btn(self):
        self.game_insurance = Button(self.bc, text='INSURANCE', command=self.insurance)
        self.game_insurance.config(self.btn_config, width=8)

        self.bc.create_window(475, 267, window=self.game_insurance, anchor='center')


    def deal(self):
        self.btn_game_deal = Button(self.bc, text='DEAL', command=self.re_deal)
        self.btn_game_deal.config(self.btn_config)

        self.bc.create_window(475, 225, window=self.btn_game_deal, anchor='center')


    def hit(self):
        self.game_hit = Button(self.bc, text='HIT', command=self.player_hit)
        self.game_hit.config(self.btn_config)

        self.bc.create_window(25, 400, window=self.game_hit, anchor='nw')


    def split(self):
        if self.d_d_btn == True:
            self.d_d_btn.destroy()
        self.game_split = Button(self.bc, text='SPLIT', command=self.player_split)
        self.game_split.config(self.btn_config)

        self.bc.create_window(25, 500, window=self.game_split, anchor='nw')


    def stand(self):
        self.game_stand = Button(self.bc, text='STAND', command=self.player_stand)
        self.game_stand.config(self.btn_config)

        self.bc.create_window(25, 450, window=self.game_stand, anchor='nw')


    def hit_left(self):
        self.game_hit_l = Button(self.bc, text='HIT', command=lambda player=0: self.split_hit(player))
        self.game_hit_l.config(self.btn_config, width=7)

        self.bc.create_window(275, 550, window=self.game_hit_l, anchor='center')


    def stand_left(self):
        self.game_stand_left = Button(self.bc, text='STAND', command=lambda player=0: self.split_player_stand(player))
        self.game_stand_left.config(self.btn_config, width=7)

        self.bc.create_window(375, 550, window=self.game_stand_left, anchor='center')


    def hit_right(self):
        self.game_hit_r = Button(self.bc, text='HIT', command=lambda player=1: self.split_hit(player))
        self.game_hit_r.config(self.btn_config, width=7)

        self.bc.create_window(575, 550, window=self.game_hit_r, anchor='center')


    def stand_right(self):
        self.game_stand_right = Button(self.bc, text='STAND', command=lambda player=1: self.split_player_stand(player))
        self.game_stand_right.config(self.btn_config, width=7)

        self.bc.create_window(675, 550, window=self.game_stand_right, anchor='center')


#------------------------------------------------------------------
#                               Functions                         -
#------------------------------------------------------------------


    def n_g(self):
        self.clean()
        self.game = Game(2)
        self.bet_frame()
        self.play()
        self.bet()
        self.amount = 0
        self._cash(self.game._bet.cash)
        self.sound.s_welcome()


    def exit(self):
        master.destroy()


    def play_again(self):
        self.clean()
        self._cash(self.game._bet.cash)
        self.deal()
        self.bet_frame()
        self.bet()


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
            
            self.bc.itemconfigure(self.money, text=f'${self.game._bet.cash}')
            self.moneybox(360, 450)


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

            self.sound.s_option()
            time.sleep(0.5)
            self.d_d_btn.destroy()
            self.moneybox(360, 450)
            self.master.update()
            self.bc.itemconfigure(self.money, text=f'${self.game._bet.cash}')
            self.master.update()
            time.sleep(1)
            self.player_hit()
            self.master.update()
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
        self.game._bet.amount = self.game._bet.cash
        self.betting = self.game._bet.bet(self.game._bet.cash)
        self.bc.itemconfigure(self.money, text=f'${self.game._bet.cash}')
        self.moneybox(360, 450)


    def bj_deal(self):
        self.p0 = False
        self.p1 = False
        if self.game._bet.amount == 0:
            self.no_bet()
        else:
            self.game_play.destroy()

            if self.game_deal:
                self.clean()
                self.moneybox(360, 450)
                self._cash(self.game._bet.cash)
                time.sleep(0.3)
            self.game.HAND[0] = []
            self.game.HAND[1] = []

            #self.clean()
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
            self.game_split.destroy()
        if len(self.game_deal[0]) == 4 or len(self.game_deal[0]) == 8 or len(self.game_deal[0]) == 12:
            self.player_row +=80
        hit = self.game.hit(0)
        self.card_generator(self.bc, self.player_row, self.player_column, hit[0][-1])
        self.scores(0)
        self.player_column += 25
        self.player_row -=20
        if self.score <=21:
            self.bc.delete(self.p_scores)
            self.player_scores()
            if self.score == 21:
                self.game_hit.config(state='disable')

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
                    self.game_hit_l.config(state='disable')

            else:
                self.bc.delete(self.p_scores_0)
                self.split_player_scores(player)
                self.game_hit_l.config(state='disable')

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
                    self.game_hit_r.config(state='disable')

            else:
                self.bc.delete(self.p_scores_1)
                self.split_player_scores(player)
                self.game_hit_r.config(state='disable')


    def player_split(self):
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
            self.game_hit.destroy()
            self.game_stand.destroy()
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
            self.game_stand_left.config(state='disable')
            self.game_hit_l.config(state='disable')
            self.p0 = True
        if player ==1:
            self.game_stand_right.config(state='disable')
            self.game_hit_r.config(state='disable')
            self.p1 = True

        if self.p0 == True and self.p1 == True:
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
        if self.game_split:
            self.game_split.destroy()
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
                    self.master.update()
                    time.sleep(0.3)
                if player == 1:
                    self.card_generator(self.bc, self.p1_row, self.p1_column, c)
                    self.p1_column +=25
                    self.p1_row -=20
                    self.master.update()
                    time.sleep(0.3)
        else:
            for c in self.game_deal[player]:
                self.card_generator(self.bc, self.player_row, self.player_column, c)
                self.player_column +=25
                self.player_row -=20
                self.master.update()
                time.sleep(0.3)


    def dealer_cards(self):
        self.card_generator(self.bc, self.dealer_row, self.dealer_column, self.game_deal['dealer'][0])
        self.dealer_column +=25
        self.dealer_row +=20
        self.master.update()
        time.sleep(0.3)
        self.card_generator(self.bc, self.dealer_row, self.dealer_column, 'back')
        self.dealer_column +=25
        self.dealer_row +=20
        self.master.update()
        time.sleep(0.3)
        if self.game_deal['dealer'][0][0] == 'A':
            self.insurance_btn()


    def card_generator(self, frame, row, column, card):
        img = Image.open(self.cards[card])
        img_resize = img.resize((84, 122), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(img_resize)
        self.card_image = Label(frame, image=image)
        self.card_image.image = image
            
        self.bc.create_window(column, row, window=self.card_image)
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
                self.dealer_column -= 25
                self.dealer_row -=20
                self.card_generator(self.bc, self.dealer_row, self.dealer_column, self.game_deal['dealer'][1])
                self.game_stand.config(state='disable')
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
            self.bg_label.destroy()
            self.bc.create_window(475,300, window=self.bjlabel, anchor='center')

            self.game_hit.destroy()
            self.game_stand.destroy()
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

        self.bg_label.destroy()
        self.bc.create_window(475, 300, window=self.dw_label, anchor='center')

        self.p_again()
        self.bc.itemconfigure(self.money, text=f'${self.game._bet.cash}')
        self.game._bet.amount = 0
        self.game_hit.destroy()
        self.game_stand.destroy()
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
        self.bg_label.destroy()
        self.bc.create_window(475, 300, window=self.pw_label, anchor='center')

        self.game._bet.cash = self.game._bet.winnning(self.game._bet.amount)
        self.p_again()
        self.bc.itemconfigure(self.money, text=f'${self.game._bet.cash}')
        self.game._bet.amount = 0
        self.game_hit.destroy()
        self.game_stand.destroy()
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

        self.bg_label.destroy()
        self.bc.create_window(475, 300, window=self.tie_label, anchor='center')
        time.sleep(0.4)
        self.sound.s_tie()
        self.game._bet.cash = self.game._bet.tie(self.game._bet.amount)
        self.bc.itemconfigure(self.money, text=f'${self.game._bet.cash}')
        self.game_hit.destroy()
        self.game_stand.destroy()
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
            self.bg_label.destroy()
            self.bc.create_window(350, 300, window=self.pw_label, anchor='center')

            self.game._bet.cash = self.game._bet.winnning(self.game._bet.amount)
            self.sound.s_win()
            self.master.update()
            time.sleep(1)

        if player == 1:
            self.bg_label.destroy()
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
            self.bg_label.destroy()
            self.bc.create_window(350, 300, window=self.dw_label, anchor='center')

            self.game._bet.amount = 0
            self.sound.s_loose()
            self.master.update()
            time.sleep(1)

        if player == 1:
            self.bg_label.destroy()
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
            self.bg_label.destroy()
            self.bc.create_window(350, 300, window=self.tie_label, anchor='center')

            self.game._bet.tie(self.game._bet.amount)
            self.game._bet.amount = 0
            self.sound.s_tie()
            self.master.update()
            time.sleep(1)

        if player == 1:
            self.bg_label.destroy()
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
    master = Tk()
    master.iconphoto(False, PhotoImage(file='img/ico.png'))
    app = LasVegas(master)
    mainloop()
