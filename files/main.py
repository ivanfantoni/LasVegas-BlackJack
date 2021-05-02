from lasvegas import *
from cards import deck_dict
from tkinter import *
from PIL import Image, ImageTk
import time
import threading

class LasVegas:

    def __init__(self, master):
        self.master = master
        self.master.title('LasVegas')
        self.master.geometry('950x600')
        self.master.resizable(False, False)
        #self.color = '#1F9C6A'
        self.color = '#005b13'
        self.master.config(bg=self.color)
        #b_img= Image.open('img/new-casino-game.jpg')
        #b_image = ImageTk.PhotoImage(image=b_img)
        #self.bg_label = Label(self.master, image=b_image)
        #self.bg_label.image = b_image
        #self.bg_label.place(y=0, x=0)

        self.cards = deck_dict

        self.frame_config = {
            'bg':self.color,
            'borderwidth':2,
            'relief':GROOVE,
            'background':self.color
        }

        self.btn_config = {
            'width' : 19,
            'relief':GROOVE
        }

        self.d_d_btn = False
        self.game_deal = False
        self.game_split = False
        self.amount = 0

        self.open_frame()
        self.dealer_frame()
        self.play_frame()
        self.player_frame()
        self.command_frame()
        self.game_frame()


#------------------------------------------------------------------
#                               Frames                            -
#------------------------------------------------------------------


    def dealer_frame(self):
        self.dealer_row = 10
        self.dealer_column = 400

        self.df = Frame(self.master, height=225, width=900)
        self.df.config(self.frame_config)
        self.df.grid(row=1, column=0, pady=25, padx=25)
        self.df.grid_propagate(0)


    def play_frame(self):
        self.dealer_row = 10
        self.dealer_column = 400

        self.p_df = Frame(self.df, height=200, width=200)
        self.p_df.config(self.frame_config, relief=None)
        self.p_df.grid(row=0, column=0)
        self.p_df.grid_propagate(0)
        self.new_game()
        self.bet_frame()
        self.cash_frame()


    def bet_frame(self):
        self.b_frame = Frame(self.of, height=200, width=500)
        self.b_frame.config(self.frame_config, relief=None)
        self.b_frame.grid(row=0, column=0, padx=220)


    def cash_frame(self):
        self.c_frame = Frame(self.df, height=100, width=300)
        self.c_frame.config(self.frame_config, relief=None)
        self.c_frame.grid(row=0, column=1)


    def open_frame(self):
        self.of = Frame(self.master, height=80, width=950)
        self.of.config(bg=self.color)
        self.of.grid(row=2, column=0)
        self.of.grid_propagate(0)


    def player_frame(self):
        self.pf = Frame(self.master, height=225, width=900)
        self.pf.config(self.frame_config)
        self.pf.grid(row=3, column=0)
        self.pf.grid_propagate(0)


    def command_frame(self):
        self.cf = Frame(self.pf, height=220, width=200)
        self.cf.config(self.frame_config, relief=None)
        self.cf.grid(row=0, column=0)
        self.cf.grid_propagate(0)
        self.hit()
        self.stand()


    def game_frame(self):
        self.player_row = 75
        self.player_column = 200
        self.p0_column = 35
        self.p1_column = 380
        self.p0_row= 75
        self.p1_row= 75

        self.gf = Frame(self.pf, height=220, width=690)
        self.gf.config(self.frame_config, relief=None)
        self.gf.grid(row=0, column=1)
        self.gf.grid_propagate(0)


