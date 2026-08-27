import pygame
import random
import os

WIDTH = 640
HEIGHT = 320

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.init()
pygame.display.set_caption("Blackjack")
clock = pygame.time.Clock()  # Initialize the clock object


BLACKJACK = 21
CARD_WxH = 100

SUITS = ['C', 'D', 'H', 'S']
FACE_VALUES = ['Q','J','K','A']
VALUES = [2,3,4,5,6,7,8,9,10]


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
            for value in FACE_VALUES + VALUES:
                deck.append(Card(value, suit))
        random.shuffle(deck)


class Entity:
    def __init__(self, name=""):
        self.value = 0
        self.name = name
        self.hand = []
        self.ace_count = 0

        # value is slightly broken if get_sum is not invoked

    @property
    def get_value(self) -> int:
        return self.value # python encapsulation weird???...

    def card_GUI(self):
        print(self.hand) # not very pythonic GUI

        card_x = 0     
        card_y = HEIGHT-CARD_WxH 
        for card in self.hand: # could use list for loops but not in the mood
            if (card_x > WIDTH-60):
                card_x = 0
                card_y -= 90
            image = pygame.transform.scale(card.get_image(),(CARD_WxH,CARD_WxH)) # perhaps i could override or create my own method instead of repeating logic...
            screen.blit(image,(card_x,card_y))
            card_x += CARD_WxH


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

    def give_card(self, entity: Entity, deck: list[Card]):
        entity.hand.append(deck.pop(0))

    def reveal_card(self):
        self.hand[0]

    def logic(self, deck: list[Card], player: Entity):
        if (self.value == 17):
            return self.value
        if (self.value < 16 and player.value > 18):
            self.hand.append(deck.pop(0))

        while (self.value != BLACKJACK and player.value == BLACKJACK):
            self.hand.append(deck.pop(0))
               



    def deal_cards(self, entity: Entity, deck: list[Card]):
        for card in range(2): # this is the first hand
            self.hand.append(give_card(deck))
            entity.hand.append(give_card(deck)) # i feel like this can be DNRY'd

    #overriding inherited function not sure if there is a better approach
    def card_GUI(self):
            card_x = 30
            image = pygame.transform.scale(self.hand[0].get_image(),(CARD_WxH,CARD_WxH))
            screen.blit(image,(card_x, 50 ))
            card_x += CARD_WxH


            # for card in self.hand: # could use list for loops but not in the mood
            #     image = pygame.transform.scale(card.get_image(),(CARD_WxH,CARD_WxH))
            #     screen.blit(image,(card_pos, 50 ))
            #     card_pos += CARD_WxH

class Blackjack:

    def __init__(self, player: Entity, dealer: Dealer):
        self.player = player
        self.dealer = dealer
    
    def run(self): 
        deck: list[Card] = []
        init_deck(deck)
        running = True

        self.dealer.deal_cards(self.player, deck)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()

            self.player.hand_sum()
            self.dealer.hand_sum()

            screen.fill((50,255,10))

            if keys[pygame.K_SPACE] and self.player.value != 21 and self.player.value < 21:
                self.dealer.give_card(self.player, deck)
                self.player.hand_sum()


            self.dealer.logic(deck, self.player)
            

            print(self.dealer.hand_sum())

            self.player.card_GUI()
            self.dealer.card_GUI()
            
            pygame.display.flip()
            clock.tick(10.0)
            pygame.display.update()

if __name__ == "__main__":
    blackjack = Blackjack(Entity("Jacob"), Dealer("John"))
    blackjack.run()