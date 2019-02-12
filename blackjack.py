# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0


# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        ans = "Hand contains"
        for i in range(0, len(self.cards)):
            ans += " " + str(self.cards[i])
        return ans

    def add_card(self, card):
        self.cards.append(card)	# add a card object to a hand

    def get_value(self):
        hand_value = 0
        aces = 0
        for j in self.cards:
            hand_value += VALUES[str(j)[1]]
            if str(j)[1] == "A":
                aces += 1
        if aces == 0:
            return hand_value
        else:
            if hand_value + 10 <= 21:
                return hand_value + 10
            else:
                return hand_value
        
    def draw(self, canvas, pos):
        for k in range(0, len(self.cards)):
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(str(self.cards[k])[1]), 
                        CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(str(self.cards[k])[0]))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + k * (50 + CARD_CENTER[0]), pos[1] + CARD_CENTER[1]], CARD_SIZE)
        

# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        self.deal = ""
        for i in SUITS:
            for j in RANKS:
                self.deck.append(str(Card(i, j)))

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        self.deal = self.deck.pop()
        return Card(self.deal[0], self.deal[1])
    
    def __str__(self):
        ans = "Deck contains"
        for i in self.deck:
            ans += " " + i
        return ans
        # return str(self.deal)	# return a string representing the deck


#define event handlers for buttons
def deal():
    global outcome, in_play, deck, new_player, dealer
    
    deck = Deck() 
    new_player = Hand()
    dealer = Hand()
    outcome = ""

    # your code goes here
    deck.shuffle()
    p1 = deck.deal_card()
    new_player.add_card(p1)
    
    d1= deck.deal_card()
    dealer.add_card(d1)
    
    p2 = deck.deal_card()
    new_player.add_card(p2)
    
    d2 = deck.deal_card()
    dealer.add_card(d2)
        
    in_play = True
def hit():
    global outcome, in_play, score, new_player
    # if the hand is in play, hit the player
    if new_player.get_value() <= 21:
        p3 = deck.deal_card()
        new_player.add_card(p3)
    
    # if busted, assign a message to outcome, update in_play and score
    if new_player.get_value() > 21:
        out_come = "You have busted"
        in_play = False
        score -= 1
        
def stand():
    global in_play, score, outcome
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    while(in_play == True and dealer.get_value() < 17):
        d3 = deck.deal_card()
        dealer.add_card(d3)
        
    # assign a message to outcome, update in_play and score
    if dealer.get_value() > 21:
        outcome = "The dealer busted"
        in_play = False
        score += 1
    else:
        if dealer.get_value() >= new_player.get_value():
            outcome = "You lose"
            in_play = False
            score -= 1
        else:
            outcome = "You win"
            in_play = False
            score += 1

# draw handler    
def draw(canvas):
    global score, outcome, new_player, dealer
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("Blackjack", (100, 100), 50, "Aqua")
    canvas.draw_text(outcome, (300, 150), 30, "Black")
    canvas.draw_text("score " + str(score), (400, 100), 30, "Black")
    canvas.draw_text("Dealer", (70, 150), 30, "Black")
    canvas.draw_text("Player", (70, 350), 30, "Black")
    
    new_player.draw(canvas, [100, 400])
    dealer.draw(canvas, [100, 200])
    if in_play == True:
        canvas.draw_image(card_back, (108, 48), CARD_SIZE, (100, 248), CARD_SIZE)
        canvas.draw_text("Hit or Stand", (300, 350), 30, "Black")
    else:
        canvas.draw_text("New Deal?", (300, 350), 30, "Black")

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric