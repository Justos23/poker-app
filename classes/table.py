import random, time
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
        self.money_on_table_this_round = 0




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
            return (player.stack + player.current_bet) >= self.bet
        elif action == 'raise':
            return (player.stack + player.current_bet) > self.bet


    def call(self, player):
        #if the player has already placed money on the table he only should place the difference to call a raise.
        if self.has_sufficient_funds(player, 'call'):
            to_call = (self.bet - player.current_bet)
            player.stack -= to_call
            spent = to_call
            print(f"{player.name} is calling")
        else:
            spent = player.stack
            player.stack = 0
            print(f"{player.name} is all-in!")
        return spent, self.bet

    def raise_bet(self, player):
        if player.stack >= self.bet * 2:
            if self.bet == 0:
                spent = self.bb * 2
            else:
                spent = self.bet * 2 
            player.stack -= (spent + player.current_bet)
            print(f"{player.name} is raising: ${spent}")
        else:
            spent = player.stack
            player.stack = 0
            print(f"{player.name} puts ${spent} on the table and is all-in!")
        self.bet = spent
        return spent, spent


    def do_fold(self, player):
        del self.running_players[player.id[0]]
        player.is_fold = True
        return -1


    def take_action(self, player):
        if self.bet == 0:
            action = choice([-1, 0, "raise"], 1, p=[0.1, 0.55, 0.35])[0]
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
            bet, action = self.call(player)
            self.money_on_table_this_round += bet
            player.current_bet = bet
        elif action == 'raise':
            bet, action = self.raise_bet(player)
            self.money_on_table_this_round += bet
            player.current_bet = bet
        return action


    def check_authorized_action(self, player, action):
        print(f"Your current stack is {player.stack}")
        return any([action in ("-1", "0"), (int(action) >= self.bet and (player.stack + player.current_bet) >= int(action))])


    def real_player_take_action(self, player):
        authorized = False
        while not authorized:
            if self.bet == 0:
                action = input(f"Your turn to play: (Enter -1 to fold, 0 to check, or any amount to raise). You have ${player.stack} in your stack")
            else:
                action = input(f"Your turn to play: {self.bet} to call (Enter -1 to fold, {self.bet} to call or any amount to raise). You have ${player.stack} in your stack")
            authorized = self.check_authorized_action(player, action)
        if action == "-1":
            print(f"{player.name} has fold")
            action = self.do_fold(player)
        elif action == "0":
            print(f"{player.name} checks")
            action = 0
        else:
            #TODO change this part to either raise and update self.bet or call or all-in...
            self.bet = int(action)
            amount_to_put = self.bet - player.current_bet
            player.stack -= amount_to_put
            player.current_bet = self.bet
            print(f"{player.name} puts ${action} on the table")
            if player.stack == 0:
                print(f"{player.name} is all-in")
        return int(action)

    def check_all_good(self, actions):
        bets = [x for x in actions if x != -1] 
        return len(list(set(bets))) == 1


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
                if self.allplayers[player].is_real_player:
                    action = self.real_player_take_action(self.allplayers[player])
                else:
                    action = self.take_action(self.allplayers[player])
                time.sleep(2)
                actions[to_play%len(self.allplayers)] = action
                if action == -1:
                    if len(self.running_players) == 1:
                        self.pot += self.money_on_table_this_round
                        self.reset_bet()
                        return 
                if self.check_all_good(actions):
                    all_good = True
                    break
                to_play += 1
        self.pot += self.money_on_table_this_round
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
        self.money_on_table_this_round = 0
        for player in self.allplayers:
            self.allplayers[player].current_bet = 0
        return


    def reset(self):
        self.reset_deck()
        self.change_button()
        self.reset_players()
        self.reset_pot()


    def reset_deck(self):
        self.deck = self.init_deck.copy()
        self.cards_in_the_middle = []
        return 
    

    def reset_players(self):
        self.winners = []
        self.check_busted()
        for player in self.allplayers:
            self.allplayers[player].reset()
        self.running_players = self.allplayers.copy()
        return 


    def change_button(self):
        self.button = (self.button+1)%len(self.allplayers)
        return
    

    def reset_pot(self):
        self.pot = 0
        return
    
    def check_busted(self):
        players_to_remove = []
        for player in self.allplayers:
            if self.allplayers[player].stack <= 0:
                loser = self.allplayers[player].name
                players_to_remove.append(self.allplayers[player].id[0])
                print(f"{loser} is eliminated!")
        for player in players_to_remove:
            del self.allplayers[player]
        self.allplayerslist = list(self.allplayers.keys())
        return