#------------------------------------------------------------------
#                               Buttons                           -
#------------------------------------------------------------------


    def play(self):
        self.game_play = Button(self.p_df, text='PLAY', command=self.bj_deal)
        self.game_play.config(self.btn_config)
        self.game_play.grid(row=0, column=0, padx=10, pady=10)


    def new_game(self):
        self.game_ng = Button(self.p_df, text='NEW GAME', command=self.n_g)
        self.game_ng.config(self.btn_config)
        self.game_ng.grid(row=0, column=0, padx=10, pady=10)


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

        self.d_d_btn = Button(self.b_frame,image=d_d_im, command=self.double_down)
        self.d_d_btn.image = d_d_im
        self.d_d_btn.config(border=0, bg=self.color,fg=self.color, activebackground=self.color, highlightthickness=0)
        self.d_d_btn.grid(row=0, column=0, columnspan=3, padx=220, pady=0, sticky='WE')


    def p_again(self):
        self.game_p_again = Button(self.p_df, text='PLAY AGAIN', command=self.play_again)
        self.game_p_again.config(self.btn_config)
        self.game_p_again.grid(row=3, column=0, padx=10, pady=10)


    def deal(self):
        self.btn_game_deal = Button(self.p_df, text='DEAL', command=self.re_deal)
        self.btn_game_deal.config(self.btn_config)
        self.btn_game_deal.grid(row=3, column=0, padx=10, pady=10)


    def hit(self):
        self.game_hit = Button(self.cf, text='HIT', command=self.player_hit)
        self.game_hit.config(self.btn_config)
        self.game_hit.config(state='disable')
        self.game_hit.grid(row=1, column=0, padx=10, pady=10)


    def split(self):
        if self.d_d_btn == True:
            self.d_d_btn.destroy()
        self.game_split = Button(self.cf, text='SPLIT', command=self.player_split)
        self.game_split.config(self.btn_config)
        self.game_split.grid(row=2, column=0, padx=10, pady=10)


    def stand(self):
        self.game_stand = Button(self.cf, text='STAND', command=self.player_stand)
        self.game_stand.config(self.btn_config)
        self.game_stand.config(state='disable')
        self.game_stand.grid(row=7, column=0, padx=10, pady=10)


    def hit_left(self):
        self.game_hit_l = Button(self.cf, text='HIT LEFT HAND', command=lambda player=0: self.split_hit(player))
        self.game_hit_l.config(self.btn_config)
        self.game_hit_l.grid(row=3, column=0, padx=10, pady=10)


    def hit_right(self):
        self.game_hit_r = Button(self.cf, text='HIT RIGHT HAND', command=lambda player=1: self.split_hit(player))
        self.game_hit_r.config(self.btn_config)
        self.game_hit_r.grid(row=4, column=0, padx=10, pady=10)


    def stand_left(self):
        self.game_stand_left = Button(self.cf, text='STAND LEFT HAND', command=lambda player=0: self.split_player_stand(player))
        self.game_stand_left.config(self.btn_config)
        self.game_stand_left.grid(row=5, column=0, padx=10, pady=10)


    def stand_right(self):
        self.game_stand_right = Button(self.cf, text='STAND RIGHT HAND', command=lambda player=1: self.split_player_stand(player))
        self.game_stand_right.config(self.btn_config)
        self.game_stand_right.grid(row=6, column=0, padx=10, pady=10)


