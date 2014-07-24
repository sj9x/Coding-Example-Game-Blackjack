### THESE FUNCTIONS ARE CALLED TO INITILIAZE THE SCREEN AND CLEAR SCREEN
import curses

##############################################################
def PrintRules(screen):
    '''Prints rules'''
    screen.addstr(0,0, 'Most Blackjack Rules Apply, Some rules vary with casino and for this game are:'+
    '\n1. Only One Deck Of Cards Allowed'+
    '\n2. Splitting is allowed is 3 times, NO BLACK JACK AFTER SPLITTING'+
    '\n3. Second Card for the subsequent hand is dealt only after earlier hand'+
    '\n4. Maximum number of hits per hand are 4'+
    '\n5. You can surrender on the first move only, and will loose 50 %'+
    '\n  DICTIONARY FOR SCORE DISPLAY:'+
    '\n: (S): Spades, (H): Hearts. (D): Diamonds, (C): Clubs'+
    '\n: For multiple score possibility, the scores are represented as [s1,s2,..]'+
    '\n'+'='*100,curses.A_DIM)  
    screen.addstr(12,0,'\n') 
    
######################## Initiate Screen#####################
def Screen_Initiate():    
    '''Initiates the variable screen and calls Print Rules'''
    screen=curses.initscr()
    curses.start_color()
    screen.addstr(0,0,'\n'+'x'*100)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    screen.bkgd(' ', curses.color_pair(1))
    PrintRules(screen)
    return screen

def ClearScreen(screen):
    '''Clears all the screen beneath the rules'''
    screen.move(10,0)
    screen.clrtobot()
    screen.refresh()
    
def CloseScreen():
    '''Closes the screen'''
    curses.endwin()
    
#### INITIALIZE TABLE AND PLAYERS ################
