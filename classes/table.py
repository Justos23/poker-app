import random
from numpy.random import choice

class Table():

    def __init__(self, players):
        self.allplayers = players
        self.allplayerslist = list(self.allplayers.keys())
        self.running_players = self.allplayers.copy()
        self.bb = 25
        self.sb = 10
        self.button = 0
        self.pot = self.bb + self.sb
        self.init_deck = ['2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '10H', 'JackH', 'QueenH','KingH', 'AceH',\
                 '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '10D', 'JackD', 'QueenD','KingD', 'AceD',\
                 '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', 'JackS', 'QueenS','KingS', 'AceS',\
                 '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C', 'JackC', 'QueenC','KingC', 'AceC',]
        self.deck = self.init_deck.copy()
        self.cards_in_the_middle = []
        self.winners = []
        self.bet = 0




    def draw(self, n):
        drawn_cards = []
        for _ in range(n):
            r = random.randrange(len(self.deck))
            drawn_cards.append(self.deck[r])
            self.deck.pop(r)
        self.cards_in_the_middle.extend(drawn_cards)
        return drawn_cards


    def has_sufficient_funds(self, player, action):
        if action == 'call':
            return player.stack >= self.bet
        elif action == 'raise':
            return player.stack > self.bet


    def call(self, player):
        if self.has_sufficient_funds(player, 'call'):
            player.stack -= self.bet
            spent = self.bet
            print(f"{player.name} is calling")
        else:
            spent = player.stack
            player.stack = 0
            print(f"{player.name} is all-in!")
        return spent

    def raise_bet(self, player):
        if player.stack >= self.bet * 2:
            if self.bet == 0:
                spent = self.bb * 2
            else:
                spent = self.bet * 2
            player.stack -= spent
            print(f"{player.name} is raising: ${spent}")
        else:
            spent = player.stack
            player.stack = 0
            print(f"{player.name} puts ${spent} on the table and is all-in!")
        self.bet = spent
        return spent


    def do_fold(self, player):
        del self.running_players[player.id[0]]
        player.is_fold = True
        return -1


    def take_action(self, player):
        if self.bet == 0:
            action = choice([-1, 0, "raise"], 1, p=[0.2, 0.5, 0.3])[0]
        elif self.has_sufficient_funds(player, 'raise') and not self.bet == 0:
            action = choice([-1, "call", "raise"], 1, p=[0.4, 0.5, 0.1])[0]
        else:
            action = choice([-1, "call"], 1, p=[0.5, 0.5])[0]

        if action == "-1":
            print(f"{player.name} has fold")
            action = self.do_fold(player)
        elif action == "0":
            print(f"{player.name} checks")
            action = 0
        elif action == 'call':
            action = self.call(player)
        elif action == 'raise':
            action = self.raise_bet(player)
        return action


    def check_all_good(self, actions):
        bets = [x for x in actions if x != -1] 
        return len(list(set(bets))) == 1



    def end_round(self, winner):
        winner.stack += self.pot
        self.reset()
        return


    def play_round(self): 
        dealer = self.allplayerslist[self.button]
        print(f"{self.allplayers[dealer].name} has the button")
        to_play = self.button + 1
        all_good = False
        actions = [None]*len(self.allplayers)
        while not all_good:
            for n in range(len(self.allplayers)):
                player = self.allplayerslist[to_play%len(self.allplayers)]
                if self.allplayers[player].is_fold:
                    actions[to_play%len(self.allplayers)] = -1
                    to_play += 1
                    continue
                print(f"{self.allplayers[player].name} to play")
                action = self.take_action(self.allplayers[player])
                actions[to_play%len(self.allplayers)] = action
                if action == -1:
                    if len(self.running_players) == 1:
                        return 
                else:
                    self.pot += action
                if self.check_all_good(actions):
                    all_good = True
                    break
                to_play += 1
        self.reset_bet()
        return 


    def get_winner(self):
        highest = [["None"], 0]
        for player in self.running_players:
            highest_score = highest[1]
            if self.running_players[player].score > highest_score:
                highest = [[self.running_players[player]], self.running_players[player].score]
            elif self.running_players[player].score == highest_score:
                highest[0].append(self.running_players[player])
            else:
                continue
        self.winners = highest[0]
        return


    def distribute_gains(self):
        share = len(self.winners)
        for winner in self.winners:
            winner.stack += self.pot/share
        return


    def reset_bet(self):
        self.bet = 0
        return


    def reset(self):
        self.reset_deck()
        self.reset_players()
        self.change_button()
        self.reset_players()

    def reset_deck(self):
        self.deck = self.init_deck
        return 


    def reset_players(self):
        self.running_players = self.allplayers
        return 
    
    def reset_players(self):
        self.winners = []
        for player in self.allplayers:
            self.allplayers[player].reset()
        return 


    def change_button(self):
        self.button = (self.button+1)%len(self.allplayers)
        return