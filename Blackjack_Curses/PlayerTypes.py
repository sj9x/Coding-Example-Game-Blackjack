### THIS FILE CONTAINS THE CLASS DEALER AND THE PLAYER, THEY ARE VERY SIMILAR

class Player(object):
    '''Atrributes of the player, which are his 1. hands: List of list of cards in 
    each hand, 2. score for each hand, 3. handstatus, i.e. playing, Stand, Bust,
    Lost, Won, 4. chips: total number of chips 5. chisperhand: A list
    6. Current hand: Index of the hand that is currently playing (for split hands)
    and his valid moves'''
    def __init__(self,chips):
        self.hands=[[]]
        self.score=[[0]]
        self.handstatus=['Playing']
        self.chips=chips
        self.chipsperhand=[]
        self.current_hand=-1
        
    def ValidMoves(self):
        '''This function returns the Valid move set to the main function 
        based on which the input is processed'''
        if self.current_hand==-1:
            return 'dq'
        elif self.current_hand==0:
            # CHECK IF SPLIT is possible, Max number of splits reached, then no ?
            if self.hands[0][0].value==self.hands[0][1].value and len(self.hands)+1<=3:
                if len(self.hands[self.current_hand])==2 and len(self.hands)<2:
                    return 'uhsp'
                else:
                    return 'hsp'               
            else:
                if len(self.hands[self.current_hand])==2 and len(self.hands)<2:
                    return 'uhs'
                elif len(self.hands[self.current_hand])>=5:
                    return 'Maximum number of hits reached'               
                else:
                   return 'hs'  
        elif len(self.hands[self.current_hand])>=5:
            return 'Maximum number of hits reached'
        else:
            return 'hs'
            
    def PrintValidMoves(self):
        '''Used to Prints instruction for adding valid moves on the screen'''
        
        if self.current_hand==-1:
            return '\nType D for Deal and Q to Quit-->'
        elif self.current_hand==0:
            if self.hands[0][0].value==self.hands[0][1].value and len(self.hands)+1<3:
                if len(self.hands[self.current_hand])==2 and len(self.hands)<2:
                    return '\nFor Hand no.'+ str(self.current_hand+1)+'\nU to surrender, \nH to Hit, \nS to Stand or \nP to Split for Hand no.'+ str(self.current_hand+1)+ '-->'
                else:
                    return '\nFor Hand no.'+ str(self.current_hand+1)+'\nH to Hit, \nS to Stand or \nP to Split -->'               
            else:
                if len(self.hands[self.current_hand])==2 and len(self.hands)<2:
                    return '\nFor Hand no.'+ str(self.current_hand+1)+'\nU to surrender, \nH to Hit, Or \nS to Stand '+ '-->'               
                elif len(self.hands[self.current_hand])>=5:
                    return 'Maximum number of hits reached'
                else: 
                   return '\nFor Hand no.'+ str(self.current_hand+1)+'\nH to Hit, or \nS to Stand -->'
        elif len(self.hands[self.current_hand])>=5:
            return 'Maximum number of hits reached'
        else:
            return '\nFor Hand no.'+ str(self.current_hand+1)+  '\nH to Hit, or \nS to Stand -->'
        
##########        
class Dealer(object):
    '''Atrributes of the player, which are his 1. hands: List of list of cards in 
    the hand, 2. score for the hand (list of list), 3. card status: OPEN (SHOWING) 
    or CLOSE (NOT SHOWING) 4.. Current hand: Index of the hand that is currently playing, which is always one'''
    def __init__(self):
        self.hands=[[]]
        self.openclose=['close','open']
        self.score=[[0]]
        self.current_hand=0
        