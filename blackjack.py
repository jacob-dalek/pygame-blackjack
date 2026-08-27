import pygame
import random
import os

WIDTH = 640
HEIGHT = 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))

SUITS = ['C', 'D', 'H', 'S']
FACE_VALUES = ['J','K','Q','A']
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

    def __str__(self):
        return f"{self.value} {self.suit}"

def init_deck(deck: list[Card]):
        for suit in SUITS:
            for value in VALUES + FACE_VALUES:
                deck.append(Card(value, suit))
        random.shuffle(deck)


class Entity:
    def __init__(self, name=""):
        self.__value = 0
        self.name = name
        self.hand = []
        self.ace_count = 0

    def card_GUI(self): # not very pythonic


    def hand_sum(self):
        if not self.hand and len(self.hand) < 1:
            return self.__value
        sum = 0
        for card in self.hand:
            sum += card_logic(card.value, self)
        self.__value = sum

def card_logic(value, entity: Entity):
        if value not in FACE_VALUES:
            return value
        if value == 'A':
            ++entity.ace_count
        else:
            return 10
        
def give_card(deck: list[Card])-> Card:
    return deck.pop(0)

class Dealer(Entity):
    def __init__(self, name=""):
        super().__init__(name)

    

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

            screen.fill((100,255,0))
            pygame.display.flip()
            pygame.display.update()

if __name__ == "__main__":
    Blackjack.run()