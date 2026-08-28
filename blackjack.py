import pygame
import random
import os
from package.cosntants import * # constant dependency package. although polutting file namespace with constant values may cause issues...

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack")
clock = pygame.time.Clock()  # Initialize the clock object

class Card:
    def __init__(self, value, suit, size):
        self.value = value
        self.suit = suit
        self.size = size 

    def get_image_url(self):
        card = f"{os.getcwd()}/cards/{self.value}-{self.suit}.png" 
        return card

    def __repr__(self): # not __str__ weird dundee methods 
        return f"{self.value} {self.suit}"

class Card_GUI:
    def __init__(self, entity, card_size=90):
        self.entity = entity
        self.card_size = card_size

    def display_hand(self, card_x=0):
        card_y = HEIGHT-self.card_size
        for url in [card.get_image_url() for card in self.entity.hand]:
            if (card_x > WIDTH-60): # will need alternative resolution logic
                card_x = 0
                card_y -= self.card_size

            image = pygame.image.load(url)
            image = pygame.transform.scale(image, (self.card_size, self.card_size))
            screen.blit(image, (card_x, card_y))
            card_x += self.card_size




class Entity:
    def __init__(self, name=""):
        self.value = 0
        self.name = name
        self.hand = []
        self.ace_count = 0
        self.end_turn = False

    def output_card(self, card_gui: Card_GUI, card_x=0): # defualt arg not great there is a better way of handling data surely
        card_gui.display_hand(card_x)

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
        # if (self.value < 16 and player.value > 18):
        #     self.hand.append(deck.pop(0))

        while (self.value != BLACKJACK and player.value == BLACKJACK): # drains the deck not to sure why needs to ne debugged
            self.hand.append(deck.pop(0))
               
    def deal_cards(self, entity: Entity, deck: list[Card]):
        for _ in range(2):
            self.give_card(self, deck)
            self.give_card(entity, deck)

    #overriding inherited function not sure if there is a better approach
    # def card_gui(self, player: Entity):
    #         card_x = 30
    #         image = pygame.transform.scale(self.hand[0].get_image_url(),(CARD_WxH,CARD_WxH))
    #         screen.blit(image,(card_x, 50 ))
    #         card_x += CARD_WxH

class Blackjack:
    def __init__(self, player: Entity, dealer: Dealer):
        self.player = player
        self.dealer = dealer


    @staticmethod
    def init_deck(deck: list[Card]):
        for suit in SUITS:
            for value in FACE_VALUES + VALUES:
                deck.append(Card(value, suit, 90))
        random.shuffle(deck)

    
    
    def run(self): 
        deck: list[Card] = []
        Blackjack.init_deck(deck)
        print(deck)
        running = True

        self.dealer.deal_cards(self.player, deck)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()

            self.player.hand_sum()
            self.dealer.hand_sum()

            screen.fill((50,225,10))

            if keys[pygame.K_SPACE]:
                ...

            # self.dealer.logic(deck, self.player)
            # self.dealer.card_gui(self.player)
            # print(self.dealer.hand_sum()) =




            self.player.output_card(Card_GUI(self.player))
            
            pygame.display.flip()
            clock.tick(10.0)
            pygame.display.update()

if __name__ == "__main__":
    blackjack = Blackjack(Entity("Jacob"), Dealer("John"))
    blackjack.run()