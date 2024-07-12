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
            if len(table.running_player) == 1:
                break

            drawn_cards = table.draw(3)
            print(f"{drawn_cards} at the flop")
            #table.play_round()
            if len(table.running_player) == 1:
                break

            drawn_cards, current_deck = table.draw(1, current_deck)
            print(f"{drawn_cards} at the turn")
            table.play_round()
            if len(table.running_player) == 1:
                break

            drawn_cards, current_deck = table.draw(1, current_deck)
            print(f"{drawn_cards} at the river")
            table.play_round()
            if len(table.running_player) == 1:
                break
            
        print(f"Cards in the middle : {table.cards_in_the_middle}")
        for player in table.running_players:
            players[player].hand.extend(table.cards_in_the_middle)
            print(f"Player {players[player].name} has {players[player].hand} in hand")
            players[player].get_result()
            print(players[player].statement)
            print(players[player].score)

        table.get_winner()

        share = len(table.winners)

        winners_list = []
        for winner in table.winners:
            winners_list.append(winner.name)
        winner = " and ".join(winners_list)
        if share > 1:
            print(f"{winner} are sharing the pot: {table.pot/share}")
        else:
            print(f"{winner} wins and gets ${table.pot}")

        current_deck = table.reset_deck()

        play = False
    

    

    #Player_3 = ['KingS', '5C', 'KingC', '6H', 'JackD']
    #Player_4 = ['JackS', '5C', 'KingC', '2H', 'JackD']
    #Player_5 = ['QueenS', '5C', 'KingC', '2H', 'QueenD']
    #Player_1 = ['9S', 'QueenS', 'KingS', '10S', 'JackS']
    #Player_2 = ['9S', '10S', '8S', 'QueenS', 'JackS']

    results = []
    hands = []
    prt = []
    p1_result = outcome(Player_1)
    results.append(p1_result[0])
    hands.append(p1_result[1])
    prt.append(p1_result[2])
    p2_result = outcome(Player_2)
    results.append(p2_result[0])
    hands.append(p2_result[1])
    prt.append(p2_result[2])
    p3_result = outcome(Player_3)
    results.append(p3_result[0])
    hands.append(p3_result[1])
    prt.append(p3_result[2])
    p4_result = outcome(Player_4)
    results.append(p4_result[0])
    hands.append(p4_result[1])
    prt.append(p4_result[2])
    p5_result = outcome(Player_5)
    results.append(p5_result[0])
    hands.append(p5_result[1])
    prt.append(p5_result[2])

    print('Player 1 : {} --> {} \nPlayer 2 : {} --> {} \nPlayer 3 : {} --> {}\nPlayer 4 : {} --> {} \nPlayer 5 : {} --> {}'.format(p1_result[1], p1_result[2], p2_result[1], p2_result[2], p3_result[1], p3_result[2], p4_result[1], p4_result[2], p5_result[1], p5_result[2]))

    win = get_winner(results, hands)
    if len(win) > 1:
        draw = 'Draw :'
        for p in range(len(win)):
            draw += (' Player {},'.format(win[p]+1))
        draw += (' with {} '.format(prt[win[0]]))
        print(draw)
    else:
        print('Player {} wins! {}'.format(win[0]+1, prt[win[0]]))

if __name__ == '__main__':
    print('The game is about to start')

    main()