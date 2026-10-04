import random as r
import os
#import card_counting
import time
print("Welcome to the wonderful game of blackjack. The controls for this game will be as follows\n\n"
  "To hit for a card you will type 'h'\n" 
"When you are satisfied with what you got use 's' to stay\n"
"\n"
"We will being giving you a great hand now, you better play it well!\n\n")

nmbr_of_same_cards = 4
#Start of global variables
cards = []
cards_left = 13*nmbr_of_same_cards
#End of global variables
true_count = 0

def card_counting(hand_1, hand_2):
  global true_count
  
  list = hand_1 + hand_2

  for element in list:
    if element >= 10 or element == 1: 
      true_count -= 1
    elif 2<= element <= 6:
      true_count += 1
    

def create_deck(cards):
  """Creates a deck to use and all you will need to create the deck is an emtpy list.
  
      What this ends up doing is making a list all Ace to King cards. An element in cards will have two values associated with it. [0] will be the card number. And [1] will be the amount of the card."""
  for i in range (1,13+1):
    cards.append([i,nmbr_of_same_cards])
  return cards


def deal(hand):
  """This function is used for dealing any hand. You will only need to in their hand as the argument. This function will also reset if the delaer runs out."""
  global cards
  global cards_left
  global true_count
  if cards_left <=0: 
    cards.clear()
    cards = create_deck(cards)
    cards_left = 13*nmbr_of_same_cards
    true_count = 0
    print("I had to shuffle in a new deck for ya.")
  
  index = r.randint(0,12)
  while (cards[index][1] <= 0) :
    index = r.randint(0,12)
  hand.append(cards[index][0])
  cards[index][1] -= 1
  cards_left -= 1
  if len(hand) <= 1:#Draws two cards for the start of every new hand
    deal(hand)
  return hand

def user_hit(user_hand):
  """Combines the the deal() funtion with the hand_display() funtion and is specific for readibility"""
  user_hand = deal(user_hand)
  hand_display(user_hand)
  return user_hand

def dealer_hit(dealer_hand,bool):
  """This only happens once apparently"""
  #if sum_of_hand(dealer_hand) < 17: dealer_hand = deal(dealer_hand) //For some reason I thouhgt the dealer delt with the person
  if bool: dealer_hand = deal(dealer_hand)
  hand_display(dealer_hand, 1)
  return dealer_hand



def hand_display(cards_list, variation=0):
  """The first parameter in this list here is to show either the dealers hand and the second parameter is boolean like. 0 = player_deal , 1 = dealer_deal , 2 = is used for the end when you either win or lose. """
  if (variation == 0): print("your hand:", end=" ")
  if (variation == 1 or variation == 2): print("dealers hand:", end = " ")
  for element in cards_list:
    if (variation == 0 or variation == 2):
      if (1 < element <= 10):
        print(element, end =" ")
      elif (element == 1):
        print("A", end = " ")
      elif (element == 11):
        print("J", end = " ")
      elif (element == 12):
        print("Q", end = " ")
      elif (element == 13):
        print("K", end = " ")
    else:
      print("X", end=" ")
      variation = 0
  print("\n")
  return None


def sum_of_hand(hand):
  """Used to dertimine the sum on any hand, and will revert an Ace to a 1 if it would set you over 21."""
  sum = 0
  ace = 0
  for element in hand:
    if (1 < element <= 10):
      sum += element
      
    elif (element > 10):
      sum += 10
      
    elif (element == 1):
      sum += 11
      ace += 1
  while (sum > 21 and ace):#If ace makes you go over 21 it changes it to a 1
    sum -= 10
    ace -= 1

    
  return sum

def win_or_lose(user_hand, dealer_hand, money, bet):
  """This function will set up the win window, and will get the dealer up to 17 if he hasn't gotten up to there yet. This returns a boolean which is used to increment the win_counter"""
  global true_count
  hand_display(user_hand)
  while sum_of_hand(dealer_hand) < 17:
    dealer_hand = deal(dealer_hand)
  hand_display(dealer_hand, 2)
  card_counting(user_hand, dealer_hand)
  print("Card count", true_count)
  bool = False
  
  if sum_of_hand(dealer_hand) * (sum_of_hand(dealer_hand) <= 21) < sum_of_hand(user_hand) <= 21: bool = True
    
  if bool:
    money += bet*2
    print("You win!!!!\n")
  else: 
    money -= bet
    print("Better luck next time...\n")
  return money

def restart(money):
  """Clears both the players and the dealers hand, and this returns the amount of game_played + 1"""
  global dealer_bool
  user_hand.clear()
  dealer_hand.clear()
  dealer_bool = True
  if money > 0: 
    try:
        bet = int(input(f"You have ${money} how much do you want to bet?: "))
        while not(bet <= money):
          bet = int(input(f"Please input a number > or = {money}: "))
    except:
      bet = 0
  else: bet = 0

  return bet


user_hand = []
dealer_hand = []

games_played = 0
win_count = 0
play_again = ""
h_or_s = ""

money = 100
bet = restart(money)

cards = create_deck(cards)
dealer_bool = True
while (play_again == "") and money > 0:
  if h_or_s.upper() == "S":#staying
    win_count += 1 
    
    money = win_or_lose(user_hand, dealer_hand, money, bet)

    games_played += 1
  
    bet = restart(money)
    print(f"You have played {games_played} times! and won {win_count} times.\n")
    
    #play_again = input("Do you want to play again? 'press enter to play again'").upper()
    h_or_s = ""
    
  else:#else hit
    if sum_of_hand(user_hand) > 21: #if you lost
      money = win_or_lose(user_hand, dealer_hand,money, bet)
      
      games_played += 1
      bet = restart(money)
      print(f"You have played {games_played} times! and won {win_count} times.\n")
      
      #play_again = input("Do you want to play again? 'press enter to play again'").upper()
      
    else:#if you can still play
      user_hit(user_hand)
      dealer_hit(dealer_hand,dealer_bool)
      dealer_bool = False
      if (sum_of_hand(user_hand) <= 21): h_or_s = input("Hit or Stay?: ")#This is for if the user if the user ends up over 21. So it will ignore this and go back up to the top
  
  os.system("cls")

print("You're broke as shit XDDDDDD")
time.sleep(1)
  