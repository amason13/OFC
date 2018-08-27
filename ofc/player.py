''' 
Author: amason13
Player class for ofc
'''

from treys import Card, Evaluator
import itertools
import numpy as np
from ofc import methods

evaluator = Evaluator()

class Player:
    
    
    
    def __init__(self):
        
        self.dealt_cards = []
        self.top_hand = []
        self.middle_hand = []
        self.bottom_hand = []
        self.discards = []
        
        
    def reset(self):
        self.__init__()
        
        
    def is_misset(self):
        # bypass incomplete hands
        if (len(self.top_hand)<3) or (len(self.middle_hand)<5) or (len(self.bottom_hand)<5):
            return 0
        
        t = evaluator.evaluate(self.top_hand,[])
        m = evaluator.evaluate(self.middle_hand,[])
        b = evaluator.evaluate(self.bottom_hand,[])
        
        if not t >= m >= b:
            return 1
        else:
            return 0


    
    def is_fantasy(self):
        # bypass incomplete hands
        if (len(self.top_hand)<3) or (len(self.middle_hand)<5) or (len(self.bottom_hand)<5):
            return 0
        
        if self.is_misset == 1:    
            return 0
        else:
            if methods.top_royalties(self.top_hand) > 6:
                return 1    
            
            
    def get_royalties(self):
    
        top_rank = evaluator.evaluate(self.top_hand,[])
        mid_rank = evaluator.evaluate(self.middle_hand,[])
        bot_rank = evaluator.evaluate(self.bottom_hand,[])
        
        mid = evaluator.get_rank_class(mid_rank)
        bot = evaluator.get_rank_class(bot_rank)
        
        royalties = 0
        
        BOTTOM_RANK_TO_ROYALTY = {
            1: 15, # Straight flush
            2: 10, # Quads
            3: 6,  # Full house
            4: 4,  # Flush
            5: 2,  # Straight
            6: 0,  # Trips
            7: 0,  # 2 pair
            8: 0,  # Pair
            9: 0   # high card
        }
        
        MIDDLE_RANK_TO_ROYALTY = {
            1: 30, # Straight flush
            2: 20, # Quads
            3: 12, # Full house
            4: 8,  # Flush
            5: 4,  # Straight
            6: 2,  # Trips
            7: 0,  # 2 pair
            8: 0,  # Pair
            9: 0   # high card
        }
        
        # need to add royal flushes into here too
        if not bot_rank<=mid_rank<=top_rank: 
            royalties = 0
        elif mid_rank == 1:
            royalties += 75 + methods.top_royalties(self.top_hand)
        elif bot_rank ==1:
            royalties += 50 +MIDDLE_RANK_TO_ROYALTY[mid] + methods.top_royalties(self.top_hand)
        else:
            royalties += MIDDLE_RANK_TO_ROYALTY[mid] + BOTTOM_RANK_TO_ROYALTY[bot] + methods.top_royalties(self.top_hand)
       
        return royalties
        



    def set_fantasy(self):
        
        min_tot_rank = 0
        max_royalties = 0
        best_top = []
        best_mid = []
        best_bot = []
        
        bottomcombos = itertools.combinations(self.dealt_cards, 5)
          
        for bcombo in bottomcombos:
            
            remaining_cards = list(set(self.dealt_cards)-set(bcombo))
            middlecombos = itertools.combinations(remaining_cards,5)
            
            for mcombo in middlecombos:
                
                remaining_cards_2 = list(set(remaining_cards)-set(mcombo))
                topcombos = itertools.combinations(remaining_cards_2,3)
                
                
                for tcombo in topcombos:
                    
                    discard = list(set(remaining_cards_2)-set(tcombo))
                    
                    self.top_hand = tcombo
                    self.middle_hand = mcombo
                    self.bottom_hand = bcombo
                    self.discards = discard
                    
                    trank = evaluator.evaluate(self.top_hand,[])
                    mrank = evaluator.evaluate(self.middle_hand,[])
                    brank = evaluator.evaluate(self.bottom_hand,[])
                    
                    totrank = trank + mrank + brank
                    royalties = self.get_royalties()
                    
                    if royalties>max_royalties:
                        
                        max_royalties = royalties
                        best_top = self.top_hand
                        best_mid = self.middle_hand
                        best_bot = self.bottom_hand
                        discard = self.discards
                        min_tot_rank = totrank
                        
                    elif (royalties == max_royalties) and (royalties>0):
                        if totrank < min_tot_rank:
                            max_royalties = royalties
                            best_top = self.top_hand
                            best_mid = self.middle_hand
                            best_bot = self.bottom_hand
                            discard = self.discards
                            min_tot_rank = totrank
                        
                        
        self.top_hand = best_top
        self.middle_hand = best_mid
        self.bottom_hand = best_bot
        self.discards = discard
        self.dealt_cards =  []
    
    def is_still_fantasy(self):
        
        mid_rank = evaluator.evaluate(self.middle_hand,[])
        bot_rank = evaluator.evaluate(self.bottom_hand,[])
        
        mid = evaluator.get_rank_class(mid_rank)
        bot = evaluator.get_rank_class(bot_rank)
        
        BOTTOM_RANK_TO_ROYALTY = {
            1: 15, # Straight flush
            2: 10, # Quads
            3: 6,  # Full house
            4: 4,  # Flush
            5: 2,  # Straight
            6: 0,  # Trips
            7: 0,  # 2 pair
            8: 0,  # Pair
            9: 0   # high card
        }
        
        MIDDLE_RANK_TO_ROYALTY = {
            1: 30, # Straight flush
            2: 20, # Quads
            3: 12, # Full house
            4: 8,  # Flush
            5: 4,  # Straight
            6: 2,  # Trips
            7: 0,  # 2 pair
            8: 0,  # Pair
            9: 0   # high card
        }
        
        if (methods.top_royalties(self.top_hand)>9) or (MIDDLE_RANK_TO_ROYALTY[mid]>9) or (BOTTOM_RANK_TO_ROYALTY[bot]>9):
            return 1
        else:
            return 0
    
    
    
    def display_hand(self):
        print("Top:")
        print(Card.print_pretty_cards(self.top_hand))
        print("Middle:")
        print(Card.print_pretty_cards(self.middle_hand))
        print("Bottom:")
        print(Card.print_pretty_cards(self.bottom_hand))


    def get_available_actions(self):
        T=self.top_hand
        M=self.middle_hand
        B=self.bottom_hand
            
        if len(self.dealt_cards)==5:
            
            return np.ones(232)
        
        elif len(self.dealt_cards)==3:
            pass # need to add the logic for pinapple here
        
        elif len(self.dealt_cards)==2:
            pass # need to add the logic for 2 card draw version
    
        else:
            t,m,b = 0,0,0
            
            if len(T)<3:
                t = 1
            
            if len(M)<5:
                m = 1
                
            if len(B)<5:
                b = 1     
            
        return np.array([t,m,b]) 
   
    def hand_is_empty(self):
        
        if not (self.top_hand==[]) and (self.middle_hand==[]) and (self.bottom_hand==[]) and (self.discards==[]):
            return 0
        else:
            return 1

    def hand_is_full(self):
        
        if not (len(self.top_hand)==3) and (len(self.middle_hand)==5) and (len(self.bottom_hand)==5) and (len(self.discards)==3):
            return 0
        else:
            return 1
        
        
        
    def score_hand(self, opponent):
    
        top_rank1 = evaluator.evaluate(self.top_hand,[])
        mid_rank1 = evaluator.evaluate(self.middle_hand,[])
        bot_rank1 = evaluator.evaluate(self.bottom_hand,[])
        
        top_rank2 = evaluator.evaluate(opponent.top_hand,[])
        mid_rank2 = evaluator.evaluate(opponent.middle_hand,[])
        bot_rank2 = evaluator.evaluate(opponent.bottom_hand,[])
        
        # if both players foul
        if (not bot_rank1<=mid_rank1<top_rank1) and (not bot_rank2<=mid_rank2<=top_rank2):
            return (0,0)
            
        # if player 1 only fouls
        elif not bot_rank1<=mid_rank1<=top_rank1:
            r = opponent.get_royalties()
            return (-6-r,6+r)
        
        # if player 2 only fouls
        elif not bot_rank2<=mid_rank2<=top_rank2:
            r = self.get_royalties()
            return (6+r,-6-r)
        
        # if neither player fouls    
        else:
            r1 = self.get_royalties()
            r2 = opponent.get_royalties()
            
            # bottom hand
            if bot_rank1<bot_rank2:
                bs = 1
            elif bot_rank1 == bot_rank2:
                bs = 0
            else: bs = -1
            # middle hand
            if mid_rank1<mid_rank2:
                ms = 1
            elif mid_rank1 == mid_rank2:
                ms = 0
            else: ms = -1
            # top hand
            if top_rank1<top_rank2:
                ts = 1
            elif top_rank1>top_rank2:
                ts = -1
                
            # the folowing should take care of the 3-to-5 card mapping being many-to-one
            else:
                dummy_top1 = [self.top_hand[0],self.top_hand[1],self.top_hand[2]]
                dummy_top2 = [opponent.top_hand[0],opponent.top_hand[1],opponent.top_hand[2]]
                ranked1 = methods.split_by_rank(dummy_top1)
                ranked2 = methods.split_by_rank(dummy_top2)
                
                if len(ranked1[0]) == 2: # for pairs
                    if Card.get_rank_int(ranked1[1][0]) == Card.get_rank_int(ranked2[1][0]):
                        ts = 0
                    elif Card.get_rank_int(ranked1[1][0]) > Card.get_rank_int(ranked2[1][0]):
                        ts = 1
                    else:
                        ts = -1
                        
                else:   # for high cards
                    if Card.get_rank_int(ranked1[0][0]) > Card.get_rank_int(ranked2[0][0]):
                        ts = 1
                    elif Card.get_rank_int(ranked1[0][0]) < Card.get_rank_int(ranked2[0][0]):
                        ts = -1
                    else:
                        if Card.get_rank_int(ranked1[1][0]) > Card.get_rank_int(ranked2[1][0]):
                            ts = 1
                        elif Card.get_rank_int(ranked1[1][0]) < Card.get_rank_int(ranked2[1][0]):
                            ts = -1
                        else:
                            if Card.get_rank_int(ranked1[2][0]) > Card.get_rank_int(ranked2[2][0]):
                                ts = 1
                            elif Card.get_rank_int(ranked1[2][0]) < Card.get_rank_int(ranked2[2][0]):
                                ts = -1
                            else:
                                ts = 0
                    
            
            # calculate sum of individual score
            s = bs + ms +ts
            
            # double score if player wins all three hands (as per POFC scoring rules)
            if s % 3 == 0:
                s = 2*s
            
            # calculate player1 score by adding difference of royalties
            s = s + r1 - r2
            
            return s
        
    def players_to_board(self,opponent):
    
        full_deck = []
    
        for suit, val in Card.CHAR_SUIT_TO_INT_SUIT.items():
            for rank in Card.STR_RANKS:
                        full_deck.append(Card.new(rank + suit))
        
        board = np.zeros(52)
        
        for card in self.top_hand:
            board[full_deck.index(card)] = 1
            
        for card in self.middle_hand:
            board[full_deck.index(card)] = 2
            
        for card in self.bottom_hand:
            board[full_deck.index(card)] = 3
    
        for card in self.discards:
            board[full_deck.index(card)] = 4
            
        for card in self.dealt_cards:
            board[full_deck.index(card)] = 5
        
        for card in opponent.top_hand:
            board[full_deck.index(card)] = -1
            
        for card in opponent.middle_hand:
            board[full_deck.index(card)] = -2
            
        for card in opponent.bottom_hand:
            board[full_deck.index(card)] = -3
    
        for card in opponent.discards:
            board[full_deck.index(card)] = -4
    
    #    for card in opponent.dealt_cards:
    #        board[full_deck.index(card)] = -5
        
    
        return np.array(board)
        
        
