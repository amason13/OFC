# -*- coding: utf-8 -*-

'''
Author: amason13
General functions needed for aspects of pofc
'''
from treys import Evaluator, Card
from copy import deepcopy
import numpy as np


evaluator = Evaluator()

def split_by_rank(cards):
    
    aces = []
    kings = []
    queens = []
    jacks = []
    tens = []
    nines = []
    eights = []
    sevens = []
    sixes = []
    fives = []
    fours = []
    threes = []
    twos = []
    
    for card in cards:
        if Card.get_rank_int(card)==0:
            twos.append(card)
        elif Card.get_rank_int(card)==1:
            threes.append(card)
        elif Card.get_rank_int(card)==2:
            fours.append(card)
        elif Card.get_rank_int(card)==3:
            fives.append(card)
        elif Card.get_rank_int(card)==4:
            sixes.append(card)
        elif Card.get_rank_int(card)==5:
            sevens.append(card)
        elif Card.get_rank_int(card)==6:
            eights.append(card)
        elif Card.get_rank_int(card)==7:
            nines.append(card)
        elif Card.get_rank_int(card)==8:
            tens.append(card)
        elif Card.get_rank_int(card)==9:
            jacks.append(card)
        elif Card.get_rank_int(card)==10:
            queens.append(card)
        elif Card.get_rank_int(card)==11:
            kings.append(card)
        elif Card.get_rank_int(card)==12:
            aces.append(card)
        else:
            return 'Card rank ERROR'
        
    all_ranks = [aces,kings,queens,jacks,tens,nines,eights,sevens,sixes,fives,fours,threes,twos]
    
    rank_split = []
    
    for rank in all_ranks:
        if len(rank)>0:
            rank_split.append(rank)
    
    rank_split.sort(key=len, reverse=True)
    
    return rank_split
        
def split_by_suit(cards):
    
    spades = []
    hearts = []
    diamonds = []
    clubs = []
    
    for card in cards:
        if Card.get_suit_int(card)==1:
            spades.append(card)
        elif Card.get_suit_int(card)==2:
            hearts.append(card)
        elif Card.get_suit_int(card)==4:
            diamonds.append(card)
        elif Card.get_suit_int(card)==8:
            clubs.append(card)
        else:
            return 'Card suit ERROR'
        
    all_suits = [spades,hearts,diamonds,clubs]
    
    suit_split = []
    for suit in all_suits:
        if len(suit)>0:
            suit_split.append(suit)
    
    suit_split.sort(key=len, reverse=True)
    
    return suit_split

    
def get_max_rank(cards):
    max_rank = 0
    for c in cards:
        if Card.get_rank_int(c)>max_rank:
            max_rank=Card.get_rank_int(c)
    return max_rank


def get_min_rank(cards):
    min_rank = 0
    for c in cards:
        if Card.get_rank_int(c)<min_rank:
            min_rank=Card.get_rank_int(c)
    return min_rank
        

def top_royalties(cards):
    ranked_cards = split_by_rank(cards)
    top_roy=0
    if len(ranked_cards) == 1:
        top_roy += Card.get_rank_int(ranked_cards[0][0])+10
    elif len(ranked_cards) == 2:
        top_roy += Card.get_rank_int(ranked_cards[0][0])-3
    return top_roy
    
    
def score_players(player1,player2):
    
    top_rank1 = evaluator.evaluate(player1.top_hand,[])
    mid_rank1 = evaluator.evaluate(player1.middle_hand,[])
    bot_rank1 = evaluator.evaluate(player1.bottom_hand,[])
    
    top_rank2 = evaluator.evaluate(player2.top_hand,[])
    mid_rank2 = evaluator.evaluate(player2.middle_hand,[])
    bot_rank2 = evaluator.evaluate(player2.bottom_hand,[])
    
    # if both players foul
    if (not bot_rank1<=mid_rank1<top_rank1) and (not bot_rank2<=mid_rank2<=top_rank2):
        return (0,0)
        
    # if player 1 only fouls
    elif not bot_rank1<=mid_rank1<=top_rank1:
        r = player2.get_royalties()
        return (-6-r,6+r)
    
    # if player 2 only fouls
    elif not bot_rank2<=mid_rank2<=top_rank2:
        r = player1.get_royalties()
        return (6+r,-6-r)
    
    # if neither player fouls    
    else:
        r1 = player1.get_royalties()
        r2 = player2.get_royalties()
        
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
            dummy_top1 = [player1.top_hand[0],player1.top_hand[1],player1.top_hand[2]]
            dummy_top2 = [player2.top_hand[0],player2.top_hand[1],player2.top_hand[2]]
            ranked1 = split_by_rank(dummy_top1)
            ranked2 = split_by_rank(dummy_top2)
            
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

    
  
