import random
import pygame
from collections import Counter
import os
from classes.players import Player
from classes.table import Table
import uuid


def main():
    number_of_players = 5
    players = {}
    ids = []
    names = []
    for player in range(number_of_players):
        id_already_exists = True
        while id_already_exists:
            new_id = uuid.uuid4()
            if new_id not in ids:
                ids.append(new_id)
                id_already_exists = False

        name_already_exists = True
        while name_already_exists:
            new_player = Player(new_id, 5000, names)
            if new_player.name not in names:
                names.append(new_player.name)
                players[new_id] = new_player
                print(f'A new player has joined: {new_player.name}')
                name_already_exists = False

    table = Table(players)
    play = True
    while play == True:
        current_deck = table.deck
        for draw in range(2):
            for player in players:
                draw = random.randrange(len(current_deck))
                players[player].hand.append(current_deck[draw])
                current_deck.pop(draw)
                print(f"Player {players[player].name} has {players[player].hand} in hand")

        no_winner = True
        while no_winner:
            table.play_round()
            if len(table.running_players) == 1:
                break

            drawn_cards = table.draw(3)
            print(f"{drawn_cards} at the flop")
            table.play_round()
            if len(table.running_players) == 1:
                break

            drawn_cards = table.draw(1)
            print(f"{drawn_cards} at the turn")
            print(f"Cards in the middle : {table.cards_in_the_middle}")
            table.play_round()
            if len(table.running_players) == 1:
                break

            drawn_cards = table.draw(1)
            print(f"{drawn_cards} at the river")
            print(f"Cards in the middle : {table.cards_in_the_middle}")
            table.play_round()
            if len(table.running_players) == 1:
                break
            no_winner = True

        if len(table.running_players) > 1:
            for player in table.running_players:
                players[player].hand.extend(table.cards_in_the_middle)
                print(f"Player {players[player].name} has {players[player].hand} in hand")
                players[player].get_result()
                print(players[player].statement)
                print(players[player].score)

            table.get_winner()
        else:
            for player in table.running_players:
                table.winners = [table.running_players[player]]

        share = len(table.winners)

        winners_list = []
        for winner in table.winners:
            winners_list.append(winner.name)
        winner = " and ".join(winners_list)
        if share > 1:
            print(f"{winner} are sharing the pot: {table.pot/share}")
        else:
            print(f"{winner} wins and gets ${table.pot}")

        table.distribute_gains()

        current_deck = table.reset()

        play = False
    

if __name__ == '__main__':
    print('The game is about to start')

    main()
