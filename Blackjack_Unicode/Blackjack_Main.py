#1. MAKE ALL THE FEATURES for the player such as update score
# see if the current hand or all hands are already lost or bust, update chips
# as functions within the class
# 2. We do not need to pass deck1 everytime if we do p1.deck = deck1 and d1.deck1=deck1
# it will be fine. Also look a class inheritence
# If we make a class table with moves, and have table.players = p1, it will be better
#4. Think about the dealer being a player as well
# 3. Modify split to include multiple splits

import random
from Cards_unicode import Deck
from PlayerTypes_Unicode import Player,Dealer
from TableandMoves_unicode import Table

#############Print Rules##################        
def PrintRules():
    print('\n'+'x'*80)   
    print(' Most Blackjack Rules Apply, Some rules vary with casino and for this game are:') 
    print('\n1. Only One Deck Of Cards Allowed')
    print('\n2. Splitting is allowed 3'+ 'times')
    print('\n3. Second Card for the subsequent hand is dealt only after earlier hand stops playing')
    print('\n4. NO BLACK JACK AFTER SPLITTING')
    print('\n5. Maximum number of hits per hand are 5 (including the deal hits)')
    print('\n6. You can surrender on the first move only, and will loose 50 %')
    print('\n'+'x'*80)

PrintRules()
########SET UP TABLE##

def SetupTable(chips):
    ''' This function initializes the player object, the dealer object,
    deck object and the table object'''
    p1=Player(float(chips))
    d1=Dealer()
    deck1=Deck()
    t1=Table(p1,d1,deck1)
    return p1,t1,d1,deck1

### PLAY ###### 
p1,t1,d1,deck1 = SetupTable(100)
while p1.chips>=1 and t1.tableStatus.lower()!='q': # Loop exits if player bankrupt or says quit
    print('Total number of chips-->' + str(p1.chips))
    t1.tableStatus=raw_input(p1.PrintValidMoves())
    if t1.tableStatus.lower() in p1.ValidMoves():          
        if t1.tableStatus.lower()=='d':
            # Player now starts playing and the index of his playing hand is 0
            p1.current_hand+=1 
            result=t1.Deal()  
            if result == True:
                while True and p1.current_hand+1<=len(p1.hands): 
                    '''The loop will not run if we have analyzed all player 
                    hands: i.e. the index of the playing hand exceeds the length 
                    of the hands'''
                    if p1.ValidMoves()=='Maximum number of hits reached':
                        t1.tableStatus='s'
                    else:
                        t1.tableStatus=raw_input(p1.PrintValidMoves())

                    if t1.tableStatus.lower() in p1.ValidMoves():          
                        if t1.tableStatus.lower()=='u': # u is for surrender
                            result=t1.Surrender()
                            if result == False:
                                break
                        if t1.tableStatus.lower()=='h': # h is for hit
                            result = t1.hit()
                            if result == False:
                                break
                        if t1.tableStatus.lower()=='p': # p is for split
                            result = t1.split()
                            if result == False:
                                break
                        if t1.tableStatus.lower()=='s': # s is for stand
                            p1.handstatus[p1.current_hand]='On Stand'
                            result=t1.StandCurrentHand()
                            if result == False:
                                break              
        elif t1.tableStatus.lower()=='q':
            break
   
    if p1.chips<1 :
        a=raw_input('You are out of chips, Do you want to buy 100 more chips (Y or any key for no) ?')
        if a.lower()=='y':
            p1.chips+=100
    p1,t1,d1,deck1 = SetupTable(p1.chips)
