from random import shuffle

SUITS = ['C', 'D', 'H', 'S']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

class BlackJack:


    def __init__(self):
        sabot = self.sabot()


    def deck(self):
        deck = []
        for s in SUITS:
            for c in RANKS:
                deck.append(c+s)
        return deck


    def shuffle_deck(self, deck):
        shuffled_deck = shuffle(deck)
        return shuffled_deck


    def sabot(self):
        d1 = self.deck()
        d2 = self.deck()
        big_d = d1+d2
        self.shuffle_deck(big_d)
        return big_d


class Betting:


    def __init__(self):
        self.amount = 0
        self.amount2 = 0
        self.amount_insurance = 0


    def dollars(self):
        self.cash = 1000
        return self.cash


    def black_jack(self, amount):
        self.cash += amount + amount*1.5
        return int(self.cash)


    def winnning(self, amount):
        self.cash += amount*2
        return self.cash


    def tie(self, amount):
        self.cash += amount
        return self.cash


    def bet(self, amount):
        self.cash -= amount
        return self.cash


    def doubledown(self, amount):
        return amount*2


    def insurance(self):
        self.amount_insurance = self.amount*0.5
        self.cash -= int(self.amount_insurance)

class Game(BlackJack):


    def __init__(self, gamers):
        self.gamers = gamers
        self.game_sabot = self.sabot()
        self._bet = Betting()
        self.cash = self._bet.dollars()
        self.HAND = {g:[] for g in range(self.gamers)}


    def deal(self):
        self._bet.amount_insurance = 0
        for g in range(self.gamers):
            if g == self.gamers-1:
                self.HAND['dealer'] = self.HAND[g]
                del self.HAND[g]
        
        for g in self.HAND:
            try:
                self.HAND[g].append(self.game_sabot[0])
                del self.game_sabot[0]
            except IndexError:
                self.game_sabot = self.game_sabot + self.sabot()
                self.HAND[g].append(self.game_sabot[0])
                del self.game_sabot[0]

        for g in self.HAND:
            try:
                self.HAND[g].append(self.game_sabot[0])
                del self.game_sabot[0]
            except IndexError:
                self.game_sabot = self.game_sabot + self.sabot()
                self.HAND[g].append(self.game_sabot[0])
                del self.game_sabot[0]
                self.scores(g)
        return self.HAND


    def hit(self, player):
        try:
            self.HAND[player].append(self.game_sabot[0])
            del self.game_sabot[0]
            self.scores(player)
        except IndexError:
            self.game_sabot = self.game_sabot + self.sabot()
            self.HAND[player].append(self.game_sabot[0])
            del self.game_sabot[0]
            self.scores(player)
        return self.HAND


    def split(self):
        self.HAND[1] = []
        self.HAND[1].append(self.HAND[0][1])
        del self.HAND[0][1]
        self.hit(0)
        self.hit(1)
        self._bet.amount2 = self._bet.amount
        self._bet.bet(self._bet.amount2)


    def dealer_game(self):
        if self._bet.amount_insurance != 0:
            if self.scores('dealer') == 21:
                self._bet.cash += int(self._bet.amount_insurance*2)
        while self.scores('dealer') < 17:
            self.hit('dealer')


    def scores(self, player):
        score = 0
        cards = [x[:-1] for x in self.HAND[player]]
        for c in cards:
            if c == 'J' or c == 'Q' or c == 'K':
                score += 10
            elif c == 'A':
                score += 11
            else:
                score += int(c)

        if score>21:
            for c in cards:
                if c == 'A':
                    score -=10
        return score


    def player_stand(self, player):
        self.dealer_game()
        self.results(player)


    def results(self, player):
        if len(self.HAND) == 2:
            for g in self.HAND:
                if g == 'dealer':
                    self.dealer_result = self.scores('dealer')
                elif type(g) == int:
                    self.player_result = self.scores(player)
            return self.end_game(player)

        if len(self.HAND) == 3:
            self.dealer_result = self.scores('dealer')

            for g in self.HAND:
                if type(g) == int:
                    self.player_result = self.scores(player)
                    self.end_game(player)


    def end_game(self, player):
        if self.player_result > 21:
            state = 'dealer'
        else:
            if self.player_result < self.dealer_result:
                state = 'dealer'
            if self.player_result > self.dealer_result:
                state = ['player', player]
            if self.player_result == self.dealer_result:
                state = 'tie'
            if self.dealer_result > 21:
                state = ['player', player]

        self.result = state
        return self.result