##########################################################
'''    
    def place_5_cards(self, dealt_cards):
        
        hand_rank = evaluator.evaluate(dealt_cards,[])
        ranked_cards = split_by_rank(dealt_cards)
        suited_cards = split_by_suit(dealt_cards)
        
        # if 4 of a kind 
        if evaluator.get_rank_class(hand_rank)==2: 
            
            # assign those 4 cards to bottom hand
            self.bottom_hand.append(ranked_cards[0])
            
            # place 5th card according to its rank
            if Card.get_rank_int(ranked_cards[1])>8:
                self.top_hand.append(ranked_cards[1])
            elif Card.get_rank_int(ranked_cards[1])>3:
                self.middle_hand.append(ranked_cards[1])
            else:
                self.bottom_hand.append(ranked_cards[1])
               
        # if straight or better, but not 4 of a kind       
        elif evaluator.get_rank_class(hand_rank)<6:
            self.bottom_hand.append(dealt_cards)
        
        # if three of a kind 
        elif evaluator.get_rank_class(hand_rank)==6:
            self.bottom_hand.append(ranked_cards[0])
            
            # if remaining 2 cards are two of {A,K,Q} place highest in middle and lowest in top
            if Card.get_rank_int(ranked_cards[1])>9 and Card.get_rank_int(ranked_cards[2])>9:
                self.middle_hand.append(ranked_cards[1])
                self.top_hand.append(ranked_cards[2])
            
            # else if other 2 cards are suited, place in middle.
            elif Card.get_suit_int(ranked_cards[1])==Card.get_suit_int(ranked_cards[2]):
                self.middle_hand.append(ranked_cards[1])
                self.middle_hand.append(ranked_cards[2])
                
            # if Queen or better, put at the top.
            elif Card.get_rank_int(ranked_cards[1]) > 9:
                self.top_hand.append(ranked_cards[1])
                self.middle_hand.append(ranked_cards[2])
                
            # as above - not 100% sure this is necessary as it may be included within other conditionals.
            elif Card.get_rank_int(ranked_cards[2])>9:
                self.top_hand.append(ranked_cards[2])
                self.middle_hand.append(ranked_cards[1])
            
            # if remaining 2 card ranks differ by at most 2
            elif abs(Card.get_rank_int(ranked_cards[1])-Card.get_rank_int(ranked_cards[2]))<3:
                self.middle_hand.append(ranked_cards[1])
                self.middle_hand.append(ranked_cards[2])
            
            # otherwise
            else:
                self.middle_hand.append(ranked_cards[1,2])
        
        # if two pair
        elif evaluator.get_rank_class(hand_rank)==7:
            self.bottom_hand.append(ranked_cards[0])
            # if Queen or better: top, else: middle
            if Card.get_rank_int(ranked_cards[1]) > 9:
                self.top_hand.append(ranked_cards[1])
            else:
                self.middle_hand.append(ranked_cards[1])
        
        # if 1 pair, 3 flush. 3 bottom, mid pair middle, QQ+ top. 
        # if 1 pair 2 flush...
            
        # if 1 pair or worse
        else:
            # if 4 to a flush, place at bottom
            if len(suited_cards[0]) == 4:
                self.bottom_hand.append(suited_cards[0])
                # if Queen or better: top, else: middle
                if Card.get_rank_int(ranked_cards[1]) > 9:
                    self.top_hand.append(ranked_cards[1])
                else:
                    self.middle_hand.append(ranked_cards[1])
            
            # if 4 to a straight with 2 cards to complete straight
            elif 
                    
            # if 3 to a flush 
            elif len(suited_cards[0]) == 3 and len(suited_cards[1])==2:
                if suited_cards[1][0]=
                # if remaining are 2 flush
                elif len(suited_cards[1])==2:
                    if get_max_rank(suited_cards[0])
                    
            
            
            
            if evaluator.get_rank_class(hand_rank)==8:
            
 '''     
