#1. MAKE ALL THE FEATURES for the player such as update score
# see if the current hand or all hands are already lost or bust, update chips
# as functions within the class
# 2. We do not need to pass deck1 everytime if we do p1.deck = deck1 and d1.deck1=deck1
# it will be fine. Also look a class inheritence
# If we make a class table with moves, and have table.players = p1, it will be better
#4. Think about the dealer being a player as well
# 3. Modify split to include multiple splits


import curses
from Cards import Deck
from PlayerTypes import Player,Dealer
from TableandMoves import Table
from ScreenFunctions import*
#import moves


########SET UP TABLE##

def SetupTable(chips):
    ''' This function initializes the player object, the dealer object,
    deck object and the table object and Prints RULES ON THE SCREEN'''
    p1=Player(float(chips))
    d1=Dealer()
    deck1=Deck()
    screen=curses.initscr()
    t1=Table(p1,d1,deck1,screen)
    PrintRules(screen)
    return p1,t1,d1,deck1,screen

### PLAY ###### 
p1,t1,d1,deck1,screen = SetupTable(100)

while p1.chips>=1 and t1.tableStatus.lower()!='q': # The loop stops if player has no chips or quits
    ClearScreen(screen) # Clears the whole screen below the rules
    screen.addstr('\nTotal number of chips-->' + str(p1.chips))
    screen.addstr('\n'+p1.PrintValidMoves())
    t1.tableStatus=screen.getstr() 
    if t1.tableStatus.lower() in p1.ValidMoves():          
        if t1.tableStatus.lower()=='d':
            p1.current_hand+=1
            result=t1.Deal()  
            if result == True:
                while True and p1.current_hand+1<=len(p1.hands):
                    if p1.ValidMoves()=='Maximum number of hits reached':
                        # If maximum number of hits reached, put the current + 1 hand on stand
                        t1.tableStatus='s'
                    else:
                        screen.addstr(16,0,'\n'+p1.PrintValidMoves())
                        t1.tableStatus=screen.getstr() 
                    if t1.tableStatus.lower() in p1.ValidMoves():          
                        if t1.tableStatus.lower()=='u':# u is surrender
                            result=t1.Surrender()
                            if result == False:
                                break
                        if t1.tableStatus.lower()=='h': # h is hit
                            result = t1.hit()
                            if result == False:
                                break
                        if t1.tableStatus.lower()=='p': # p is split
                            result = t1.split()
                            if result == False:
                                break
                        if t1.tableStatus.lower()=='s': # s is stand
                            p1.handstatus[p1.current_hand]='On Stand'
                            result=t1.StandCurrentHand()
                            if result == False:
                                break              
        elif t1.tableStatus.lower()=='q':
            break
   
    if p1.chips<1 :
        screen.addstr('You are out of chips, Do you want to buy 100 more chips (Y or any key for no) ?')
        a=screen.getstr()
        if a.lower()=='y':
            p1.chips+=100
    p1,t1,d1,deck1,screen = SetupTable(p1.chips)
   
## CLOSE THE TERMINAL     
CloseScreen()