#------------------------------------------------------------------
#                               Functions                         -
#------------------------------------------------------------------


    def n_g(self):
        self.clean()
        self.game = Game(2)
        self.game_ng.destroy()
        self.play()
        self.bet()
        self.amount = 0
        self._cash(self.game._bet.cash)


    def play_again(self):
        self.clean()
        self._cash(self.game._bet.cash)
        self.deal()
        self.bet()


    def bj_bet(self, amount):
        if self.game._bet.amount == 0:
            self.game._bet.amount = amount
        else:
            self.game._bet.amount += amount
        if amount > self.game._bet.cash:
            flash = threading.Thread(target=self.amount_flash)
            flash.start()
        else:
            self.betting = self.game._bet.bet(amount)
            
            self.money.destroy()
            self._cash(self.game._bet.cash)


    def double_down(self):
        self.game._bet.bet(self.game._bet.amount)
        self.game._bet.amount *= 2

        self.d_d_btn.destroy()
        self.master.update()
        self._cash(self.game._bet.cash)
        self.master.update()
        time.sleep(1)
        self.player_hit()
        self.master.update()
        self.player_stand()


    def amount_flash(self):
        for i in range(6):
            self.money.config(foreground='red')
            self.money.update()
            time.sleep(0.1)
            self.money.config(foreground='yellow')
            self.money.update()
            time.sleep(0.1)


    def all_in(self):
        self.game._bet.amount = self.game._bet.cash
        self.betting = self.game._bet.bet(self.game._bet.cash)
        self.money.destroy()
        self._cash(self.game._bet.cash)


    def bj_deal(self):
        self.p0 = False
        self.p1 = False
        self.b_frame.destroy()

        if self.game_deal:
            self.clean()
            time.sleep(0.3)
        self.game.HAND[0] = []
        self.game.HAND[1] = []
    
        self.game_deal = self.game.deal()
        self._cash(self.game._bet.cash)
        self.player_cards(0)
        self.dealer_cards()
        self.scores(0)
        self.player_scores()
        self.game_hit.config(state='active')
        self.game_stand.config(state='active')
        self.game_play.destroy()
        self.new_game()
        self.open_frame()
        self.bet_frame()
        if self.score >= 9 and self.score <= 11:
            self.ddown()
        self._split()
        self._blackjack()


    def re_deal(self):
        self.p0 = False
        self.p1 = False

        if self.game_deal:
            self.clean()
            time.sleep(0.3)
        if len(self.game.HAND) == 3:
            del self.game.HAND['dealer']
            del self.game.HAND[1]
        else:
            del self.game.HAND['dealer']
        self.game.HAND[0] = []
        self.game.HAND[1] = []
        self.game_deal = self.game.deal()
        self._cash(self.game._bet.cash)
        self.player_cards(0)
        self.dealer_cards()
        self.scores(0)
        self.player_scores()
        self.game_hit.config(state='active')
        self.game_stand.config(state='active')
        self.open_frame()
        self.bet_frame()
        if self.score >= 9 and self.score <= 11:
            self.ddown()
        self._split()
        self._blackjack()


    def scores(self, player):
        self.score =  self.game.scores(player)


    def player_scores(self):
        self.p_scores = Label(self.gf, text=self.score, font=('shanti', 36), foreground='yellow', background=self.color)
        self.p_scores.place(y=3, x=160)


    def split_player_scores(self, player):
        self.scores(player)

        if player == 0:
            self.p_scores = Label(self.gf, text=self.score, font=('shanti', 36), foreground='yellow', background=self.color)
            self.p_scores.place(y=3, x=0)
        if player ==1:
            self.p_scores = Label(self.gf, text=self.score, font=('shanti', 36), foreground='yellow', background=self.color)
            self.p_scores.place(y=3, x=330)


    def dealer_scores(self):
        self.d_scores = Label(self.df, text=self.score, font=('shanti', 36), foreground='yellow', background=self.color)
        self.d_scores.place(y=10, x=800)


    def player_hit(self):
        if self.game_split:
            self.game_split.destroy()
        if len(self.game_deal[0]) == 4 or len(self.game_deal[0]) == 8 or len(self.game_deal[0]) == 12:
            self.player_row +=80
        hit = self.game.hit(0)
        self.card_generator(self.gf, self.player_row, self.player_column, hit[0][-1])
        self.scores(0)
        self.player_column += 25
        self.player_row -=20
        if self.score <=21:
            self.p_scores.destroy()
            self.player_scores()
            if self.score == 21:
                #self._player_win()
                self.game_hit.config(state='disable')
                #self.game_stand.config(state='disable')

        else:
            self.p_scores.destroy()
            self.player_scores()
            self._dealer_win()
            self.game_hit.config(state='disable')
            self.game_stand.config(state='disable')


    def split_hit(self, player):
        if player == 0:
            if len(self.game_deal[player]) == 4 or len(self.game_deal[player]) == 8 or len(self.game_deal[player]) == 12:
                self.p0_row +=80
            hit = self.game.hit(player)
            self.card_generator(self.gf, self.p0_row, self.p0_column, hit[player][-1])
            self.scores(player)
            self.p0_column += 25
            self.p0_row -=20

            if self.score <=21:
                self.p_scores.destroy()
                self.split_player_scores(player)
                if self.score == 21:
                    self.game_hit_l.config(state='disable')

            else:
                self.p_scores.destroy()
                self.split_player_scores(player)
                self.game_hit_l.config(state='disable')

        if player == 1:
            if len(self.game_deal[player]) == 4 or len(self.game_deal[player]) == 8 or len(self.game_deal[player]) == 12:
                self.p1_row +=80
            hit = self.game.hit(player)
            self.card_generator(self.gf, self.p1_row, self.p1_column, hit[player][-1])
            self.p1_column += 25
            self.p1_row -=20
            self.scores(player)
            
            if self.score <=21:
                self.p_scores.destroy()
                self.split_player_scores(player)
                if self.score == 21:
                    self.game_hit_r.config(state='disable')

            else:
                self.p_scores.destroy()
                self.split_player_scores(player)
                self.game_hit_r.config(state='disable')


    def player_split(self):
        self.game_split.destroy()
        self.game_hit.destroy()
        self.game_stand.destroy()
        self.p_scores.destroy()
        self.stand_left()
        self.stand_right()
        self.hit_left()
        self.hit_right()
        self.game.split()
        self.game_frame()
        self.player_cards(0, split=True)
        self.split_player_scores(0)
        self.player_cards(1, split=True)
        self.split_player_scores(1)
        self._cash(self.game._bet.cash)


    def split_player_stand(self, player):
        if player == 0:
            self.game_stand_left.config(state='disable')
            self.game_hit_l.config(state='disable')
            self.p0 = True
        if player ==1:
            self.game_stand_right.config(state='disable')
            self.game_hit_r.config(state='disable')
            self.p1 = True

        if self.p0 and self.p1 == True:
            for i in range(2):
                stand = self.game.player_stand(i)

                self.dealer_column -=25
                self.dealer_row -=20
                if i == 0:
                    for e , s in enumerate(self.game_deal['dealer'][1:]):
                        if e+1 == 4 or e+1 == 8 or e+1 == 12:
                            self.dealer_row -=80
                        self.card_generator(self.df, self.dealer_row, self.dealer_column, s)
                        self.dealer_column +=25
                        self.dealer_row +=20
                        self.scores('dealer')
                        self.master.update()
                        time.sleep(0.3)
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
        stand = self.game.player_stand(0)
        self.dealer_column -=25
        self.dealer_row -=20
        for e , s in enumerate(self.game_deal['dealer'][1:]):
            if e+1 == 4 or e+1 == 8 or e+1 == 12:
                self.dealer_row -=80
            self.card_generator(self.df, self.dealer_row, self.dealer_column, s)
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
                    self.card_generator(self.gf, self.p0_row, self.p0_column, c)
                    self.p0_column +=25
                    self.p0_row -=20
                    self.master.update()
                    time.sleep(0.3)
                if player == 1:
                    self.card_generator(self.gf, self.p1_row, self.p1_column, c)
                    self.p1_column +=25
                    self.p1_row -=20
                    self.master.update()
                    time.sleep(0.3)
        else:
            for c in self.game_deal[player]:
                self.card_generator(self.gf, self.player_row, self.player_column, c)
                self.player_column +=25
                self.player_row -=20
                self.master.update()
                time.sleep(0.3)


    def dealer_cards(self):
        self.card_generator(self.df, self.dealer_row, self.dealer_column, self.game_deal['dealer'][0])
        self.dealer_column +=25
        self.dealer_row +=20
        self.master.update()
        time.sleep(0.3)
        self.card_generator(self.df, self.dealer_row, self.dealer_column, 'back')
        self.dealer_column +=25
        self.dealer_row +=20
        self.master.update()
        time.sleep(0.3)


    def card_generator(self, frame, row, column, card):
        img = Image.open(self.cards[card])
        img_resize = img.resize((93, 135), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(img_resize)
        self.card_image = Label(frame, image=image)
        self.card_image.image = image
        self.card_image.place(x=column, y=row)


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
                self._cash(self.game._bet.cash)
                return True
            else:
                self.dealer_column -= 25
                self.dealer_row -=20
                self.card_generator(self.df, self.dealer_row, self.dealer_column, self.game_deal['dealer'][1])
                self.game_stand.config(state='disable')
                self._tie()
        else:
            return False


    def _blackjack(self):
        if self.check_blackjack() == True:
            if self.d_d_btn == True:
                self.d_d_btn.destroy()
            bj_img = Image.open(f'img/bj.png')
            bj_img_resize = bj_img.resize((300, 100), Image.ANTIALIAS)
            bj_im = ImageTk.PhotoImage(bj_img_resize)

            self.bjlabel = Label(self.b_frame,image=bj_im)
            self.bjlabel.image = bj_im
            self.bjlabel.config(border=0, bg=self.color,fg=self.color, activebackground=self.color, highlightthickness=0)
            self.bjlabel.place(x=270, y=30, anchor='center')

            self.game_hit.config(state='disable')
            self.game_stand.config(state='disable')
            self.game._bet.amount = 0
            self.p_again()


    def _split(self):
        if self.check_split() == True:
            self.split()


#------------------------------------------------------------------
#                           Labels Results                        -
#------------------------------------------------------------------


    def _dealer_win(self):
        dw_img = Image.open(f'img/dw.png')
        dw_img_resize = dw_img.resize((300, 100), Image.ANTIALIAS)
        dw_im = ImageTk.PhotoImage(dw_img_resize)

        self.dw_label = Label(self.b_frame,image=dw_im)
        self.dw_label.image = dw_im
        self.dw_label.config(border=0, bg=self.color,fg=self.color, activebackground=self.color, highlightthickness=0)
        self.dw_label.place(x=270, y=30, anchor='center')

        self.p_again()
        self._cash(self.game._bet.cash)
        self.game._bet.amount = 0
        self.game_hit.config(state='disable')
        self.game_stand.config(state='disable')


    def _player_win(self):
        pw_img = Image.open(f'img/pw.png')
        pw_img_resize = pw_img.resize((300, 100), Image.ANTIALIAS)
        pw_im = ImageTk.PhotoImage(pw_img_resize)

        self.pw_label = Label(self.b_frame,image=pw_im)
        self.pw_label.image = pw_im
        self.pw_label.config(border=0, bg=self.color,fg=self.color, activebackground=self.color, highlightthickness=0)
        self.pw_label.place(x=270, y=30, anchor='center')
        self.game._bet.cash = self.game._bet.winnning(self.game._bet.amount)
        self.p_again()
        self._cash(self.game._bet.cash)
        self.game._bet.amount = 0
        self.game_hit.config(state='disable')
        self.game_stand.config(state='disable')


    def _split_player_win(self, player):
        self.p_again()
        if player == 0:
            pw_img = Image.open(f'img/pw.png')
            pw_img_resize = pw_img.resize((240, 80), Image.ANTIALIAS)
            pw_im = ImageTk.PhotoImage(pw_img_resize)

            self.pw_label = Label(self.of,image=pw_im)
            self.pw_label.image = pw_im
            self.pw_label.config(border=0, bg=self.color,fg=self.color, activebackground=self.color, highlightthickness=0)
            self.pw_label.place(x=350, y=30, anchor='center')
            
            self.game._bet.cash = self.game._bet.winnning(self.game._bet.amount)

        if player == 1:
            pw_img = Image.open(f'img/pw.png')
            pw_img_resize = pw_img.resize((240, 80), Image.ANTIALIAS)
            pw_im = ImageTk.PhotoImage(pw_img_resize)

            self.pw_label = Label(self.of,image=pw_im)
            self.pw_label.image = pw_im
            self.pw_label.config(border=0, bg=self.color,fg=self.color, activebackground=self.color, highlightthickness=0)
            self.pw_label.place(x=670, y=30, anchor='center')

            self.game._bet.cash = self.game._bet.winnning(self.game._bet.amount2)

        self._cash(self.game._bet.cash)


    def _split_dealer_win(self, player):
        self.p_again()
        if player == 0:
            dw_img = Image.open(f'img/dw.png')
            dw_img_resize = dw_img.resize((240, 80), Image.ANTIALIAS)
            dw_im = ImageTk.PhotoImage(dw_img_resize)

            self.dw_label = Label(self.of,image=dw_im)
            self.dw_label.image = dw_im
            self.dw_label.config(border=0, bg=self.color,fg=self.color, activebackground=self.color, highlightthickness=0)
            self.dw_label.place(x=350, y=30, anchor='center')

            self.game._bet.amount = 0

        if player == 1:
            dw_img = Image.open(f'img/dw.png')
            dw_img_resize = dw_img.resize((240, 80), Image.ANTIALIAS)
            dw_im = ImageTk.PhotoImage(dw_img_resize)

            self.dw_label = Label(self.of,image=dw_im)
            self.dw_label.image = dw_im
            self.dw_label.config(border=0, bg=self.color,fg=self.color, activebackground=self.color, highlightthickness=0)
            self.dw_label.place(x=670, y=30, anchor='center')

            self.game._bet.amount2 = 0

        self._cash(self.game._bet.cash)


    def _split_tie(self, player):
        self.p_again()
        if player == 0:
            tie_img = Image.open(f'img/tie.png')
            tie_img_resize = tie_img.resize((240, 80), Image.ANTIALIAS)
            tie_im = ImageTk.PhotoImage(tie_img_resize)

            self.tie_label = Label(self.of,image=tie_im)
            self.tie_label.image = tie_im
            self.tie_label.config(border=0, bg=self.color,fg=self.color, activebackground=self.color, highlightthickness=0)
            self.tie_label.place(x=350, y=30, anchor='center')

            self.game._bet.tie(self.game._bet.amount)
            self.game._bet.amount = 0
        if player == 1:
            tie_img = Image.open(f'img/tie.png')
            tie_img_resize = tie_img.resize((240, 80), Image.ANTIALIAS)
            tie_im = ImageTk.PhotoImage(tie_img_resize)

            self.tie_label = Label(self.of,image=tie_im)
            self.tie_label.image = tie_im
            self.tie_label.config(border=0, bg=self.color,fg=self.color, activebackground=self.color, highlightthickness=0)
            self.tie_label.place(x=670, y=30, anchor='center')


            self.game._bet.tie(self.game._bet.amount2)
            self.game._bet.amount2 = 0

        self._cash(self.game._bet.cash)


    def _tie(self):
        self.p_again()
        tie_img = Image.open(f'img/tie.png')
        tie_img_resize = tie_img.resize((300, 100), Image.ANTIALIAS)
        tie_im = ImageTk.PhotoImage(tie_img_resize)

        self.tie_label = Label(self.b_frame,image=tie_im)
        self.tie_label.image = tie_im
        self.tie_label.config(border=0, bg=self.color,fg=self.color, activebackground=self.color, highlightthickness=0)
        self.tie_label.place(x=270, y=30, anchor='center')

        self.game._bet.cash = self.game._bet.tie(self.game._bet.amount)
        self._cash(self.game._bet.cash)
        self.game_hit.config(state='disable')
        self.game_stand.config(state='disable')
        self.game._bet.amount = 0


    def _cash(self, money):
        self.money = Label(self.c_frame, text=f'${money}',background=self.color, font=('ubuntu', 32),foreground='yellow', width=5)
        self.money.grid(row=0, column=1)


    def clean(self):
        self.dealer_frame()
        self.play_frame()
        self.open_frame()
        self.player_frame()
        self.command_frame()
        self.game_frame()
        self.bet_frame()

        
if __name__ == '__main__':
    master = Tk()
    app = LasVegas(master)
    mainloop()
