### DEFINE CLASS FOR CARDS####
import random
class Card(object):
    ''' This class is used to generate an instance of a card 
    which has a rank, suite, value(i.e. the score) in the game, and 
    a symbol (in unicode encoding)'''
    def __init__(self,rank,suite):
        self.rank=rank
        self.suite=suite
        self.value=[]
        self.DefineValue()
        self.DefineSymbol()
    def DefineValue(self):
        if self.rank==1:
            self.value=[1,11]
        elif self.rank>=10:
            self.value.append(10)
        else:
            self.value.append(self.rank)
    def DefineSymbol(self):
        ### GENERATER SYMBOL for each card
        dict_ranks={1:'A',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',
        8:'8',9:'9',10:'10',11:'J',12:'Q',13:'K'}
        self.symbol=dict_ranks[self.rank]+'('+self.suite[0]+')'
            
        
class Deck(object):
    '''This object holds the deck of cards'''
    def __init__(self):        
        self.deckofcards=[]
        self.MakeDeckOfCards()
    
    def MakeDeckOfCards(self):
        ranks=range(1,14)
        suite=['Spade','Heart','Diamond','Club']
        for i in ranks:
            for j in suite:
                self.deckofcards.append(Card(i,j))  
    def DrawCard(self):
        indexofcard=random.choice(range(len(self.deckofcards)))
        newcard=Card(self.deckofcards[indexofcard].rank,
        self.deckofcards[indexofcard].suite)
        self.deckofcards.pop(indexofcard)
        return newcard