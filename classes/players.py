import names
from collections import Counter


class Player():

    def __init__(self, id, buy_in, players):
        self.id = id,
        self.stack = buy_in
        self.is_fold = False
        self.hand = []
        self.name = self.generate_random_name()
        self.statement = ""
        self.score = 0
        self.digit_dict = {'2' : 2, '3' : 3, '4' : 4, '5' : 5, '6' : 6, '7' : 7, '8' : 8, '9' : 9, '10' : 10, 'Jack' : 11, 'Queen' : 12, 'King' : 13, 'Ace' : 14}

    def generate_random_name(self):
        return names.get_first_name()



    def get_digit(self, hand):
            digit =  []
            for card in range(len(hand)):
                digit.append(self.digit_dict[hand[card][:-1]])
            return digit


    def get_suit(self, hand):
        suite = []
        for card in range(len(hand)):
            suite.append(hand[card][-1])
        return suite


    def check_flush(self, suit, hand):
        for key, val in suit.items():
            if val >= 5:
                return key
        return None


    def check_straight(self, digits):
        if 14 in digits:
            digits.append(1)
        straight_high = None
        i = 1
        sorted_cards = sorted(digits)
        prev = sorted_cards[0]
        for d in sorted_cards[1:]:
            
            if prev + 1 == d:
                i += 1
                if i >= 5:
                    straight_high = d
            else:
                i = 1
            prev = d
        return straight_high
        

    def check_four_of_a_kind(self, digit):
        for key, val in digit.items():
            if val == 4:
                high = max([k for k,v in digit.items() if k != key])
                return key, [key, high]
        return None, None


    def check_full_house(self, digit):
        full = []
        three = [k for k,v in digit.items() if v == 3]
        two = [k for k,v in digit.items() if v == 2]
        if three:
            three = max(three)
            full.append(three)
        if two:
            two = max(two)
            full.append(two)
        if len(full) == 2:
            return full
        else:
            return None


    def check_three_of_a_kind(self, digit):
        three = [k for k,v in digit.items() if v == 3]
        if three:
            key = max(three)
            three_of_a_kind = [key]
            for n in range(2):
                three_of_a_kind.append(max([k for k,v in digit.items() if k not in three_of_a_kind]))
            return key, three_of_a_kind
        else:
            return None, None


    def check_two_pairs(self, digit):
        two_pairs = [k for k,v in digit.items() if v == 2]
        if len(two_pairs) >= 2:
            two_pairs = sorted(two_pairs, reverse=True)[:2]
            keys = two_pairs
            high = max([k for k,v in digit.items() if k not in two_pairs])
            two_pairs.append(high)
            return keys, two_pairs
        else:
            return None, None
        
    def check_one_pair(self, digit):
        pair = [k for k,v in digit.items() if v == 2]
        if len(pair) > 0:
            key = pair[0]
            for n in range(3):
                pair.append(max([k for k,v in digit.items() if k not in pair]))
        else:
            key, pair  = None, None
        return key, pair

    def get_score(self, result, hand):
        n = 2
        for card in hand:
            result += card/(10**n)
            n = n + 2
        return round(result, 10)

    def get_result(self):
        suit = self.get_suit(self.hand)
        digits = self.get_digit(self.hand)
        s = Counter(suit)
        d = Counter(digits)
        flush_color = self.check_flush(s, self.hand)
        if not flush_color == None:
            flush_hand = [x for x in self.hand if x[-1] == flush_color]
            flush_digits = self.get_digit(flush_hand)
            flush_straight_high = self.check_straight(flush_digits)
            if not flush_straight_high == None:
                if flush_straight_high == 14:
                    result = 9
                    self.statement = f"{self.name} has a Royal flush!"
                    self.score = result
                    return
                else:
                    result = self.get_score(8, [flush_straight_high])
                    self.statement = f"{self.name} has a flush straight of high {list(self.digit_dict.values()).index(flush_straight_high)}"
                    self.score = result
                    return
            else:
                temp_result = self.get_score(5, sorted(flush_digits, reverse=True)) 
        key, four_of_a_kind = self.check_four_of_a_kind(d)
        if not four_of_a_kind == None:
            result = self.get_score(7, four_of_a_kind)
            self.statement = f"{self.name} has a four of a kind: {list(self.digit_dict.keys())[list(self.digit_dict.values()).index(key)]}"
            self.score = result
            return
        full = self.check_full_house(d)
        if not full == None:
            result = self.get_score(6, full)
            self.statement = f"{self.name} has a full house: {list(self.digit_dict.keys())[list(self.digit_dict.values()).index(full[0])]} by the {list(self.digit_dict.keys())[list(self.digit_dict.values()).index(full[1])]}"
            self.score = result
            return
        if "temp_result" in locals():
            self.statement = f"{self.name} has a flush of high {list(self.digit_dict.keys())[list(self.digit_dict.values()).index(sorted(flush_digits)[-1])]}"
            self.score = temp_result
            return
        straight_high = self.check_straight(digits)
        if not straight_high == None:
            result = self.get_score(4, sorted([straight_high], reverse=True))
            self.statement = f"{self.name} has a flush straight of high {list(self.digit_dict.keys())[list(self.digit_dict.values()).index(straight_high)]}"
            self.score = result
            return
        key, three_of_a_kind = self.check_three_of_a_kind(d)
        if not three_of_a_kind == None:
            result = self.get_score(3, three_of_a_kind)
            self.statement = f"{self.name} has a three of a kind of {list(self.digit_dict.keys())[list(self.digit_dict.values()).index(key)]}"
            self.score = result
            return
        key, two_pairs = self.check_two_pairs(d)
        if not two_pairs == None:
            result = self.get_score(2, two_pairs)
            self.statement = f"{self.name} has two pairs: {list(self.digit_dict.keys())[list(self.digit_dict.values()).index(key[0])]} and {list(self.digit_dict.keys())[list(self.digit_dict.values()).index(key[1])]}"
            self.score = result
            return
        key, one_pair = self.check_one_pair(d)
        if not one_pair == None:
            result = self.get_score(1, one_pair)
            self.statement = f"{self.name} has one pair of {list(self.digit_dict.keys())[list(self.digit_dict.values()).index(key)]}"
            self.score = result
            return
        else:
            result = self.get_score(0, sorted(d, reverse=True))
            self.statement = f"{self.name} has a high of {list(self.digit_dict.keys())[list(self.digit_dict.values()).index(sorted(d, reverse=True)[0])]}"
            self.score = result
            return


    def reset(self):
        self.is_fold = False
        self.hand = []
        self.statement = ''
        self.score = 0
        return