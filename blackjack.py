import pygame
import random
import os

WIDTH = 640
HEIGHT = 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
BLACKJACK = 21
CARD_WxH = 180

SUITS = ['C', 'D', 'H', 'S']
FACE_VALUES = ['A','A','A','A']
# VALUES = [2,3,4,5,6,7,8,9,10]


class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def get_image(self):
        card = f"{os.getcwd()}/cards/{self.value}-{self.suit}.png" 
        image = pygame.image.load(card)
        return image
        # image = pygame.transform.scale(image,(180,180))
        # screen.blit(image,(0,HEIGHT-180))

    def __repr__(self): # not __str__ weird dundee methods 
        return f"{self.value} {self.suit}"

def init_deck(deck: list[Card]):
        for suit in SUITS:
            for value in FACE_VALUES:
                deck.append(Card(value, suit))
        random.shuffle(deck)


class Entity:
    def __init__(self, name=""):
        self.value = 0
        self.name = name
        self.hand = []
        self.ace_count = 0

    @property
    def get_value(self) -> int:
        return self.value # python encapsulation weird???...

    

    def card_GUI(self):
        print(self.hand) # not very pythonic GUI

        card_pos = 0        
        for card in self.hand: # could use list for loops but not in the mood
            image = pygame.transform.scale(card.get_image(),(CARD_WxH,CARD_WxH))
            screen.blit(image,(card_pos,HEIGHT-CARD_WxH))
            card_pos += CARD_WxH


    def hand_sum(self):
        if not self.hand and len(self.hand) < 1:
            return self.value
        sum = 0
        for card in self.hand:
            sum += card_logic(card.value, self)

        self.value = sum

        ace_logic(self)
        
        return self.value

def card_logic(value, entity: Entity):        
        if value not in FACE_VALUES:
            return value
        if value == 'A':
            entity.ace_count += 1
            return 11
        
        else:
            return 10

def ace_logic(entity: Entity):
    while (entity.ace_count > 0 and entity.value > 21):
        entity.ace_count -= 1
        entity.value -= 10
     
def give_card(deck: list[Card])-> Card:
    return deck.pop(0)

class Dealer(Entity):
    def __init__(self, name=""):
        super().__init__(name)

    def give_card(entity: Entity, deck: list[Card]):
        entity.hand.append(deck.pop(0))

    def reveal_card(self):
        self.hand[0].load_image()

    def deal_cards(self, entity: Entity, deck: list[Card]):
        for card in range(2): # this is the first hand
            self.hand.append(give_card(deck))
            entity.hand.append(give_card(deck)) # i feel like this can be DNRY'd


class Blackjack:

    @staticmethod
    def run(): 
        clock = pygame.time.Clock()  # Initialize the clock object
        deck: list[Card] = []
        init_deck(deck)
        pygame.init()
        running = True

        dealer: Dealer = Dealer("John")
        me: Entity = Entity("Jacob")
        dealer.deal_cards(me, deck)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False


            screen.fill((50,255,10))

            me.card_GUI()
            

            print(me.hand_sum())

            
            pygame.display.flip()
            pygame.display.update()

if __name__ == "__main__":
    Blackjack.run()