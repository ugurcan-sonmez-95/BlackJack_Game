### BlackJack Game ### 

from random import shuffle

# Firstly, create suits, ranks and values of cards
suits = ('Hearts', 'Spades', 'Diamonds', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Queen', 'Jack', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Queen':10, 'Jack':10, 'King':10, 'Ace':11}

# Create a variable for checking whether the game is on
game = True

# Create a Card class
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    def __str__(self):
        return (self.rank+' of '+self.suit)

# Create a Deck class
class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))
    def shuffleDeck(self):
        shuffle(self.deck)
    def draw_card(self):
        return self.deck.pop()

# Create a Hand class
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if (card.rank == 'Ace'):
            self.aces += 1
    def exception_for_ace(self):
        while ((self.value > 21) and (self.aces)):
            self.value -= 10
            self.aces -= 1

# Create a Chips class
class Chips:
    def __init__(self, balance=100):
        self.balance = balance
        self.bet = 0
    def win_bet(self):
        self.balance += self.bet
    def lose_bet(self):
        self.balance -= self.bet

# Create a function to get input correctly for betting
def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("\nHow many chips would you like to bet?: "))
        except ValueError:
            print("Sorry, you did not enter an integer. Please try again.")
        else:
            if (chips.bet > chips.balance):
                print("Sorry, the bet amount exceeds your balance.")
            else:
                break

# Create a function for Player to draw card
def hit(deck, hand):
    hand.add_card(deck.draw_card())
    hand.exception_for_ace()

# Create a function to give Player 'hit' and 'stand' options
def hit_or_stand(deck, hand):
    global game
    while True:
        ans = input("\nWould you like to Hit or Stand? Enter 'h' or 's': ")
        if (ans[0].lower() == 'h'):
            hit(deck, hand)
        elif (ans[0].lower() == 's'):
            print("\nPlayer has decided to stand. Dealer's turn!")
            game = False
        else:
            print("\nSorry, you have entered wrong. Please try again.")
            continue
        break

# Create a function to show first two cards of Player and Dealer
def show_first_cards(player, dealer):
    print("Dealer's Hand:")
    print("<hidden card>")
    print(dealer.cards[1], '\n')
    print("Player's Hand:")
    for card in player.cards:
        print(card)

# Create a function to show all cards of Player and Dealer
def show_all_cards(player, dealer):
    print("Dealer's Hand:")
    for card in dealer.cards:
        print(card)
    print("Dealer's Value =", dealer.value, '\n')
    print("Player's Hand:")
    for card in player.cards:
        print(card)
    print("Player's Value =", player.value)

# Create functions to control win-lose, bust and tie game situations
def player_bust(player, dealer, chips):
    print("\nPlayer busted!")
    chips.lose_bet()

def player_win(player, dealer, chips):
    print("\nPlayer wins!")
    chips.win_bet()

def dealer_bust(player, dealer, chips):
    print("\nDealer busted!")
    chips.win_bet()

def dealer_win(player, dealer, chips):
    print("\nDealer wins!")
    chips.lose_bet()

def tie_game(player, dealer):
    print("\nIt is a tie!")

# Create Player's chips (it is set to 100 as default)
player_chips = Chips()

# Game phase
while True:
    print("\nWelcome to BlackJack! GOOD LUCK!")
    # Create the deck and shuffle it
    deck = Deck()
    deck.shuffleDeck()
    # Create Player's hand and draw the first cards
    player_hand = Hand()
    player_hand.add_card(deck.draw_card())
    player_hand.add_card(deck.draw_card())
    # Create Dealer's hand and draw the first cards
    dealer_hand = Hand()
    dealer_hand.add_card(deck.draw_card())
    dealer_hand.add_card(deck.draw_card())
    # Get the input for bet correctly and show the first two cards of Player and Dealer
    take_bet(player_chips)
    show_first_cards(player_hand, dealer_hand)
    # After Player plays his/her first turn, check whether the value of Player's hand > 21 
    while game:
        hit_or_stand(deck, player_hand)
        if (player_hand.value > 21):
            show_all_cards(player_hand, dealer_hand)
            player_bust(player_hand, dealer_hand, player_chips)
            break
        else:
            show_all_cards(player_hand, dealer_hand)
    # (If the value is not > 21) After Player stands, Dealer hits until reaching the value of 17 at least.
    # Then, check the win-lose or tie game situations 
    if (player_hand.value <= 21): 
        while (dealer_hand.value < 17):
            hit(deck, dealer_hand)
        print("\nAfter Dealer hits or stands:")
        show_all_cards(player_hand, dealer_hand)
        if (dealer_hand.value > 21):
            dealer_bust(player_hand, dealer_hand, player_chips)
        elif (dealer_hand.value > player_hand.value):
            dealer_win(player_hand, dealer_hand, player_chips)
        elif (dealer_hand.value < player_hand.value):
            player_win(player_hand, dealer_hand, player_chips)
        else:
            tie_game(player_hand, dealer_hand)

    print(f"\nPlayer's balance: {player_chips.balance}")
    new_game = input("\nWould you like to play again? Enter 'y' or 'n': ")
    if (new_game[0].lower() == 'y'):
        game = True
        if (player_chips.balance == 0):
            player_chips = Chips()
        continue
    else:
        print("\nThanks for playing!\n")
        break