def try_remove(myelement, mylist):
    if myelement in mylist:
        mylist.remove(myelement)

        
def normalise_rank_5(rank):
    nor = (7462-rank)/7462
    return nor

def normalise_rank_3(rank):
    nor = (7462-rank)/5787
    return nor  



def state_value_estimator(player1, player2, deck):
    # number of iterations
    n=10000
    
    score = 0


    for i in range(n):
        # make a copy of the remaining deck and shuffle
        dummy = deepcopy(deck)
        dummy.reshuffle()
        
        # make a copy of each player
        dummyp1 = deepcopy(player1)
        dummyp2 = deepcopy(player2)
        
        # randomly fill up hands
        while len(dummyp1.top_hand)<3:
            dummyp1.top_hand.append(dummy.draw(1))
        while len(dummyp1.middle_hand)<5:
            dummyp1.middle_hand.append(dummy.draw(1))
        while len(dummyp1.bottom_hand)<5:
            dummyp1.bottom_hand.append(dummy.draw(1))
               
        while len(dummyp2.top_hand)<3:
            dummyp2.top_hand.append(dummy.draw(1))
        while len(dummyp2.middle_hand)<5:
            dummyp2.middle_hand.append(dummy.draw(1))
        while len(dummyp2.bottom_hand)<5:
            dummyp2.bottom_hand.append(dummy.draw(1))
                   
        s = score_players(dummyp1,dummyp2)
        score += s
        
    #average scores and ranks
    av_score = score/n
    
        
    return av_score

                
def players_to_board(player1,player2):
    
    full_deck = []

    for suit, val in Card.CHAR_SUIT_TO_INT_SUIT.items():
        for rank in Card.STR_RANKS:
                    full_deck.append(Card.new(rank + suit))
    
    board = np.zeros(52)
    
    for card in player1.top_hand:
        board[full_deck.index(card)] = 1
        
    for card in player1.middle_hand:
        board[full_deck.index(card)] = 2
        
    for card in player1.bottom_hand:
        board[full_deck.index(card)] = 3

    for card in player1.discards:
        board[full_deck.index(card)] = 4
        
    for card in player1.dealt_cards:
        board[full_deck.index(card)] = 5
    
    for card in player2.top_hand:
        board[full_deck.index(card)] = -1
        
    for card in player2.middle_hand:
        board[full_deck.index(card)] = -2
        
    for card in player2.bottom_hand:
        board[full_deck.index(card)] = -3

#    for card in player2.discards:
#        board[full_deck.index(card)] = -4

#    for card in player2.dealt_cards:
#        board[full_deck.index(card)] = -5
    

    return np.array(board)



def board_to_players(board,player1,player2):
    player1.reset()
    player2.reset()
    board = list(board)
    unseen = []
    full_deck = []

    for suit, val in Card.CHAR_SUIT_TO_INT_SUIT.items():
        for rank in Card.STR_RANKS:
                    full_deck.append(Card.new(rank + suit))
    
    BOARD_TO_HAND = {0:unseen,
                     1:player1.top_hand,
                     2:player1.middle_hand,
                     3:player1.bottom_hand,
                     4:player1.discards,
                     5:player1.dealt_cards,
                     -1:player2.top_hand,
                     -2:player2.middle_hand,
                     -3:player2.bottom_hand,
                     -4:player2.discards,
                     -5:player2.dealt_cards}
    
    for i in range(52):
        BOARD_TO_HAND[board[i]].append(full_deck[i])
        
    board = np.array(board)
    
    


