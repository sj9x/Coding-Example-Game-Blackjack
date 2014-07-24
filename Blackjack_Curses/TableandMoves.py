import curses
from ScreenFunctions import*

class Table(object):
    '''The Table has 1 player, 1 dealer, 1 deck, 1 screen
    and a status i.e., whether the cards are being dealt, hit, stand'''
    '''Apart from things, Table has MOVES which are the functions in this class:
    Deal, Surrender,Split,Hit, Stand, Dealer Draws Cards, TallyScore '''
    ''' There are also events which are Updatecardsandscores and PrintCards'''
    def __init__(self,p1,d1,deck1,screen):
        self.p1=p1 # This is the player
        self.d1=d1 # This is the dealer
        self.deck1=deck1 # This is the deck 
        self.tableStatus='d' # This is the table status
        self.screen=screen # This is the screen
        
    ## ####Update Cards###
    def UpdateCards(self,person):
        '''This function updates cards and scores for the person who can be dealer or the player,
        If the table status is deal, it deals two cards, else 1 card'''
        if self.tableStatus=='d' or self.tableStatus=='D' :
            cardsToDraw=2
        else:
            cardsToDraw=1
        for i in range(cardsToDraw): 
            card=self.deck1.DrawCard()
            person.score[person.current_hand]=ScoreCalculator(person.score[person.current_hand],card.value)
            person.hands[person.current_hand].append(card)
    ######## MOVES###################################
    def Deal(self):
        '''Step 1: Ask the player for the bet money
        if the input is not an integer, ask again
        Step2: Update players and the dealers cards
        Step3 : If anyone has 21 the game is over and go to Final Tally Score
        else just print cards (return True)'''
    #'''Initialize everything and Draws cards and print return false if player has blackjack'''
    # Step1: Ask for the betting money
        while True:
            self.screen.addstr(14,0,'\nHow many chips to bet, Min bet =1 and Max bet ='+str(self.p1.chips)+'-->')
            bet=self.screen.getstr() 
            try:
                bet = int(bet)
                if bet<=self.p1.chips and bet >=1:
                    break
                else: 
                    self.screen.addstr(13,0,'\nNo. of chips should be an integer')      
            except ValueError:
                self.screen.addstr(13,0,'\nNo. of chips should be an integer')

        self.p1.chips-=float(bet)
        self.p1.chipsperhand.append(float(bet))
    
    
    ### Step2: Draw cards for player and print 
    #'''Draw card and update score can be combined'''
        self.UpdateCards(self.p1)
    
        # Step3: Draw card for dealer and print
        self.UpdateCards(self.d1)
        # CHECK IF ANYONE HAS BLACKJACK (Move to dealdraws or Tally scores)
        if self.d1.score[0][0] == 21 or self.p1.score[0][0]==21:
            self.FinalTallyScores()
            return False
        else:
            self.PrintCards('Cards:')
            return True
             
    ## Surrender    
    def Surrender(self):
        ''''If the player wants to surrender, open the dealers card
        return half of the players chips and print scores, return False'''
        '''The presentation for the final results will have a header
        depending on the result
        The PrintCards fn takes this header as an input'''
        
        header='*'*20 + 'Game Over' + '*'*20+'\nYou Surrendered!\nFinal Results:'
        self.p1.handstatus[0]='Surrendered'
        self.d1.openclose[0]='open'
        self.p1.chips+=0.5*self.p1.chipsperhand[0]
        self.p1.chipsperhand[0]=[0]
        self.PrintCards(header)
        self.screen.getch()  
        return False
        ####### SPLIT    
    
    def split(self):
        '''Input: object of type player, table
        Splits the player cards and draws a card for the first hand 
        Update players cards and its status of the player
        If the hand one score is 21, put it on Stand else return
        to the main program after printing the cards'''
    
        # add another hand and remove one card from first hand
        self.p1.hands.append([self.p1.hands[0][0]])
        self.p1.handstatus.append('Playing')
        self.p1.hands[0].pop(1)
        
        # add another element to list of Players score 
        self.p1.score[0]=self.p1.hands[0][0].value
        self.p1.score.append(self.p1.hands[0][0].value)
        
        # Update his chips
        self.p1.chips-=self.p1.chipsperhand[0]
        self.p1.chipsperhand.append(self.p1.chipsperhand[0])
        
        # Update cards for hand 1(not for hand 2)
        self.UpdateCards(self.p1)
        
        # CHECK IF Hand 1 Has 21
        if self.p1.score[self.p1.current_hand][0] ==21:
            self.p1.handstatus[self.p1.current_hand]='On Stand'
            return self.StandCurrentHand()  
        else:
            self.PrintCards('Cards:')
            return True   
    
    ####### HIT
    
    def hit(self):
        '''Increase players card and  call the Updates players card 
        and scores function
        If the score > 21, make the current hand status = Bust and put it on stand
        else if it ==21, put it on stand, else return '''
        '''The presentation for the final results will have a header
        depending on the result
        The PrintCards fn takes this header as an input'''
        
        self.UpdateCards(self.p1)
    
        if self.p1.score[self.p1.current_hand][0]>21:
            self.p1.handstatus[self.p1.current_hand]='Bust'  
            return self.StandCurrentHand()  
        elif self.p1.score[self.p1.current_hand][0]==21:
            self.p1.handstatus[self.p1.current_hand]='On Stand' # Line Can be removed
            return self.StandCurrentHand()      
        else: 
            self.PrintCards('Cards:')        
            return True
     
     #########
    def StandCurrentHand(self):
        '''When the player goes on Stand his score is fixed to his max score 
        which is less than 21
        If we have scanned through all the hands and they are either Bust or
        on Stand, open dealers card. If all hands are bust,
        Print result else dealer compares and draws a card. Otherwise
        move to the next hand by increasing the index (self.current_hand)'''
        '''The presentation for the final results will have a header
        depending on the result
        The PrintCards fn takes this header as an input'''
        
        
        self.p1.score[self.p1.current_hand]=[max(self.p1.score[self.p1.current_hand])]
        if self.p1.current_hand+1==len(self.p1.hands):
            self.d1.openclose[0]='open'    
            if all(map(lambda x: x=='Bust',self.p1.handstatus)):
               self.FinalTallyScores()
               return False
            else:
                self.DealerDraws()
                return False
            return False
        else:
            self.p1.current_hand+=1
            return self.hit()
            
     
    ## Dealer Draws               
    def DealerDraws(self):
        ''' If dealers score is greater than 17 or higher thanall of the 
        players hands, then tallyscore else dealer draws a card, the status of 
        the new card is OPEN
        The presentation for the Cards will have a header
        depending on the result.The PrintCards fn takes this header as an input'''
        
        # CHECK IF BOTH HANDS ALREADY BUST    
        
        while True:    
            if max(self.d1.score[0])>=17 or (max(self.d1.score[0])<17 and max(self.d1.score[0])> max(self.p1.score)):
                self.FinalTallyScores()
                break
            else: 
                self.UpdateCards(self.d1)
                self.d1.openclose.append('open')
                self.PrintCards('Cards:--->')   
     ## Final Tally Score       
    def FinalTallyScores(self):
        '''Final Score Tally, We will check for Blackjack and check for the
        players hands that have been lost, won, or push'''
        '''The presentation for the final results will have a header
        depending on the result
        The PrintCards fn takes this header as an input'''
        
        self.d1.openclose[0]='open'
        
        header='*'*20 + 'Game Over' + '*'*20
        
        # BLACKJACK CHECK 
        if self.tableStatus.lower()=='d':            
            if self.d1.score[0][0] == 21 and self.p1.score[0][0] != 21:
                self.p1.handstatus[0]='Lost'
                header=header+'\nYou loose dealer has Blackjack !'
            elif self.p1.score[0][0] == 21 and self.d1.score[0][0] != 21:
                self.p1.handstatus[0]='Won'
                header= header+'\nBlackjack You win !!!'
                self.p1.chips+=self.p1.chipsperhand[0]*2.5
            else: 
                self.p1.handstatus[0]='Push'
                header = header+'\nDealer and You have 21'
                self.p1.chips+=self.p1.chipsperhand[0]*1.0
                
        # CHECK IF DEALER IS BUST (Remember that at least one playe
        # hand is not bust)       
        elif max(self.d1.score[0])>21:
            for i in range(len(self.p1.hands)):
                if self.p1.handstatus[i]!= 'Lost' and self.p1.handstatus[i]!= 'Bust':
                    self.p1.handstatus[i]='Won'
                    self.p1.chips+=2.0*self.p1.chipsperhand[i]
                    header= header +'\nFinal Results'
        
        else: # COMPARE
            for i in range(len(self.p1.hands)):
                if self.p1.handstatus[i]!= 'Lost' and self.p1.handstatus[i]!= 'Bust':
                    if max(self.d1.score[0])>self.p1.score[i][0]:
                        self.p1.handstatus[i]='Lost'
                    elif max(self.d1.score[0])==self.p1.score[i][0]:
                        self.p1.handstatus[i]='Push'
                        self.p1.chips+=self.p1.chipsperhand[i]
                    else:
                        self.p1.handstatus[i]='Won'
                        self.p1.chips+=2.0*self.p1.chipsperhand[i] 
                        header=header +'\nFinal Results'
        self.p1.chipsperhand=[0]  
        self.PrintCards(header) 
        self.screen.getch()  
        return False
        
    ###RINT CARDS  AND FINAL SCORE
    def PrintCards(self,header):
        ''' This function will be used to print the results in the format
        Hand no. Card1, Card2, Score, and Status for the player and the dealer'''
        '''The presentation for the final results will have a header
        depending on the result
        The PrintCards fn takes this header as an input'''
        
        ClearScreen(self.screen)
        self.screen.addstr(10,0,header,curses.A_BOLD)
        self.screen.addstr(12,0,'(Chips on bet = ' + str(self.p1.chipsperhand))
        self.screen.addstr(', Chips in hand = ' + str([self.p1.chips])+')')
    #Players cards AND SCORE
        for j in range(len(self.p1.hands)):      
            allcards=''
            for i in range(len(self.p1.hands[j])):
                allcards=allcards+' ' + self.p1.hands[j][i].symbol
            self.screen.addstr('\nHand '+str(j+1)+ ':'+ allcards + '  Score = '+str(self.p1.score[j])+'     Status: '+ self.p1.handstatus[j] )
                
   ### PRINT Dealers cards and SCORE
        allcards=''
        if self.d1.openclose[0]=='close': 
            deal_score=['not revealed']
        else: 
            deal_score=self.d1.score[0]
        for i in range(len(self.d1.openclose)):
            if self.d1.openclose[i]=='open':
                    allcards=allcards+' '+self.d1.hands[0][i].symbol
        self.screen.addstr('\nDealer'+ ':'+ allcards+ '  Score =' + str(deal_score)  )
        self.screen.addstr('\n'+'*'*40)
####### ADD SCORE OF NEW CARD ########################
def ScoreCalculator(oldscore,value):
    '''Adds value (list object) of the new card to the oldscore (list object)
    returns newscore(list object)'''
    newscore=[]
    for j in range(len(oldscore)):
        for i in range(len(value)):
            summation=oldscore[j]+value[i]
            if summation == 21 or newscore == [21]:
                newscore=[21]
            elif summation not in newscore: 
                newscore.append(oldscore[j]+value[i])
    if len([x for x in newscore if x>21])>0 and len([x for x in newscore if x<=21])>0:
         newscore=[x for x in newscore if x<=21]  
    return newscore   